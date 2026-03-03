from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import (
    BID_WAIT_TIMEOUT_SECONDS,
    COOKIES_FILE,
    LOGIN_URL,
    SEARCH_PAGES_END,
    SEARCH_PAGES_START,
    SEARCH_PROJECTS_URL,
    TARGET_URL,
)
from freelancer import fill_bid_and_submit, get_project_links, get_project_title_and_details


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
            index = 0
            total = len(links)
            while index < total:
                link_number = index + 1
                answer = input(
                    f"Press Enter to go to link {link_number}, "
                    f"or type 'r' then Enter to go back to link {link_number - 1}... "
                ).strip().lower()

                if answer == "r":
                    if index == 0:
                        print("Already at the first link; cannot go back further.")
                        continue
                    index -= 1
                    link_number = index + 1
                    print(f"Reversing to link {link_number}...")

                link = links[index]
                driver.get(link)
                title, details = get_project_title_and_details(driver)
                fill_bid_and_submit(
                    driver, title, details, BID_WAIT_TIMEOUT_SECONDS
                )
                index += 1

        input("Press Enter to close the browser... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
