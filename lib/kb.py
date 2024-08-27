from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='', callback_data='' )]
])

menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn1 = KeyboardButton('Каталог товаров')
btn2 = KeyboardButton('Профиль')
btn3 = KeyboardButton('Информация')
btn4 = KeyboardButton('Наши проекты')
btn5 = KeyboardButton('Наш чат услуг')

menu.add(btn1).row(btn2, btn3).row(btn4, btn5)

def categories(res):
    kb = []
    for i in range(len(res)):
        kb.append([InlineKeyboardButton(text=res[i].name, callback_data='category;' + str(i))])
    return ReplyKeyboardMarkup(kb)

admin_kb = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Добавить товар', callback_data='add_good')],
    [InlineKeyboardButton(text='Добавить категорию', callback_data='add_category')],
    [InlineKeyboardButton(text='Удалить товар', callback_data='del_good')],
    [InlineKeyboardButton(text='Удалить категорию', callback_data='del_category')]
])

