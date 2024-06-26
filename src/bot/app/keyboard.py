from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, LoginUrl

start = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Registration',
                                                                    login_url=LoginUrl(
                                                                        url='https://dc9b-57-129-24-117.ngrok-free.app/auth',
                                                                        bot_username='innolan_bot',
                                                                        request_write_access=True))]])

room = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Events', callback_data='Events')],
                                             [InlineKeyboardButton(text='Routine', callback_data='Routine')]
                                             ])
