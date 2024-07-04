__all__ = ["dburl", "bot_username", "bot_token"]

import os
from dotenv import load_dotenv

load_dotenv()

dburl = os.environ.get("DB_URL" if os.environ.get("PROD") else "DEV_DB_URL")
bot_username = os.environ.get("BOT_PROD" if os.environ.get("PROD") else "BOT_DEV")
bot_token = os.environ.get("BOT_TOKEN" if os.environ.get("PROD") else "DEV_BOT_TOKEN")
