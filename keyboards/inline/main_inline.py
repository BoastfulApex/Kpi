from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from backend.models import *
from utils.db_api.database import *


async def go_web_app():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Kirish",
                web_app=WebAppInfo(url="https://0cdaa0b06b31.ngrok-free.app/web_app/"))]
        ]
    )
    return keyboard