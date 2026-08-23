import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import COOKIES_FILE, DEFAULT_SEARCH_PROJECTS_URL, LOGIN_URL, TARGET_URL
from config.logging_setup import setup_logging
from freelancer import fill_bid_and_submit, get_project_links, get_project_title_and_details

logger = logging.getLogger(__name__)


def main() -> None:
    log_path = setup_logging()
    logger.info("Logging initialized log_file=%s", log_path)

    search_projects_url = os.environ.get("SEARCH_PROJECTS_URL", DEFAULT_SEARCH_PROJECTS_URL)
    search_pages_start = int(os.environ.get("SEARCH_PAGES_START", "3"))
    search_pages_end = int(os.environ.get("SEARCH_PAGES_END", "10"))
    wait_timeout_seconds = int(os.environ.get("WAIT_TIMEOUT_SECONDS", "2"))

    driver = create_chrome_driver()
    try:
        ensure_logged_in(driver, LOGIN_URL, Path(COOKIES_FILE))
        driver.get(TARGET_URL)
        input("Press Enter to start... ")
        success_bids = 0
        failed_bids = 0
        for page in range(search_pages_start, search_pages_end + 1):
            logger.info("Starting page page=%s", page)
            url = f"{search_projects_url}&page={page}"
            driver.get(url)
            links = get_project_links(driver)
            logger.info("Found project links page=%s count=%s", page, len(links))
            for i, link in enumerate(links, start=1):
                logger.info("Starting project index=%s url=%s", i, link)
                driver.get(link)
                title, details = get_project_title_and_details(driver)
                outcome = fill_bid_and_submit(
                    driver, title, details, wait_timeout_seconds
                )
                if outcome == "success":
                    success_bids += 1
                elif outcome == "failed":
                    failed_bids += 1
                time.sleep(wait_timeout_seconds)
            logger.info(
                "Page done page=%s success_bids=%s failed_bids=%s",
                page,
                success_bids,
                failed_bids,
            )

        logger.info(
            "All pages done success_bids=%s failed_bids=%s",
            success_bids,
            failed_bids,
        )
        input("Press Enter to close the browser... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
