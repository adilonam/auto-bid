from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
