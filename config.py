import os


access_keys = {
    # "CHROME_PATH": os.environ['CHROME_PATH'],
    # "CHROME_BIN": os.environ['CHROME_BIN'] if 'CHROME_BIN' in os.environ else None,
    "wallet": {
        "username": os.environ['SERVICE_ACCOUNT_USER'],
        "password": os.environ['SERVICE_ACCOUNT_PASSWORD']
    },
}
