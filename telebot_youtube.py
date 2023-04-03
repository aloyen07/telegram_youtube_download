### ЗАДАЧА: ###
# Сделать бота в телеграмме, который будет скачивать видео с ютуба.
# Далее, бот отправляет этот видос в чат, после чего, можно выбрать что делать с этим видосом (конвертировать во что-то, ухудшить качество)
### ТРЕБОВАНИЯ: ###
# Бот должен отправлять видео либо в .zip формате, либо тупо простым видосом
# Можно выбрать качество скачанного видео
# Видео можно во что-то конвертировать (.mp4, .flac, другие форматы видео)

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import re
from pytube import YouTube

TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)

dump_directory = os.path.join(os.getcwd(), 'mp3')
os.makedirs(dump_directory, exist_ok=True)

bug_users = []
buttons = ["Использование бота", "🦊 О создателе", "🦀 Баг-репорт", "🌚 Донатики", "💢 Отмена!"]

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add(KeyboardButton("Использование бота"))
down_btn1 = KeyboardButton("🦊 О создателе")
down_btn2 = KeyboardButton("🦀 Баг-репорт")
down_btn3 = KeyboardButton("🌚 Донатики")
default_keyboard.add(down_btn1, down_btn2, down_btn3)

bug_report_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
bug_report_keyboard.add(KeyboardButton("💢 Отмена!"))

@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет!\nЭто скачиватель видео с YouTube.\nПосмотрите кнопки ниже.", reply_markup=default_keyboard)

@bot.message_handler(regexp="🦊 О создателе")
def send_admin(message):
    bot.send_message(message.chat.id, """
Создатель: @denisorlov2
И я не знаю что тут ещё написать.
""")

@bot.message_handler(regexp="🦀 Баг-репорт")
def send_bug(message):
    bot.send_message(message.chat.id, "Извини, ещё не готово.")

@bot.message_handler(regexp="🌚 Донатики")
def send_donations(message):
    bot.send_message(message.chat.id, "Если не трудно, то закинь небольшую копеечку на киви -> ALOYEN228\nНу, пожалуйста.")
    bug_users.append(message.chat.id)

# @bot.message_handler(regexp="💢 Отмена!")
# def bug_cancel(message):
#     if message.chat.id not in bug_users:
#         bot.send_message(message.chat.id, "И отменять то нечего было.", reply_markup=default_keyboard)
#     else:
#         bot.send_message(message.chat.id, "Хорошо, отменяю баг-репорт.", reply_markup=default_keyboard)
#         try:
#             bug_users.remove(message.chat.id)
#         except:
#             pass

@bot.message_handler(regextp="Использование бота")
def usage(message):
    bot.send_message(message.chat.id, "Всё очень легко.\nПришли мне ссылку и качество, разделённые пробелами и & (например, 'https://www.youtube.com/watch?v=fKN6P6xzbPc & 360p) и жди. Бот отправит тебе то, что ты просил, если у него есть доступ к видео.")

@bot.message_handler()
def downloader(message):
    if message.text not in buttons:
        pattern = r"https:\/\/\S* \& \S*"
        if re.findall(pattern=pattern, string=message.text)!=[]:
            try:
                bot.send_message(message.chat.id, "Downloading...")
                yt = YouTube(message.text).streams.filter(resolution=message.text.split(" & ")[1]).first().download(dump_directory)
                bot.send_message(message.chat.id, "Sending...")
                video = open(yt, "rb")
                bot.send_video(message.chat.id, video)
                video.close()
            except Exception as e:
                bot.send_message(message.chat.id, "Не получилось скачать видео.\nВозможно, неверна ссылка или же видео доступно ограниченному кругу людей.\nТак же, возможно, на видео нет такого качества")
                print(e)
        else:
            bot.send_message(message.chat.id, "Не найдена ссылка в сообщении!")

    elif message.text == "Использование бота":
        bot.send_message(message.chat.id, "Всё очень легко.\nПришли мне ссылку, выбери формат видео, потом качество и жди. Бот отправит тебе то, что ты просил, если у него есть доступ к видео.")



# @bot.message_handler()
# def default_handler(message):
#     if message.text not in buttons:
#         if message.chat.id in bug_users:
#             bug_users.remove(message.chat.id)
#             file = open("./bugs.txt", "a")
#             file.write("\n" + message.text)
#             file.close()
#             bot.send_message(message.chat.id, "Баг-репорт успешно отправлен. Спасибо.", reply_markup=default_keyboard)

bot.infinity_polling()