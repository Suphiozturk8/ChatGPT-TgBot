
from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config:
    API_ID = int(getenv("API_ID"))
    API_HASH = str(getenv("API_HASH"))
    BOT_TOKEN = str(getenv("BOT_TOKEN"))
    API_BASE_URL = str(getenv("API_BASE_URL"))
