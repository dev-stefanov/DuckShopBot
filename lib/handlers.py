from telebot import TeleBot, types as tt

import lib.kb as kb
from lib.db import DataBase
import lib.text as text
from threading import Event
from lib.env import cfg

def create_handlers(bot: TeleBot, db: DataBase):

    ## WAIT FOR MESSAGE
    def wait_for_message(msg: tt.Message):
        e = Event()
        d = {}
        def on_answer(msg: tt.Message):
            d['answer'] = msg.text
            e.set()
        bot.register_next_step_handler(msg, on_answer)
        e.wait()
        return d.get('answer', None)
    def auto_add_goods():
        for i in range(5):
            db.add_good('Почты', 'Mail' + str(i), i * 10, i * 2)
        for i in range(5):
            db.add_good('Прокси', 'Proxy' + str(i), i * 10, i * 2)
    def auto_add_category():
        db.add_category('Почты')
        db.add_category('Прокси')
    auto_add_category()
    auto_add_goods()

    ## START
    @bot.message_handler(commands=['start'])
    def start(msg: tt.Message):
        user_id = msg.from_user.id
        balance = 0
        count_buy = 0
        if 'r_' in msg.text:
            if user_id != msg.text.split('r_')[-1]:
                referal_id = int(msg.text.split('r_')[-1])
        else:
            referal_id = 0
        if user_id == int(cfg['admin_id']):
            is_admin = True
        else:
            is_admin = False
        db.create_user(user_id, balance, count_buy, referal_id, is_admin)
        bot.send_message(user_id, f"👋Приветствую в {text.shop_name}. \n💗Наши проекты - {text.shop_projects} \n🛒Приятных покупок.", reply_markup=kb.menu)   
    
    ## IS ADMIN
    @bot.message_handler(commands=['admin'])
    def admin(msg: tt.Message):
        user_id = msg.chat.id
        user = db.get_user(user_id)
        if user.is_admin:
            bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)
        else:
            bot.send_message(user_id, "Fuck you")

    ## TEXT
    @bot.message_handler(content_types=['text'])
    def get_answer(msg: tt.Message):
        user_id = msg.from_user.id
        message = msg.text
        if message == "Каталог товаров":
            res = db.get_categories()
            bot.send_message(user_id, "Категории: ", reply_markup=kb.categories(res))
        elif message == 'Профиль':
            bot.send_message(user_id, "Профиль")
            
    ## CALLBACK
    @bot.callback_query_handler(lambda x: True)
    def query_handler(q: tt.CallbackQuery):
        data = q.data
        user_id = q.from_user.id
        bot.delete_message(user_id, q.message.id)

        cmd, *data = data.split(";")

        ## ADD CATEGORY
        if cmd == 'add_category':
            msg = bot.send_message(user_id, 'Введите название категории')
            name = wait_for_message(msg)
            db.add_category(name)

        elif cmd == 'add_good':
            msg = bot.send_message(user_id, 'Введите категорию товара:')
            category = wait_for_message(msg)
            msg = bot.send_message(user_id, 'Введите название товара:')
            name = wait_for_message(msg)
            msg = bot.send_message(user_id, 'Введите стоимость товара:')
            cost = wait_for_message(msg)
            msg = bot.send_message(user_id, 'Введите количество товара:')
            count = wait_for_message(msg)
            db.add_good(category, name, cost, count)


