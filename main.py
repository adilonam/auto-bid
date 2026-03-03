from pathlib import Path

from browser import create_chrome_driver
from browser.session import ensure_logged_in
from config import COOKIES_FILE, LOGIN_URL, TARGET_URL
from freelancer import get_project_links


def main() -> None:
    driver = create_chrome_driver()
    try:
        ensure_logged_in(driver, LOGIN_URL, Path(COOKIES_FILE))
        driver.get(TARGET_URL)

        input("When you are on the project page, press Enter... ")
        links = get_project_links(driver)
        for url in links:
            print(url)

        input("Press Enter to close the browser... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
