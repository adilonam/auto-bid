import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Use system Chromium + chromedriver in container (apt chromium / chromium-driver)
_SYSTEM_CHROMEDRIVER_PATHS = (
    "/usr/bin/chromedriver",
    "/usr/lib/chromium/chromedriver",
    "/usr/lib/chromium-browser/chromedriver",
)
_SYSTEM_CHROMIUM_PATHS = ("/usr/bin/chromium", "/usr/bin/chromium-browser")


def _system_driver_and_binary():
    for driver_path in _SYSTEM_CHROMEDRIVER_PATHS:
        if not os.path.isfile(driver_path):
            continue
        for binary_path in _SYSTEM_CHROMIUM_PATHS:
            if os.path.isfile(binary_path):
                return driver_path, binary_path
    return None, None


def create_chrome_driver(*, headless: bool = False) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")

    driver_path, binary_path = _system_driver_and_binary()
    if driver_path and binary_path:
        options.binary_location = binary_path
        service = Service(driver_path)
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)
