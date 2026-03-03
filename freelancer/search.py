from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from freelancer.selectors import PROJECT_LINKS_BASE_XPATH, PROJECT_LINKS_MAX


def get_project_links(driver: webdriver.Chrome, timeout: int = 10) -> list[str]:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, f"{PROJECT_LINKS_BASE_XPATH}/a[1]"))
    )
    links: list[str] = []
    for i in range(1, PROJECT_LINKS_MAX + 1):
        elements = driver.find_elements(By.XPATH, f"{PROJECT_LINKS_BASE_XPATH}/a[{i}]")
        if not elements:
            break
        href = elements[0].get_attribute("href")
        if href:
            links.append(href)
    return links
