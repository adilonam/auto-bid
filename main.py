from pathlib import Path

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import COOKIES_FILE, LOGIN_URL, TARGET_URL
from freelancer import get_project_links


def main() -> None:
    driver = create_chrome_driver()
    try:
        already_on_page = ensure_logged_in(driver, LOGIN_URL, Path(COOKIES_FILE))
        if not already_on_page:
            driver.get(TARGET_URL)

        links = get_project_links(driver)
        for url in links:
            print(url)

        input("Press Enter to close the browser... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
