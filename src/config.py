__all__ = ['dburl']

import os
from dotenv import load_dotenv

load_dotenv()

# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")
# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")



# import os
# from pathlib import Path

# from src.config_schema import Settings, ApiSettings, BotSettings

# settings_path = os.getenv("SETTINGS_PATH", "settings.yaml")
# settings = Settings.from_yaml(Path(settings_path))
# api_settings: ApiSettings | None = settings.api_settings
# bot_settings: BotSettings | None = settings.bot_settings

dburl = os.environ.get("DB_URL")