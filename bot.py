import logging
import os
import random
from random import shuffle

import telebot

import config
import utils
from dao import MusicDao

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['game'])
def game(message):
    logging.info("User {} started the game".format(message.chat.id))

    db_worker = MusicDao(config.database_name)

    answer_options = random.sample(range(db_worker.count_rows()), 4)

    # Получаем строки из БД
    rows = [db_worker.find_by_id(option + 1) for option in answer_options]
    shuffle(rows)

    names = [row[2] for row in rows]
    hidden = names[0]

    logging.info("Hidden song: {}, answer options: {}".format(names[0], names))

    markup = generate_markup(names)

    # Отправляем аудиофайл с вариантами ответа
    bot.send_voice(message.chat.id, rows[0][1], reply_markup=markup, duration=20)

    utils.set_user_game(message.chat.id, hidden)

    db_worker.close()


@bot.message_handler(commands=["load"])
def load_music(message):
    for file in os.listdir('music/'):
        with open('music/' + file, 'rb') as f:
            msg = bot.send_voice(message.chat.id, f, None)
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)

            db_worker = MusicDao(config.database_name)
            db_worker.add(msg.voice.file_id, file)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    logging.info("User {}, answer: ".format(message.chat.id, message.text))

    answer = utils.get_answer_for_user(message.chat.id)

    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру: /game')
    else:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()

        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)

        logging.info("User {} finished".format(message.chat.id))
        utils.finish_user_game(message.chat.id)


def generate_markup(list_items):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    shuffle(list_items)

    for item in list_items:
        markup.add(item)

    return markup


if __name__ == '__main__':
    random.seed()
    bot.infinity_polling()
