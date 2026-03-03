from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from freelancer.selectors import PROJECT_VIEW_DETAILS_XPATH, PROJECT_VIEW_TITLE_XPATH


def get_project_title_and_details(
    driver: webdriver.Chrome, timeout: int = 10
) -> tuple[str, str]:
    """Get title and full details text from current project page. Details include all child text."""
    title = ""
    details = ""
    try:
        title_el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, PROJECT_VIEW_TITLE_XPATH))
        )
        title = (title_el.text or "").strip()
    except Exception:
        pass
    try:
        details_el = driver.find_element(By.XPATH, PROJECT_VIEW_DETAILS_XPATH)
        details = (details_el.text or "").strip()
    except Exception:
        pass
    return title, details
