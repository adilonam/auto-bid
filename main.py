import os
import time

from browser import create_chrome_driver
from config import TARGET_URL


def main() -> None:
    in_container = os.path.isfile("/usr/bin/chromium") or os.path.isfile("/usr/bin/chromium-browser")
    if in_container:
        # Default headless; set HEADLESS=0 to show browser via XQuartz on Mac
        headless = os.environ.get("HEADLESS", "1") == "1"
    else:
        headless = "DISPLAY" not in os.environ
    driver = create_chrome_driver(headless=headless)
    try:
        driver.get(TARGET_URL)
        time.sleep(5)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
