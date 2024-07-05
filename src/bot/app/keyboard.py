from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LoginUrl,
)
from src.config import bot_username

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Registration",
                login_url=LoginUrl(
                    url="https://innolan.ru/api/auth/signin",
                    bot_username=bot_username,
                    request_write_access=True,
                ),
            )
        ]
    ]
)

room = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Events", callback_data="Events")],
        [InlineKeyboardButton(text="Routine", callback_data="Routine")],
    ]
)
