import os
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.chrome.service import Service


CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__name__), 'driver', 'chromedriver'))
CHROME_BIN = None


def driver_init(CHROME_PATH, CHROME_BIN=None):
    service = Service(executable_path=CHROME_PATH)
    options = webdriver.ChromeOptions()
    if CHROME_BIN:
        options.binary_location = CHROME_BIN
    options.add_argument('--window-size=1200,800')
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--incognito')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


@contextmanager
def driver_context(chrome_path=CHROME_PATH, chrome_bin=CHROME_BIN):
    driver = driver_init(chrome_path, chrome_bin)
    yield driver
    driver.quit()
