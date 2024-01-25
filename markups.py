from aiogram import types


def start_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text='Начать🤓')
    menu.add(button)
    return menu