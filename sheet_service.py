import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1aDCZ02znbKP-WD-OPj_-Q-mYeWChtoRWxGQUiPlSLyw"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

SETTING_CACHE = None
MASTER_CACHE = None
TRANSACTION_CACHE = None
USER_ROLE_CACHE = None
STOCK_CACHE = None

def refresh_cache():

    global SETTING_CACHE
    global MASTER_CACHE
    global TRANSACTION_CACHE
    global USER_ROLE_CACHE
    global STOCK_CACHE

    SETTING_CACHE = None
    MASTER_CACHE = None
    TRANSACTION_CACHE = None
    USER_ROLE_CACHE = None
    STOCK_CACHE = None

    print(
        "CACHE REFRESHED"
    )

def get_setting_full():

    global SETTING_CACHE

    if SETTING_CACHE:

        return SETTING_CACHE

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "Setting"
    )

    SETTING_CACHE = (
        sheet.get_all_values()
    )

    return SETTING_CACHE

def get_user_role_data():

    global USER_ROLE_CACHE

    if USER_ROLE_CACHE:
        return USER_ROLE_CACHE

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "USER_ROLE"
    )

    USER_ROLE_CACHE = (
        sheet.get_all_values()
    )

    return USER_ROLE_CACHE

def add_user_role(
    telegram_id,
    username,
    role
):

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "USER_ROLE"
    )

    data = sheet.get_all_values()

    no = len(data)

    sheet.append_row([
        no,
        telegram_id,
        username,
        role
    ])

    global USER_ROLE_CACHE

    USER_ROLE_CACHE = None

def get_stock_data():

    global STOCK_CACHE

    if STOCK_CACHE:

        return STOCK_CACHE

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "STOCK"
    )

    STOCK_CACHE = (
        sheet.get_all_values()
    )

    return STOCK_CACHE

def get_setting_data():

    global SETTING_CACHE

    if SETTING_CACHE:

        return SETTING_CACHE

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "Setting"
    )

    SETTING_CACHE = (
        sheet.get_all_values()
    )

    return SETTING_CACHE

def get_master_data():

    global MASTER_CACHE

    if MASTER_CACHE:

        return MASTER_CACHE

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "MASTER"
    )

    MASTER_CACHE = (
        sheet.get_all_values()
    )

    return MASTER_CACHE

def get_transaction_data():

    global TRANSACTION_CACHE

    if TRANSACTION_CACHE:

        return TRANSACTION_CACHE

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet = spreadsheet.worksheet(
        "TRANSACTION"
    )

    TRANSACTION_CACHE = (
        sheet.get_all_values()
    )

    return TRANSACTION_CACHE


if __name__ == "__main__":

    master = get_master_data()

    print(
        "MASTER :",
        len(master)
    )