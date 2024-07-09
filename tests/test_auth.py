import os
import unittest
from selenium.common.exceptions import TimeoutException
from walletapi import Wallet
from walletapi.driver_tools import driver_init
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config import access_keys


CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__name__), os.pardir, 'driver', 'chromedriver'))
CHROME_BIN = None
driver = driver_init(CHROME_PATH=CHROME_PATH, CHROME_BIN=CHROME_BIN)


class TestWalletLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the Wallet class with test credentials and ChromeDriver path
        cls.wallet = Wallet(username=access_keys["wallet"]["username"], password=access_keys["wallet"]["password"], driver=driver)

    def test_login(self):
        try:
            # Call the login method
            self.wallet.login()

            # Check for successful login by finding an element on the dashboard page
            dashboard_element = WebDriverWait(self.wallet.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"].ui.blue.mini.circular.compact.button'))
            )
            # If the element is found, login is successful
            self.assertIsNotNone(dashboard_element, "Login failed, user profile element not found")
        except TimeoutException:
            self.fail("Login failed due to timeout, user profile element not found")
        except Exception as e:
            self.fail(f"Login test failed with exception: {e}")

    @classmethod
    def tearDownClass(cls):
        # Close the browser window after tests
        cls.wallet.driver.quit()


if __name__ == '__main__':
    unittest.main()
