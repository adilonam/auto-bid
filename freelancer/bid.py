from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from freelancer.selectors import (
    BID_INCONSISTENT_MESSAGE_TEXT,
    BID_INCONSISTENT_MESSAGE_XPATH,
    BID_SUBMIT_BUTTON_XPATH,
    BID_TEXTAREA_XPATH,
    QUESTION_AREA_XPATH,
    QUESTION_SUBMIT_BUTTON_XPATH,
    QUESTION_TEXTAREA_XPATH,
    RETRACT_BID_BUTTON_XPATH,
    RETRACT_BID_CONFIRM_BUTTON_XPATH,
)
from config import FREELANCER_USER_ID
from openai_bid import generate_bid, parse_bid_and_question


def _question_area_contains_user_id(driver: webdriver.Chrome, user_id: str) -> bool:
    """Return True if any descendant of the question area has text containing user_id."""
    try:
        area = driver.find_element(By.XPATH, QUESTION_AREA_XPATH)
    except NoSuchElementException:
        return False
    for el in area.find_elements(By.XPATH, ".//*"):
        if user_id in (el.text or ""):
            return True
    return False


def fill_bid_and_submit(
    driver: webdriver.Chrome,
    title: str,
    details: str,
    wait_timeout_seconds: int,
) -> None:
    """
    If the bid textarea exists: generate bid from AI, fill bid and question
    fields, then click the submit button. Otherwise skip without calling the AI.
    """
    wait = WebDriverWait(driver, wait_timeout_seconds)
    try:
        bid_element = wait.until(
            EC.presence_of_element_located((By.XPATH, BID_TEXTAREA_XPATH))
        )
    except TimeoutException:
        print("Bid textarea not found, url:", driver.current_url)
        return

    print("Generating from AI model...")
    model_response = generate_bid(title, details)
    if model_response.startswith("Error:"):
        print(model_response)
        return

    bid_text, question_text = parse_bid_and_question(model_response)
    if not bid_text:
        print("Could not parse bid text from model response; skipping fill.")
        return

    bid_element.clear()
    bid_element.send_keys(bid_text)

    has_previous_question = _question_area_contains_user_id(driver, FREELANCER_USER_ID)
    if has_previous_question:
        print("Previous question from you found on this project; skipping question, url:", driver.current_url)
    if question_text and not has_previous_question:
        try:
            question_element = driver.find_element(By.XPATH, QUESTION_TEXTAREA_XPATH)
            question_element.clear()
            question_element.send_keys(question_text)
        except NoSuchElementException:
            print("Question textarea not found; filled bid only.")

    if question_text and not has_previous_question:
        try:
            question_btn = driver.find_element(By.XPATH, QUESTION_SUBMIT_BUTTON_XPATH)
            question_btn.click()
        except NoSuchElementException:
            print("Question submit button not found; bid and question filled but not submitted.")
            return

    try:
        bid_btn = driver.find_element(By.XPATH, BID_SUBMIT_BUTTON_XPATH)
        bid_btn.click()
    except NoSuchElementException:
        print("Bid submit button not found; question was submitted but bid was not.")
        return

    # After bid submit: if "inconsistent with profile" message appears, click retract bid
    try:
        msg_el = WebDriverWait(driver, wait_timeout_seconds).until(
            EC.presence_of_element_located((By.XPATH, BID_INCONSISTENT_MESSAGE_XPATH))
        )
        if msg_el and BID_INCONSISTENT_MESSAGE_TEXT in (msg_el.text or ""):
            print("Bid is inconsistent with profile; retracting bid. url:", driver.current_url)
            retract_btn = driver.find_element(By.XPATH, RETRACT_BID_BUTTON_XPATH)
            retract_btn.click()
            confirm_btn = WebDriverWait(driver, wait_timeout_seconds).until(
                EC.element_to_be_clickable((By.XPATH, RETRACT_BID_CONFIRM_BUTTON_XPATH))
            )
            confirm_btn.click()
    except TimeoutException:
        pass
    except NoSuchElementException:
        print("Retract bid button not found; bid may be inconsistent.")
