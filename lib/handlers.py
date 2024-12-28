from telebot import TeleBot, types as tt

import lib.kb as kb
from lib.db import DataBase
import lib.text as text
from threading import Event
from lib.env import cfg
import lib.payment as payment

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
        bot.send_message(user_id, f"*👋 Приветствую в {text.shop_name}. \n🛒 Приятных покупок.*", reply_markup=kb.menu, parse_mode="Markdown", protect_content=True)   
    
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
        if message == "🛒 Каталог товаров 🛒":
            res = db.get_categories()
            bot.send_message(user_id, "*📕 Категории в магазине: *", reply_markup=kb.categories(res), parse_mode="Markdown")
        elif message == '👤 Профиль':
            balance = db.get_user(user_id).balance
            count_buy = db.get_user(user_id).count_buy
            bot.send_message(user_id, f"🏦 *Ваш баланс*: {balance} \n🙋🏻‍♂️ *ID*: `{user_id}` \n🛍 *Количество покупок*: {count_buy}", reply_markup=kb.profile_kb, parse_mode='Markdown')
        elif message == 'ℹ Информация':
            bot.send_message(user_id, '❗ Выберите действие', reply_markup=kb.info_kb)
        else:
            bot.send_message(user_id, 'К сожалению я не могу распознать вашу команду. \nВоспользуйтесь кнопками в меню или отправьте /start')
            
    ## CALLBACK
    @bot.callback_query_handler(lambda x: True)
    def query_handler(q: tt.CallbackQuery):
        data = q.data
        user_id = q.from_user.id
        bot.delete_message(user_id, q.message.id)

        cmd, *data = data.split(";")

        ## PROFILE
        if cmd == 'deposite':
            msg = bot.send_message(user_id, 'Введите сумму пополнения')
            sum = wait_for_message(msg)
            url = payment.deposite_url(user_id, sum)
            bot.send_message(user_id, "Выбран способ оплаты через Yoomoney", reply_markup=kb.url(url))
            

        ## ADMIN
        elif cmd == 'add_category':
            msg = bot.send_message(user_id, 'Введите название категории:')
            name = wait_for_message(msg)
            msg = bot.send_message(user_id, 'Введите описание категории:')
            description = wait_for_message(msg)
            if description == 'None':
                description = ''
            bot.send_message(user_id, db.add_category(name, description))

        elif cmd == 'add_good':
            msg = bot.send_message(user_id, 'Введите категорию товара:')
            category = wait_for_message(msg)
            if category == 'exit':
                bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)
            else:
                msg = bot.send_message(user_id, 'Введите название товара:')
            name = wait_for_message(msg)
            if name == 'exit':
                bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)
            else:
                msg = bot.send_message(user_id, 'Введите стоимость товара:')
            cost = wait_for_message(msg)
            if cost == 'exit':
                bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)
            else:
                msg = bot.send_message(user_id, 'Введите количество товара:')
            count = wait_for_message(msg)
            if count == 'exit':
                bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)
            else:
                msg = bot.send_message(user_id, 'Введите описание товара:')
            description = wait_for_message(msg)
            if description == 'exit':
                bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)
            else:
                bot.send_message(user_id, db.add_good(category, name, cost, count, description))

        elif cmd == 'del_category':
            res = db.get_categories()
            bot.send_message(user_id, 'Выберите категорию:', reply_markup=kb.del_category(res))

        elif cmd == 'delete_category':
            name = db.get_category(*data).name
            bot.send_message(user_id, db.del_category(*data, name))

        elif cmd == 'del_good':
            res = db.get_all_goods()
            bot.send_message(user_id, 'Выберите товар:', reply_markup=kb.del_good(res))

        elif cmd == 'delete_good':
            name = db.get_good(*data).name
            bot.send_message(user_id, db.del_good(*data, name))

        elif cmd == 'back_to_admin':
            bot.send_message(user_id, "Admin Panel", reply_markup=kb.admin_kb)

        elif cmd == 'edit_category':
            res = db.get_categories()
            bot.send_message(user_id, 'Выберите категорию:', reply_markup=kb.edit_categories(res))

        elif cmd == 'edit_good':
            res = db.get_all_goods()
            bot.send_message(user_id, 'Выберите категорию:', reply_markup=kb.edit_goods(res))

        elif cmd == 'ed_categories':
            res = db.get_category(int(*data))
            bot.send_message(user_id, 'Выберите параметр для редактирования:', reply_markup=kb.edit_category(res))

        elif cmd == 'ed_goods':
            res = db.get_good(int(*data))
            bot.send_message(user_id, 'Выберите параметр для редактирования:', reply_markup=kb.edit_good(res))

        elif cmd == 'ed_category':
            category_id = data[0]
            name_param = data[1]
            msg = bot.send_message(user_id, text='Введите новое значение:')
            new_param = wait_for_message(msg)
            db.edit_category(category_id, name_param, new_param)
            bot.send_message(user_id, 'Редактирование завершено', reply_markup=kb.admin_kb)

        elif cmd == 'ed_good':
            good_id = data[0]
            name_param = data[1]
            msg = bot.send_message(user_id, text='Введите новое значение:')
            new_param = wait_for_message(msg)
            db.edit_good(good_id, name_param, new_param)
            bot.send_message(user_id, 'Редактирование завершено', reply_markup=kb.admin_kb)


        ## GOODS
        elif cmd == 'back_to_category':
            res = db.get_categories()
            bot.send_message(user_id, "Категории: ", reply_markup=kb.categories(res))

        elif cmd == 'back_to_goods':
            res = db.get_goods(*data)
            bot.send_message(user_id, *data, reply_markup=kb.goods(res))

        elif cmd == 'category':
            name = db.get_category(*data).name
            res = db.get_goods(name)
            description = db.get_category(*data).description
            bot.send_message(user_id, f'*📃 Категория: {name} \n📃 Описание: \n*{description}**', reply_markup=kb.goods(res), parse_mode='Markdown')

        elif cmd == 'good':
            res = db.get_good(*data)
            category = res.category
            if category == '✉️ Почты ✉️':
                bot.send_message(user_id, f'📃 *Товар*: {res.name} \n💰*Цена*: {res.cost} ₽ \n📃 *Описание*: {res.description} \n\nЗаходить с приватным прокси Германии \n\n❗*Товар выдается в формате:* \nПочта:Пароль:РезервнаяПочта:Пароль', reply_markup=kb.good(res.name, category, res.count), parse_mode='Markdown')
            elif category == '👛 Кошельки 👛':
                bot.send_message(user_id, f'📃 *Товар*: {res.name} \n💰*Цена*: {res.cost} ₽ \n📃 *Описание*: {res.description}', reply_markup=kb.good(res.name, category, res.count), parse_mode='Markdown')
            elif category == '🛡 VPN 🛡':
                bot.send_message(user_id, f'📃 *Товар*: {res.name} \n💰*Цена*: {res.cost} ₽ \n📃 *Описание*: {res.description}', reply_markup=kb.good(res.name, category, res.count), parse_mode='Markdown')
            elif category == '🌐 Прокси 🌐':
                bot.send_message(user_id, f'📃 *Товар*: {res.name} \n💰*Цена*: {res.cost} ₽ \n📃 *Описание*: {res.description}', reply_markup=kb.good(res.name, category, res.count), parse_mode='Markdown')
            elif category == '👥 Соц Сети 👥':
                bot.send_message(user_id, f'📃 *Товар*: {res.name} \n💰*Цена*: {res.cost} ₽ \n📃 *Описание*: *{res.description}*', reply_markup=kb.good(res.name, category, res.count), parse_mode='Markdown')
            

        elif cmd == 'choose_count':
            res = db.get_good(*data)
            msg = bot.send_message(user_id, f'Введите количество товара, которое хотите купить: \nМинимальное количество: 1 \nМаксимальное количество: {res.count}')
            count = wait_for_message(msg)
            balance = db.get_user(user_id).balance
            if count.isdigit():
                final_cost = int(count) * db.get_good(*data).cost
                if final_cost <= balance:
                    bot.send_message(user_id, 'Поздравляем с покупкой!')
                else:
                    bot.send_message(user_id, f'Это будет стоить {final_cost} ₽. \nНедостающий баланс: {final_cost - balance} ₽ \nПополните баланс', reply_markup=kb.deposite_kb)
            else:
                bot.send_message(user_id, 'Значение должно быть числом')

        elif cmd == 'count':
            res = db.get_good(data[0])
            count = int(data[1])
            final_cost = res.cost * count
            balance = db.get_user(user_id).balance
            if balance < final_cost:
                bot.send_message(user_id, f'Это будет стоить {final_cost} ₽. \nНедостающий баланс: {final_cost - balance} ₽ \nПополните баланс', reply_markup=kb.deposite_kb)
            else:
                bot.send_message(user_id, 'Поздравляем с покупкой!')
                



