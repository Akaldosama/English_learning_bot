import io
import os
from aiogram import Bot, Dispatcher, executor, types
import aiohttp
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage


url_api = 'https://534b-84-54-84-135.ngrok-free.app'
API_URL_REGISTER = f"{url_api}/api/registration/"
API_URL_MATERIALS = f'{url_api}/api/materials/'

TOKEN = "7029058173:AAHQskmsTIVDTDuhOsOPNRAUsaVAc-KOt-I"

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

user_data = {}


def create_default_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Beginner"),
        types.KeyboardButton("Elementary"),
        types.KeyboardButton("Pre-Intermediate")
    )
    markup.add(
        types.KeyboardButton("Intermediate"),
        types.KeyboardButton("Ielts")
    )
    return markup

def create_action():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Listening"),
        types.KeyboardButton("Writing"),
    )
    markup.add(
        types.KeyboardButton("Reading"),
        types.KeyboardButton("Speaking")
    )
    return markup


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    telegram_id = str(message.from_user.id)
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json={"telegram_id": telegram_id}) as response:
            if response.status == 200:
                # data = await response.json()
                await message.answer(f"Assalomu alaykum! Siz avval ro'yxatdan o'tgansiz.",)
                await message.answer(f"Tugmalardan birini tanlang", reply_markup=create_action())
            else:
                await message.answer("Assalomu alaykum! To'liq ismingizni kiriting.")
                user_data[message.from_user.id] = {}


@dp.message_handler(lambda message: message.from_user.id in user_data and 'fullname' not in user_data[message.from_user.id])
async def get_fullname(message: types.Message):
    user_data[message.from_user.id]['fullname'] = message.text
    await message.answer("Telefon raqamingizni kiriting (misol: +998901234567).")


@dp.message_handler(lambda message: message.from_user.id in user_data and 'phone' not in user_data[message.from_user.id])
async def get_phone(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['phone'] = message.text

    await message.answer("Ingliz tili levelingizni tanlang.", reply_markup=create_default_keyboard())


@dp.message_handler(lambda message: message.from_user.id in user_data and 'level' not in user_data[message.from_user.id])
async def get_level(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['level'] = message.text

    payload = {
        "telegram_id": str(user_id),
        "fullname": user_data[user_id]['fullname'],
        "phone": user_data[user_id]['phone'],
        "level": user_data[user_id]['level']
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json=payload) as response:
            if response.status == 200:
                await message.answer("Ro'yxatdan muvaffaqiyatli o'tdingiz!")
                await message.answer('Yonalish tanlang', reply_markup=create_action())
            else:
                error_message = (await response.json()).get('error', 'Xato yuz berdi.')
                await message.answer(f"Xatolik: {error_message}")

    user_data.pop(user_id)

@dp.message_handler(lambda message: message.text in ["Listening", "Reading", "Writing", "Speaking"])
async def get_material(message: types.Message):
    telegram_id = str(message.from_user.id)
    skill = message.text.lower()

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_MATERIALS}?telegram_id={telegram_id}&skill={skill}") as response:
            if response.status == 200:
                data = await response.json()
                file_url = data.get("file_url", None)

                if file_url:
                    async with session.get(file_url) as file_response:
                        if file_response.status == 200:
                            file_data = await file_response.read()

                            file_name = os.path.basename(file_url)

                            await message.answer_document(types.InputFile(io.BytesIO(file_data), filename=file_name))
                        else:
                            await message.answer(f"Error: Could not download {skill} material.")
                else:
                    await message.answer(f"No {skill} material available at the moment.")
            else:
                error_data = await response.json()
                await message.answer(f"Error: {error_data.get('error', 'Could not fetch material.')}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
