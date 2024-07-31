from telebot import TeleBot, types as tt

import lib.handlers as handlers
from lib.env import cfg
from lib.db import DataBase

bot = TeleBot(cfg['BOT_TOKEN'])
db  = DataBase('data.db')

handlers.create_handlers(bot, db)

bot.infinity_polling()
