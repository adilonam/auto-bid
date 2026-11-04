from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    proxy = os.environ.get("PROXY", "").strip()
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
