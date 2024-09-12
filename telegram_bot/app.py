import logging
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests


API_TOKEN = '7292204541:AAGOuzQB8UAQHOE1IegXy9pYUDHg_WSe-7M'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


FASTAPI_URL = 'http://127.0.0.1:8000/auth/register/'


@dp.message_handler(commands=['auth'])
async def welcome(message: types.Message):
    users = requests.get('http://127.0.0.1:8000/auth/').json()["items"]
    for user in users:
        await message.reply(f"""
        Username: {user['username']}\n
        email:{user['email']}\n
        password:{user['password']}\n
        """)


class RegisterForm(StatesGroup):
    username = State()
    email = State()
    password = State()


@dp.message_handler(commands='register', state='*')
async def register(message: types.Message):
    await message.answer("Username :")
    await RegisterForm.username.set()



@dp.message_handler(state=RegisterForm.username)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Username :")
    await RegisterForm.next()



@dp.message_handler(state=RegisterForm.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Email :")
    await RegisterForm.next()



@dp.message_handler(state=RegisterForm.password)
async def process_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)

    user_data = await state.get_data()
    user_name = user_data['username']
    user_email = user_data['email']
    user_password = user_data['password']

    async with aiohttp.ClientSession() as session:
        payload = {
            'username': user_name,
            'email': user_email,
            'password': user_password
        }
        async with session.post(FASTAPI_URL, json=payload) as response:
            if response.status == 200:
                await message.answer(
                    f"Success!\nUsername : {user_name}\nEmail : {user_email}")
            else:
                await message.answer(f"Incorrect username or email | and password. {response.status}")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)