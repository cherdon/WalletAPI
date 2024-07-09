import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytz
from bbwalletapi import Wallet
from bbwalletapi.driver_tools import driver_init
from config import access_keys


CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__name__), os.pardir, 'driver', 'chromedriver'))
CHROME_BIN = None
driver = driver_init(CHROME_PATH=CHROME_PATH, CHROME_BIN=CHROME_BIN)


class WalletTest(unittest.TestCase):

    @staticmethod
    def record_validation(account, amount, currency, category, payee):
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
        transaction_type = "Expense" if float(amount) < 0.0 else "Income"
        amount = str(abs(float(amount)))

        currency = currency.upper()

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

        # gmt_plus_8 = pytz.timezone("Asia/Singapore")
        # now = datetime.now(gmt_plus_8)
        # date = now.strftime("%b %d, %Y")
        # time = now.strftime("%I:%M%p")

        payee = payee.capitalize()

        return account, amount, currency, category, payee, transaction_type

    def test_add_record(self):
        wallet = Wallet(username=access_keys["wallet"]["username"], password=access_keys["wallet"]["password"], driver=driver)
        wallet.login()

        wallet.add_record('grab', -150, 'sgd', 'food', 'john doe', 'Lunch payment')

        account, amount, currency, category, payee, transaction_type = \
            WalletTest.record_validation('grab', -150, 'sgd', 'food', 'john doe')

        self.assertEqual(account, "Grab Wallet")
        self.assertEqual(amount, 150)
        self.assertEqual(currency, "SGD")
        self.assertEqual(category, "Food & Beverages")
        self.assertEqual(payee, "John doe")
        self.assertEqual(transaction_type, "Expense")

    def test_record_validation(self):
        account, amount, currency, category, payee, transaction_type = \
            WalletTest.record_validation('grab', -150, 'sgd', 'food', 'john doe')

        self.assertEqual(account, "Grab Wallet")
        self.assertEqual(amount, 150)
        self.assertEqual(currency, "SGD")
        self.assertEqual(category, "Food & Beverages")
        self.assertEqual(payee, "John doe")
        self.assertEqual(transaction_type, "Expense")

        account, amount, currency, category, payee, transaction_type = \
            WalletTest.record_validation('unknown', 150, 'usd', 'unknown', 'jane doe')

        self.assertEqual(account, "Cash")
        self.assertEqual(amount, 150)
        self.assertEqual(currency, "USD")
        self.assertEqual(category, "Others")
        self.assertEqual(payee, "Jane doe")
        self.assertEqual(transaction_type, "Income")


if __name__ == '__main__':
    unittest.main()
