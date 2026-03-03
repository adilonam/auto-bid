from pathlib import Path

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import (
    COOKIES_FILE,
    LOGIN_URL,
    SEARCH_PAGES_END,
    SEARCH_PAGES_START,
    SEARCH_PROJECTS_URL,
    TARGET_URL,
)
from freelancer import get_project_links


def main() -> None:
    driver = create_chrome_driver()
    try:
        ensure_logged_in(driver, LOGIN_URL, Path(COOKIES_FILE))
        driver.get(TARGET_URL)

        for page in range(SEARCH_PAGES_START, SEARCH_PAGES_END + 1):
            input(f"When you are ready, press Enter to start page {page}... ")
            url = f"{SEARCH_PROJECTS_URL}&page={page}"
            driver.get(url)
            links = get_project_links(driver)
            for u in links:
                print(u)

        input("Press Enter to close the browser... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
