from aiogram.types import ReplyKeyboardRemove, Message, WebAppData
from aiogram.fsm.context import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
from aiogram.utils.deep_linking import decode_payload, encode_payload
from data import config
from aiogram.filters import Command, StateFilter, CommandObject, CommandStart
from aiogram import F, Router
from states.admin import EmployeeForm, AddLocation
router = Router()
import json


dp.include_router(router)


channel_id = config.CHANNEL_ID

    
@router.message(CommandStart(deep_link=True), StateFilter(None))
async def handler(message: Message, command: CommandStart):
    args = command.args    
    if args:
        check = await is_user_employee(message.from_user.id)
        if check:
            keyboard = await go_web_app()
            await message.answer("Tugmani bosing", reply_markup=keyboard)
            
        else:
            encoded = encode_payload(message.from_user.id)
            link = f"https://t.me/BoastfulApex_bot?start={encoded}"
            await message.answer(f"⚠️ Siz xodim emassiz!\n\nBotdan foydalanish uchun xodim bo‘lishingiz kerak.\n\n")
    else:
        await message.answer(f'⚠️ Iltimos botdan qr kod orqali foydalaning 📲')


@router.message(StateFilter(None), F.text  == '12')
async def handler(message: Message):
    markup = await admin_menu_keyboard()
    await message.answer("Kerakli buyruqni tanlang", reply_markup=markup)


@router.message(StateFilter(None), F.text  == '13')
async def handler(message: Message):
    encoded = encode_payload(message.from_user.id)
    link = f"https://t.me/BoastfulApex_bot?start={encoded}"
    await message.answer(link)

@router.message(StateFilter(None), F.text  == '11')
async def handler(message: Message):
    markup = await go_web_app()
    await message.answer("Kerakli buyruqni tanlang", reply_markup=markup)
    
    # markup = await admin_menu_keyboard()
    # await message.answer("Kerakli buyruqni tanlang", reply_markup=markup)


@router.message(F.text == "🔙 Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    markup = await admin_menu_keyboard()
    await message.answer("Kerakli buyruqni tanlang:", reply_markup=markup)


# Xodim qo‘shish boshlanishi
@router.message(F.text == "🧑‍💼 Xodim qo'shish")
async def start_add_employee(message: Message, state: FSMContext):
    markup = cancel  # bu cancel tugmasi bo'lgan keyboard
    await message.answer("Xodimning Telegram user_id sini kiriting:", reply_markup=markup)
    await state.set_state(EmployeeForm.get_id)


# ID qabul qilish
@router.message(F.text, EmployeeForm.get_id)
async def process_user_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    markup = cancel
    await message.answer("Xodimning to‘liq ismini kiriting:", reply_markup=markup)
    await state.set_state(EmployeeForm.get_name)


# To‘liq ism qabul qilish va saqlash
@router.message(F.text, EmployeeForm.get_name)
async def process_full_name(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    full_name = message.text

    # Bazaga saqlash funksiyasi
    await add_employee(user_id=user_id, full_name=full_name)

    await state.clear()
    markup = await admin_menu_keyboard()
    await message.answer("✅ Xodim qo‘shildi!\n\nKerakli buyruqni tanlang:", reply_markup=markup)
    

@router.message(StateFilter(None), F.text == "📍 Manzillar")
async def show_latest_location(message: Message):
    location = await get_latest_location()
    
    if location:
        markup = address_bottom_keyboard()
        name = location.name or "Noma'lum manzil"
        await message.answer(f"📍 So‘nggi manzil: {name}", reply_markup=markup)

        if location.latitude and location.longitude:
            await message.answer_location(latitude=location.latitude, longitude=location.longitude)
        else:
            await message.answer("⚠️ Ushbu manzil uchun koordinatalar mavjud emas.")
    else:
        markup = empty_address_keyboard()
        await message.answer("❌ Hozircha manzillar mavjud emas.", reply_markup=markup)
        

@router.message(StateFilter(None), F.text == "➕ Manzil qo‘shish")
async def ask_for_location(message: Message, state: FSMContext):
    await message.answer("📍 Iltimos, yangi manzil lokatsiyasini yuboring (Telegram joylashuv orqali).")
    await state.set_state(AddLocation.waiting_for_location)


@router.message(StateFilter(None), F.text == "✏️ Manzilni yangilash")
async def ask_for_location(message: Message, state: FSMContext):
    await message.answer("📍 Iltimos, yangi manzil lokatsiyasini yuboring (Telegram joylashuv orqali).")
    await state.set_state(AddLocation.waiting_for_location)


@router.message(AddLocation.waiting_for_location, F.location)
async def save_user_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    name = await get_location_name(lat, lon)

    await save_location(name=name, lat=lat, lon=lon)

    await message.answer(f"✅ Manzil qo‘shildi:\n📍 {name}")
    markup = await admin_menu_keyboard()
    await message.answer("Kerakli bo‘limni tanlang:", reply_markup=markup)

    await state.clear()
    
    
@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    data = message.web_app_data.data
    parsed = json.loads(data)

    await message.answer(f"✅ WebAppdan keldi:\nID: {parsed['user_id']}\nIsm: {parsed['first_name']}")
