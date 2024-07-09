import pytz
import logging
import datetime
import requests
import time
from walletapi.constants import *
from walletapi.driver_tools import driver_init, CHROME_PATH, CHROME_BIN
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            email_field = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]')))
            password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

            # Enter email and password
            email_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Click the login button
            login_button.click()

            # Wait for the user to be visible
            WebDriverWait(self.driver, 180).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"].ui.blue.mini.circular.compact.button'))
            )
            logger.info("--- Login completed ---")
        except Exception as e:
            logger.error(f"Error during login: {e}")

    @staticmethod
    def record_validation(account, amount, currency, category, payee):
        # Map account to its corresponding value
        account_mapping = {
            "PAYLAH": "Paylah",
            "GRAB": "Grab Wallet",
            "CASH": "Cash",
            "CITI_PRESTIGE": "Citi Prestige",
            "CITI_CASHBACK": "Citi Cashback",
            "ENDOWUS": "Endowus",
            "ENDOWUS_CPF": "Endowus (CPF)",
            "ENDOWUS_SRS": "Endowus (SRS)",
            "CPF_OA": "CPF (Ordinary Account)",
            "GREAT_WEALTH_MULTIPLIER": "Great Wealth Multiplier",
            "CRYPTO.COM": "Crypto.com",
            "YOUTRIP": "Youtrip",
            "SYFE": "Syfe",
            "INTERACTIVE_BROKERS": "InteractiveBrokers",
            "CHOCOLATE": "Chocolate Finance"
        }
        account = account_mapping.get(account.upper(), "Cash")

        # Determine transaction type and ensure amount is non-negative
        transaction_type = "Expense" if amount < 0 else "Income"
        amount = abs(amount)

        # Uppercase the currency
        currency = currency.upper()

        # Map category
        category_mapping = {
            "food": "Food & Beverages",
            "shopping": "Shopping",
            "housing": "Housing",
            "transport": "Transportation",
            "vehicle": "Vehicle",
            "life and entertainment": "Life & Entertainment",
            "software": "Communication, PC",
            "financial expenses": "Financial Expenses",
            "investments": "Investments",
            "income": "Income",
            "others": "Others"
        }
        category = category_mapping.get(category.lower(), "Others")

        # Get current date and time in GMT+8
        # gmt_plus_8 = pytz.timezone("Asia/Singapore")
        # now = datetime.datetime.now(gmt_plus_8)
        # date = now.strftime("%b %d, %Y")
        # time = now.strftime("%I:%M%p")

        # Capitalize the first letter of payee
        payee = payee.capitalize()

        # Return the validated and formatted values
        return account, amount, currency, category, payee, transaction_type

    def add_record(self, account, amount, currency, category, payee, description):
        try:
            logger.info("--- Adding a new record ---")

            account, amount, currency, category, payee, transaction_type = \
                self.record_validation(account, amount, currency, category, payee)

            # Click on the "＋ Record" button
            record_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[type="button"].ui.blue.mini.circular.compact.button'))
            )
            record_button.click()

            # Wait for the add record modal to be visible
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ui.modal.transition.visible.active'))
            )

            # Categorize the transaction and set amount to non-negative
            transaction_type = 'Expense' if amount < 0 else 'Income'
            amount = abs(amount)

            # Use XPath to find payee input field and enter payee
            payee_field = self.driver.find_element(By.XPATH,
                                                   '//div[contains(@class, "form-detail")]//label[text()="Payee"]/following-sibling::div//input[@type="text"]')
            payee_field.send_keys(payee)
            self.driver.find_element(By.CSS_SELECTOR, 'textarea[name="note"]').send_keys(description)

            # Select transaction type
            self.select_transaction_type(transaction_type)

            # Fill in the record details
            self.select_dropdown_option('div[name="accountId"]', '//div[@role="option"]//div[@class="label" and text()="{}"]', account)
            self.driver.find_element(By.CSS_SELECTOR, 'input[name="amount"]').send_keys(amount)
            self.select_dropdown_option('div[name="currencyId"]', '//div[@role="option"]//span[@class="text" and text()="{}"]', currency)
            self.select_dropdown_option('div.ui.fluid.selection.dropdown', '//div[@class="icon-option category-option"]//div[@class="label" and text()="{}"]', category)
            # Select the first item in the category dropdown if shown
            first_category_item = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="menu transition visible"]//li[@role="option"]'))
            )
            first_category_item.click()

            # Submit the form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button.ui.circular.fluid.primary.button')
            submit_button.click()

            time.sleep(10)

            logger.info("--- Record added successfully ---")
        except Exception as e:
            logger.error(f"Error during adding record: {e}")

    def select_transaction_type(self, transaction_type):
        try:
            # Find and click on the transaction type button (Expense, Income, Transfer)
            transaction_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH,
                                            f'//div[@class="ui compact fluid inverted three item record-form-menu menu"]/a[contains(text(), "{transaction_type}")]'))
            )
            transaction_button.click()
        except Exception as e:
            logger.error(f"Error selecting transaction type: {e}")

    def select_dropdown_option(self, dropdown_css_selector, option_selector, option_text):
        dropdown = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_css_selector))
        )
        dropdown.click()
        option_selector = option_selector.format(option_text)
        option = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, option_selector)))
        option.click()
