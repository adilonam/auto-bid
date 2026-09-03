import logging
from pathlib import Path

from selenium import webdriver

from browser.cookies import load_cookies, save_cookies

logger = logging.getLogger(__name__)


def is_logged_in(driver: webdriver.Chrome, login_url: str) -> bool:
    return "login" not in driver.current_url


def ensure_logged_in(
    driver: webdriver.Chrome,
    login_url: str,
    cookies_path: Path,
    prompt: str = "Log in in the browser, then press Enter here to continue... ",
) -> bool:
    """Ensure the session is logged in. Returns True if user logged in manually (already on target page)."""
    driver.get(login_url)
    had_cookies = load_cookies(driver, cookies_path)
    if had_cookies:
        logger.info("Loaded saved cookies path=%s", cookies_path)
        driver.refresh()
    else:
        logger.info("No saved cookies found path=%s", cookies_path)

    if not is_logged_in(driver, login_url):
        logger.warning("Not logged in; waiting for manual login url=%s", login_url)
        input(prompt)
        save_cookies(driver, cookies_path)
        logger.info("Manual login complete; cookies saved path=%s", cookies_path)
        return True

    logger.info("Session active url=%s", driver.current_url)
    return False
