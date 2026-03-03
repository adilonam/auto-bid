import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import COOKIES_FILE, DEFAULT_SEARCH_PROJECTS_URL, LOGIN_URL, TARGET_URL
from freelancer import fill_bid_and_submit, get_project_links, get_project_title_and_details


def main() -> None:
    search_projects_url = os.environ.get("SEARCH_PROJECTS_URL", DEFAULT_SEARCH_PROJECTS_URL)
    search_pages_start = int(os.environ.get("SEARCH_PAGES_START", "3"))
    search_pages_end = int(os.environ.get("SEARCH_PAGES_END", "10"))
    bid_wait_timeout_seconds = int(os.environ.get("BID_WAIT_TIMEOUT_SECONDS", "2"))
    link_wait_seconds = int(os.environ.get("LINK_WAIT_SECONDS", "3"))

    driver = create_chrome_driver()
    try:
        ensure_logged_in(driver, LOGIN_URL, Path(COOKIES_FILE))
        driver.get(TARGET_URL)
        input("Press Enter to start... ")
        for page in range(search_pages_start, search_pages_end + 1):
            print(f"Starting page {page}... ")
            url = f"{search_projects_url}&page={page}"
            driver.get(url)
            links = get_project_links(driver)
            for i, link in enumerate(links, start=1):
                driver.get(link)
                title, details = get_project_title_and_details(driver)
                fill_bid_and_submit(
                    driver, title, details, bid_wait_timeout_seconds
                )
                time.sleep(link_wait_seconds)

        input("Press Enter to close the browser... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
