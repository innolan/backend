from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LoginUrl,
)

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Registration",
                login_url=LoginUrl(
                    url="https://innolan.ru/api/auth/signin",
                    bot_username="innolan_staging_bot",
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
