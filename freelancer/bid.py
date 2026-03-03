from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from freelancer.selectors import (
    BID_SUBMIT_BUTTON_XPATH,
    BID_TEXTAREA_XPATH,
    QUESTION_SUBMIT_BUTTON_XPATH,
    QUESTION_TEXTAREA_XPATH,
)
from openai_bid import generate_bid, parse_bid_and_question


def fill_bid_and_submit(
    driver: webdriver.Chrome,
    title: str,
    details: str,
    bid_wait_timeout_seconds: int,
) -> None:
    """
    If the bid textarea exists: generate bid from AI, fill bid and question
    fields, then click the submit button. Otherwise skip without calling the AI.
    """
    wait = WebDriverWait(driver, bid_wait_timeout_seconds)
    try:
        bid_element = wait.until(
            EC.presence_of_element_located((By.XPATH, BID_TEXTAREA_XPATH))
        )
    except TimeoutException:
        print("Bid textarea not found on this page; skipping AI call.")
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

    if question_text:
        try:
            question_element = driver.find_element(By.XPATH, QUESTION_TEXTAREA_XPATH)
            question_element.clear()
            question_element.send_keys(question_text)
        except NoSuchElementException:
            print("Question textarea not found; filled bid only.")

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
