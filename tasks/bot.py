import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage

import config.settings

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.settings.TELEGRAM_TOKEN)
# Диспетчер
dp = Dispatcher()


# # Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")


router = Router()


@dp.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        f"Привет! {msg.from_user.full_name} Я помогу тебе подобрать список задач по любой теме и сложности")

    kb = [
        [
            types.KeyboardButton(text="Начать поиск задач"),
            types.KeyboardButton(text="Выход")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    message = await msg.answer("Начнем поиск задач?", reply_markup=keyboard)


def input_message(message: types.Message):
    if message == "Выход":
        bot.send_message(message.chat_id, "Ждем Вас снова!")


@dp.message(Command("difficulty"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)
