from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='', callback_data='' )]
])

menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn1 = KeyboardButton('🛒 Каталог товаров 🛒')
btn2 = KeyboardButton('👤 Профиль')
btn3 = KeyboardButton('ℹ Информация')

menu.add(btn1).row(btn2, btn3)

def categories(res):
    kb = []
    for i in range(len(res)):
        kb.append([InlineKeyboardButton(text=res[i].name, callback_data='category;' + str(res[i].id))])
    return InlineKeyboardMarkup(kb)

def goods(res):
    kb =[]
    for i in range(len(res)):
        kb.append([InlineKeyboardButton(text=f'{res[i].name} | {res[i].cost} ₽ | {res[i].count} шт.', callback_data='good;' + str(res[i].id))])
    kb.append([InlineKeyboardButton(text='Назад ко всем категориям', callback_data='back_to_category')])
    return InlineKeyboardMarkup(kb)

def good(name, category, count):
    print(count)
    print(name, type(name))
    count= int(count)
    kb = InlineKeyboardMarkup(row_width=5)
    row_1 = []
    row_2 = []
    if count >= 10:
        for i in range(5):
            row_1.append(InlineKeyboardButton(text=i+1, callback_data='count;' + name + ';' + str(i+1)))
        for i in range(6, 11):
            row_2.append(InlineKeyboardButton(text=i, callback_data='count;' + name + ';' + str(i)))
        kb.add(row_1[0], row_1[1], row_1[2], row_1[3], row_1[4])
        kb.add(row_2[0], row_2[1], row_2[2], row_2[3], row_2[4])
    else:
        for i in range(count):
            row_1.append(InlineKeyboardButton(text=i+1, callback_data='count;' + name + ';' + str(i+1)))
        kb.add(*row_1)
            
    kb.add(InlineKeyboardButton(text='Ввести количество вручную', callback_data='choose_count;' + name))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_goods;' + category))
    kb.add(InlineKeyboardButton(text='Назад ко всем категориям', callback_data='back_to_category;' + name))
    return kb

def del_category(res):
    kb = []
    for i in res:
        kb.append([InlineKeyboardButton(text=i.name, callback_data='delete_category;' + str(i.id))])
    kb.append([InlineKeyboardButton(text='Назад в меню', callback_data='back_to_admin')])
    return InlineKeyboardMarkup(kb)

def del_good(res):
    kb =[]
    for i in range(len(res)):
        kb.append([InlineKeyboardButton(text=f'{res[i].name} | {res[i].category}', callback_data='delete_good;' + str(res[i].id))])
    kb.append([InlineKeyboardButton(text='Назад в меню', callback_data='back_to_admin')])
    return InlineKeyboardMarkup(kb)

def edit_categories(res):
    kb = []
    for i in res:
        kb.append([InlineKeyboardButton(text=i.name, callback_data='ed_categories;' + str(i.id))])
    kb.append([InlineKeyboardButton(text='Назад в меню', callback_data='back_to_admin')])
    return InlineKeyboardMarkup(kb)

def edit_goods(res):
    kb =[]
    for i in range(len(res)):
        kb.append([InlineKeyboardButton(text=f'{res[i].name} | {res[i].category}', callback_data='ed_goods;' + str(res[i].id))])
    kb.append([InlineKeyboardButton(text='Назад в меню', callback_data='back_to_admin')])
    return InlineKeyboardMarkup(kb)

def edit_category(res):
    kb = []
    kb.append([InlineKeyboardButton(text='Название', callback_data='ed_category;' + str(res.id) + ';name')])
    kb.append([InlineKeyboardButton(text='Описание', callback_data='ed_category;' + str(res.id) + ';description')])
    kb.append([InlineKeyboardButton(text='Назад в меню', callback_data='back_to_admin')])
    return InlineKeyboardMarkup(kb)

def edit_good(res):
    kb = []
    kb.append([InlineKeyboardButton(text=f'Название', callback_data='ed_good;' + str(res.id) + ';name')])
    kb.append([InlineKeyboardButton(text=f'Категория', callback_data='ed_good;' + str(res.id) + ';category')])
    kb.append([InlineKeyboardButton(text=f'Стоимость', callback_data='ed_good;' + str(res.id) + ';cost')])
    kb.append([InlineKeyboardButton(text=f'Количество', callback_data='ed_good;' + str(res.id) + ';count')])
    kb.append([InlineKeyboardButton(text=f'Описание', callback_data='ed_good;' + str(res.id) + ';description')])
    kb.append([InlineKeyboardButton(text='Назад в меню', callback_data='back_to_admin')])
    return InlineKeyboardMarkup(kb)


admin_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Добавить категорию', callback_data='add_category')],
    [InlineKeyboardButton(text='Добавить товар', callback_data='add_good')],
    [InlineKeyboardButton(text='Удалить категорию', callback_data='del_category')],
    [InlineKeyboardButton(text='Удалить товар', callback_data='del_good')],
    [InlineKeyboardButton(text='Редактировать категорию', callback_data='edit_category')],
    [InlineKeyboardButton(text='Редактировать товар', callback_data='edit_good')]
])

profile_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='💸 Пополнить баланс', callback_data='deposite')],
    [InlineKeyboardButton(text='👱‍♀️🤝👱‍♂️ Реферальная система', callback_data='referal_system')],
    [InlineKeyboardButton(text='🛒 История покупок', callback_data='buy_history')]
])

info_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='🆘 Тех. поддержка', callback_data='add_good')],
    [InlineKeyboardButton(text='🧠 Правила', callback_data='add_category')],
    [InlineKeyboardButton(text='🫀 Наши проекты', callback_data='del_category')]
])

deposite_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Пополнить баланс', callback_data='deposite')]
])

def url(u):
    kb = [] 
    kb.append([InlineKeyboardButton(text='Перейти к оплате', url=u)])
    return InlineKeyboardMarkup(kb)
