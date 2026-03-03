from pathlib import Path

from selenium import webdriver

from browser.cookies import load_cookies, save_cookies


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
        driver.refresh()

    if not is_logged_in(driver, login_url):
        input(prompt)
        save_cookies(driver, cookies_path)
        return True
    return False
