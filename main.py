import pytesseract
import telebot
import magic
import os
from PIL import Image
from telebot import types
from config import *


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    bot.send_message(message.chat.id, "Welcome! I can recognize text from your photo. "
                                      "For this send your photo to me as a *File*.", parse_mode='Markdown')


@bot.message_handler(content_types=['photo'])  # if the user sent a photo as a photo - ask him to send it as a file
def warning_message(message):
    bot.send_message(message.chat.id, 'Please, send the photo as a *File*, not as a *Photo*', parse_mode='Markdown')


@bot.message_handler(content_types=['document'])
def check_mime_type_of_file(message):  # magic library was used for checking mime type of sending file
    file = bot.get_file(message.document.file_id)
    download_file = bot.download_file(file.file_path)

    src = message.document.file_id

    with open(src, 'wb') as f:
        f.write(download_file)

    check_format = magic.from_file(src, mime=True)

    if check_format == 'image/jpeg' or check_format == 'image/png':
        os.remove(src)

        with open('user_photo.jpeg', 'wb') as f:
            f.write(download_file)

        buttons(message)
    else:
        bot.send_message(message.chat.id, "This is not a photo! I'm working only with `jpeg` and `png` formats.",
                         parse_mode='Markdown')
        os.remove(src)


def text_detector(message, language):
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text='Process is started.' + '\n' + 'Please, wait for the end. ')

    img = Image.open('user_photo.jpeg')
    text = pytesseract.image_to_string(img, lang=language)

    if len(text) > 4096:  # construct used to split large text into two messages
        for x in range(0, len(text), 4096):
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text[x:x + 4096])
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text)

    os.remove('user_photo.jpeg')


def buttons(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='English', callback_data='language_english')
    button2 = types.InlineKeyboardButton(text='Russian', callback_data='language_russian')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Select language of text on photo.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'language_english':
        text_detector(call.message, 'eng')
    elif call.data == 'language_russian':
        text_detector(call.message, 'rus')


if __name__ == '__main__':
    bot.polling(True)
