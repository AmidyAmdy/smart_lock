import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from face_recog.remember_face import remember_face
import re
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import shutil

class AddFaceState(StatesGroup):
    Name = State()
    Face = State()

token = '7593026254:AAFnFqgOyn-zohMsDH_SOHwtWsz_uiXZz3M'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

choice_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Добавить человека", callback_data="face")
)


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать"),
        types.BotCommand(command="/add_face", description="Добавить новое лицо"),
    ]
    await bot.set_my_commands(commands)


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def main_menu(message: types.Message):
    await message.answer("Пока всё чисто. Если хочешь добавить друга, то жми кнопку.", reply_markup=choice_keyboard)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        'Привет! Я сторожевой бот. Если кто-то захочет открыть твою коробочку, я дам тебе об этом знать.\n\nА ещё ты можешь приводить друзей, чтобы тоже дать им доступ.', reply_markup=choice_keyboard)


@dp.message_handler(commands=['add_face'])
async def handle_add_face_command(message: types.Message):
    await message.answer('Как тебя зовут?')
    await AddFaceState.Name.set()


@dp.callback_query_handler(lambda c: c.data == 'face')
async def handle_add_face_callback(callback_query: CallbackQuery):
    await callback_query.message.answer('Как тебя зовут?')
    await AddFaceState.Name.set()
    await callback_query.answer()


@dp.message_handler(state=AddFaceState.Name)
async def taking_name(message: types.Message, state: FSMContext):
    if message.text.startswith('/'):
        await state.finish()
        await message.answer("Сообщение не должно быть командой. Попробуй еще раз.", reply_markup=choice_keyboard)
        return
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer("Спасибо! Теперь пришли 3 фото по одному. Было бы здорово, если бы они были с разных ракурсов. Лицо должно быть хорошо видно.")
    await AddFaceState.Face.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=AddFaceState.Face)
async def taking_face(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    raw_name = state_data.get('Name', 'unknown')
    safe_name = re.sub(r'[^\w\-_.]', '_', raw_name)

    photo_dir = os.path.join("photos", safe_name)
    os.makedirs(photo_dir, exist_ok=True)

    photos = state_data.get('photos', [])

    if len(photos) >= 3:
        await message.answer("Ты уже отправил 3 фото. Подожди...")
        return

    photo = message.photo[-1]
    file_id = photo.file_id
    photos.append(file_id)

    await state.update_data(photos=photos)

    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = f"{message.message_id}.jpg"
    full_path = os.path.join(photo_dir, filename)
    await bot.download_file(file_path, full_path)

    if len(photos) == 3:
        await message.answer("Спасибо! Фото получены.")
        remember_face(safe_name)

        try:
            shutil.rmtree(photo_dir)
        except Exception as e:
            print(f"Не удалось удалить папку {photo_dir}: {e}")
        
        await state.finish()
        await main_menu(message)


@dp.message_handler(state=AddFaceState.Face)
async def not_photo(message: types.Message):
    await message.answer("Пожалуйста, пришли фото, а не текст или другой тип сообщения.")

async def send_alert(chat_id: int):
    await bot.send_message(chat_id, "Незнакомец замечен на камере!")

async def send_welcome(chat_id: int):
    await bot.send_message(chat_id, "Добро пожаловать!")

async def on_startup(dp):
    await set_commands(bot)


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
