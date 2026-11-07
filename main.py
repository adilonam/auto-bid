import logging
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# Optional PROXY: route browser and API traffic through it when set.
_proxy = os.environ.get("PROXY", "").strip()
if _proxy:
    for _k in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
        os.environ[_k] = _proxy
    os.environ["NO_PROXY"] = os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import COOKIES_FILE, DEFAULT_SEARCH_PROJECTS_URL, LOGIN_URL, TARGET_URL
from config.logging_setup import setup_logging
from freelancer import fill_bid_and_submit, get_project_links, get_project_title_and_details

logger = logging.getLogger(__name__)


def _log_public_ip() -> None:
    proxy_enabled = bool(_proxy)
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        public_ip = response.json().get("ip", "unknown")
        logger.info(
            "Public IP address ip=%s proxy_enabled=%s",
            public_ip,
            proxy_enabled,
        )
    except Exception as e:
        logger.warning(
            "Failed to fetch public IP error=%s proxy_enabled=%s",
            str(e),
            proxy_enabled,
        )


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    log_path = setup_logging()
    logger.info("Logging initialized log_file=%s", log_path)
    _log_public_ip()

    search_projects_url = os.environ.get("SEARCH_PROJECTS_URL", DEFAULT_SEARCH_PROJECTS_URL)
    search_pages_start = int(os.environ.get("SEARCH_PAGES_START", "3"))
    search_pages_end = int(os.environ.get("SEARCH_PAGES_END", "10"))
    wait_timeout_seconds = int(os.environ.get("WAIT_TIMEOUT_SECONDS", "2"))
    max_bidders = int(os.environ.get("MAX_BIDDERS", "35"))
    retract_bid = _env_flag("RETRACT_BID", True)
    logger.info("Retract non-conform bids retract_bid=%s", retract_bid)
    logger.info("Max bidders before skip bid max_bidders=%s", max_bidders)

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
                    driver,
                    title,
                    details,
                    wait_timeout_seconds,
                    retract_bid,
                    max_bidders,
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
