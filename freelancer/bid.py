import logging
import platform
import re
from typing import Literal, Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from freelancer.selectors import (
    BID_AMOUNT_INPUT_XPATH,
    BID_INCONSISTENT_MESSAGE_TEXT,
    BID_INCONSISTENT_MESSAGE_XPATH,
    BID_SUBMIT_BUTTON_XPATH,
    BID_TEXTAREA_XPATH,
    PROJECT_BUDGET_XPATH,
    QUESTION_AREA_XPATH,
    QUESTION_SUBMIT_BUTTON_XPATH,
    QUESTION_TEXTAREA_XPATH,
    RETRACT_BID_BUTTON_XPATH,
    RETRACT_BID_CONFIRM_BUTTON_XPATH,
)
from config import FREELANCER_USER_ID
from openai_bid import generate_bid, parse_bid_and_question

logger = logging.getLogger(__name__)


def _parse_min_budget_amount(budget_text: str) -> Optional[str]:
    """Extract the minimum amount from budget text like '$10.00 – 30.00 USD'."""
    numbers = [
        float(match.replace(",", ""))
        for match in re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?", budget_text)
    ]
    if not numbers:
        return None
    min_val = min(numbers)
    if min_val == int(min_val):
        return str(int(min_val))
    return str(min_val)


def _clear_and_type_input(element, value: str) -> None:
    """Clear a pre-filled input and type a new value."""
    element.click()
    select_all_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
    element.send_keys(select_all_key, "a")
    element.send_keys(Keys.BACKSPACE)
    element.clear()
    element.send_keys(value)


def _fill_bid_amount_from_budget(driver: webdriver.Chrome) -> bool:
    """Read project budget, set bid amount input to the minimum value."""
    url = driver.current_url
    try:
        budget_el = driver.find_element(By.XPATH, PROJECT_BUDGET_XPATH)
        budget_text = (budget_el.text or "").strip()
        min_amount = _parse_min_budget_amount(budget_text)
        logger.debug(
            "Parsed budget budget_text=%r min_amount=%r url=%s",
            budget_text,
            min_amount,
            url,
        )
        if not min_amount:
            logger.warning(
                "Could not parse min budget amount; skipping bid amount fill url=%s",
                url,
            )
            return False

        bid_amount_el = driver.find_element(By.XPATH, BID_AMOUNT_INPUT_XPATH)
        existing_value = (bid_amount_el.get_attribute("value") or "").strip()
        _clear_and_type_input(bid_amount_el, min_amount)
        logger.info(
            "Bid amount updated existing=%r updated=%r url=%s",
            existing_value,
            min_amount,
            url,
        )
        return True
    except NoSuchElementException:
        logger.warning(
            "Budget or bid amount input not found; skipping bid amount fill url=%s",
            url,
        )
        return False


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


BidOutcome = Optional[Literal["success", "failed"]]


def fill_bid_and_submit(
    driver: webdriver.Chrome,
    title: str,
    details: str,
    wait_timeout_seconds: int,
) -> BidOutcome:
    """
    If the bid textarea exists: generate bid from AI, fill bid and question
    fields, then click the submit button. Otherwise skip without calling the AI.

    Returns:
        "success" if bid stayed submitted (no inconsistent-profile message),
        "failed" if bid could not be completed or was inconsistent/retracted,
        None if skipped (e.g. no bid textarea on page).
    """
    url = driver.current_url
    wait = WebDriverWait(driver, wait_timeout_seconds)
    try:
        bid_element = wait.until(
            EC.presence_of_element_located((By.XPATH, BID_TEXTAREA_XPATH))
        )
    except TimeoutException:
        logger.info("Bid skipped: textarea not found url=%s", url)
        return None

    model_response = generate_bid(title, details)
    if model_response.startswith("Error:"):
        logger.error("AI generation failed url=%s error=%s", url, model_response)
        return "failed"

    bid_text, question_text = parse_bid_and_question(model_response)
    if not bid_text:
        logger.warning(
            "Could not parse bid text from model response url=%s", url
        )
        return "failed"

    bid_element.clear()
    bid_element.send_keys(bid_text)

    has_previous_question = _question_area_contains_user_id(driver, FREELANCER_USER_ID)
    if has_previous_question:
        logger.info(
            "Question skipped: previous question exists url=%s", url
        )
    elif question_text:
        try:
            question_element = driver.find_element(By.XPATH, QUESTION_TEXTAREA_XPATH)
            question_element.clear()
            question_element.send_keys(question_text)
            question_btn = driver.find_element(By.XPATH, QUESTION_SUBMIT_BUTTON_XPATH)
            question_btn.click()
            logger.info("Question inserted url=%s", url)
        except NoSuchElementException:
            logger.warning(
                "Question textarea or submit button not found url=%s", url
            )

    _fill_bid_amount_from_budget(driver)

    try:
        bid_btn = driver.find_element(By.XPATH, BID_SUBMIT_BUTTON_XPATH)
        bid_btn.click()
    except NoSuchElementException:
        logger.error(
            "Bid submit button not found; question may have been submitted url=%s",
            url,
        )
        return "failed"

    found_inconsistent = False
    try:
        msg_el = WebDriverWait(driver, wait_timeout_seconds + 10).until(
            EC.presence_of_element_located((By.XPATH, BID_INCONSISTENT_MESSAGE_XPATH))
        )
        if msg_el and BID_INCONSISTENT_MESSAGE_TEXT in (msg_el.text or ""):
            found_inconsistent = True
            logger.warning(
                "Bid inconsistent with profile; retracting url=%s", url
            )
            retract_btn = driver.find_element(By.XPATH, RETRACT_BID_BUTTON_XPATH)
            retract_btn.click()
            confirm_btn = WebDriverWait(driver, wait_timeout_seconds).until(
                EC.element_to_be_clickable((By.XPATH, RETRACT_BID_CONFIRM_BUTTON_XPATH))
            )
            confirm_btn.click()
            logger.info("Bid retracted url=%s", url)
    except TimeoutException:
        pass
    except NoSuchElementException:
        logger.warning(
            "Retract bid button not found; bid may be inconsistent url=%s", url
        )

    if not found_inconsistent:
        logger.info("Bid submitted successfully url=%s", url)
        return "success"
    return "failed"
