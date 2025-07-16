from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
from data import config
from aiogram.filters import Command, StateFilter, CommandObject, CommandStart
from aiogram import F, Router


router = Router()


dp.include_router(router)


channel_id = config.CHANNEL_ID


@router.message(CommandStart(), StateFilter(None))
async def handler(message: Message, command: CommandStart):
    check = await is_user_employee(message.from_user.id)
    if check:
        keyboard = await go_web_app()
        await message.answer("Tugmani bosing", reply_markup=keyboard)
    else:
        await message.answer(
            "⚠️ Siz xodim emassiz!\n\n"
            "Botdan foydalanish uchun xodim bo‘lishingiz kerak.\n"
        )

        # 2. Inline tugma bilan administratorga murojaat qilishni taklif qilamiz
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📨 Administratorga xabar yuborish", callback_data="notify_admin")]
        ])
        await message.answer("Administratorga xabar yubormoqchimisiz?", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "notify_admin")
async def notify_admin_callback(callback_query: CallbackQuery):
    user = callback_query.from_user

    # Admin telegram ID sini bu yerga yozing
    adminsts = await get_all_admin_ids()

    for admin_id in adminsts:
        await callback_query.bot.send_message(
            chat_id=admin_id,
            text=f"🚨 Yangi foydalanuvchi botga kirishga harakat qildi:\n\n"
                f"👤 Ismi: {user.full_name}\n"
                f"🆔 Telegram ID: {user.id}\n"
                f"📩 U administratorga murojaat yuborishni tanladi."
        )

    # Foydalanuvchiga tasdiq xabari
    await callback_query.message.answer("✅ Administratorga xabaringiz yuborildi.")
    await callback_query.answer()  # loading belgisi ketadi
