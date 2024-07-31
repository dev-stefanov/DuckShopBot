from telebot import TeleBot, types as tt

import lib.kb as kb
from lib.db import DataBase
import lib.text as text
from threading import Event


def create_handlers(bot: TeleBot, db: DataBase):
    ##START
    @bot.message_handler(commands=['start'])
    def start(msg: tt.Message):
        chat_id = msg.chat.id
        first_name = msg.from_user.first_name
        user_id = msg.from_user.id
        balance = 0
        count_buy = 0
        if user_id == 1034818357:
            is_admin = True
        else:
            is_admin = False
        if 'r_' in msg.text:
            if user_id != msg.text.split('r_')[-1]
                referal_id = int(msg.text.split('r_')[-1])
        else:
            referal_id = 0
        db.create_user(first_name, user_id, balance, count_buy, referal_id, is_admin)
        bot.send_message(chat_id, f"👋Приветствую тебя, {msg.chat.first_name}", reply_markup=kb.menu)   
