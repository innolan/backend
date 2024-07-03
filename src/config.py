__all__ = ["dburl"]

import os
from dotenv import load_dotenv

load_dotenv()

dburl = os.environ.get("DB_URL")