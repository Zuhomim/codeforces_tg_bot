from django.core.management import BaseCommand
import telebot
from telebot import types

import config.settings
from tasks.services import get_distinct_subject_elements, get_contest_by_task_difficulty

# Создание бота и state
bot = telebot.TeleBot(config.settings.TELEGRAM_TOKEN)
chat_state = {}
subjects = None
subjects_set = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Приветствие при старте"""

    global subjects, subjects_set
    subjects = get_distinct_subject_elements()
    subjects_set = set(subjects)

    bot.reply_to(message,
                 f"Привет, {message.from_user.full_name}!"
                 f"Я помогу тебе подобрать список задач по любой теме и сложности")

    bot.send_message(
        message.chat.id,
        "\n".join(subjects)
    )

    global chat_state
    chat_state[message.chat.id] = {"status": "STARTED", "subject": None, "from": None, "to": None}


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Основной код бота с изменением state и кнопками для выбора ответов"""

    if chat_state[message.chat.id]["status"] == "STARTED":
        if message.text in subjects_set:
            chat_state[message.chat.id]["status"] = "SUBJECT_CHOSEN"
            chat_state[message.chat.id]["subject"] = message.text

            markup = types.ReplyKeyboardMarkup()
            itembtn_1 = types.KeyboardButton('0 - 1000')
            itembtn_2 = types.KeyboardButton('1001 - 2000')
            itembtn_3 = types.KeyboardButton('2001 - 3000')
            itembtn_4 = types.KeyboardButton('3001 - 4000')
            markup.row(itembtn_1, itembtn_2)
            markup.row(itembtn_3, itembtn_4)

            bot.send_message(message.chat.id, "Выберите диапазон сложности задач:", reply_markup=markup)

        else:
            bot.send_message(
                message.chat.id,
                "Пожалуйста, введите значение из списка выше"
            )

    elif chat_state[message.chat.id]["status"] == "SUBJECT_CHOSEN":
        chat_state[message.chat.id]["status"] = "DIFFICULTY_CHOSEN"
        chat_state[message.chat.id]["from"] = int(message.text.split()[0])
        chat_state[message.chat.id]["to"] = int(message.text.split()[2])
        bot.send_message(
            message.chat.id,
            f"Выбран диапазон {chat_state[message.chat.id]['from']} - {chat_state[message.chat.id]['to']}"
        )
        contest = get_contest_by_task_difficulty(
            chat_state[message.chat.id]['subject'],
            chat_state[message.chat.id]['from'],
            chat_state[message.chat.id]['to'],
        )

        markup = types.ReplyKeyboardMarkup()
        for task in contest.tasks.all():
            itembtn = types.KeyboardButton(" ".join(task.name_with_index.split()[:-1]) + " " + task.id)
            markup.row(itembtn)
        bot.send_message(message.chat.id, "Выберите задачу:", reply_markup=markup)

    elif chat_state[message.chat.id]["status"] == "DIFFICULTY_CHOSEN":
        chat_state[message.chat.id]["status"] = "TASK_CHOSEN"
        contest_id = message.text.split()[-1].split("_")[0]
        task_index = message.text.split()[-1].split("_")[1]
        bot.send_message(
            message.chat.id,
            f"https://codeforces.com/problemset/problem/{contest_id}/{task_index}"
        )


class Command(BaseCommand):
    help = "Run the bot"

    def handle(self, *args, **options):
        bot.polling()
