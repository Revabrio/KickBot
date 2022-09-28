from telebot import types

def del_menu():
    keyboard = types.InlineKeyboardMarkup()
    return keyboard

def lang_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Русский',
                                            callback_data="['menu_language', 'RU']"))
    keyboard.add(types.InlineKeyboardButton(text='Українська',
                                            callback_data="['menu_language', 'UA']"))
    keyboard.add(types.InlineKeyboardButton(text='Отмена/Cancel',
                                            callback_data="['menu_language', '0']"))
    return keyboard