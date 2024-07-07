import json
import re
import time
import logging
import datetime
import requests
from walletapi.constants import *
from walletapi.driver_tools import driver_init, CHROME_PATH, CHROME_BIN
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger("WalletAPI")


class Wallet:
    def __init__(self, username, password, driver=None):
        self.username = username
        self.password = password
        if not driver:
            self.driver = driver_init(CHROME_PATH=CHROME_PATH, CHROME_BIN=CHROME_BIN)
        else:
            self.driver = driver

    def login(self):
        try:
            logger.info("--- Starting to login ---")
            self.driver.get(WALLET_LOGIN_URL)

            # Wait for and find the email input field
            email_field = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]')))
            password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

            # Enter email and password
            email_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Click the login button
            login_button.click()

            # Wait for the user to be visible
            WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"].ui.blue.mini.circular.compact.button'))
            )
            logger.info("--- Login completed ---")
        except Exception as e:
            logger.error(f"Error during login: {e}")
