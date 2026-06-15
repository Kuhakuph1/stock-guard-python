import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv(
    "BOT_TOKEN"
)


SPREADSHEET_ID = os.getenv(
    "SPREADSHEET_ID"
)
