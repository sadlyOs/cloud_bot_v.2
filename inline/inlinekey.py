from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.password import host, dbname, user, password
from db.main import Database

database = Database(host, dbname, user, password)
choice = InlineKeyboardMarkup(row_width=2)


# Создаём кнопки
def create_choice():
    choice = InlineKeyboardMarkup(row_width=3)
    inlin1 = InlineKeyboardButton("Добавить фото", callback_data='but1')
    inlin2 = InlineKeyboardButton("Вывести фото", callback_data='buttton')
    inlin3 = InlineKeyboardButton("Удалить категорию", callback_data='del')

    # Добавляем кнопки в клавиатуру
    choice.row(inlin1, inlin2, inlin3)
    return choice


# Парсим категории в кнопки
def add_key(id_):
    buttons = database.return_catigories(id_)  # Возращает категории из бд
    buttons = list(set(buttons))
    menu = InlineKeyboardMarkup(row_width=2)
    for button in range(len(buttons)):
        all_bt = InlineKeyboardButton(text=buttons[button], callback_data=f"{buttons[button]}")
        menu.add(all_bt)
    return menu
