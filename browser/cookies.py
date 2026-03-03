import json
from pathlib import Path

from selenium import webdriver


def load_cookies(driver: webdriver.Chrome, path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
        for c in data:
            if isinstance(c.get("expiry"), float):
                c["expiry"] = int(c["expiry"])
            try:
                driver.add_cookie(c)
            except Exception:
                pass
        return True
    except Exception:
        return False


def save_cookies(driver: webdriver.Chrome, path: Path) -> None:
    path.write_text(json.dumps(driver.get_cookies(), indent=2))
