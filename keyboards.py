import functions
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

def block_pardon_keyboard(chat_id, user_id):
    keyboard = types.InlineKeyboardMarkup()
    users_to_block = functions.get_chat_users_limit(chat_id)
    text_block = functions.get_lang_message(functions.get_lang_chat(chat_id), 'block_poll', 'block')
    text_block = text_block.replace('{vote_users_block}', str(len(functions.get_block_poll_chat_user(chat_id, user_id)[4])))
    text_block = text_block.replace('{users_need}', str(users_to_block))
    text_pardon = functions.get_lang_message(functions.get_lang_chat(chat_id), 'block_poll', 'pardon')
    text_pardon = text_pardon.replace('{vote_users_pardon}', str(len(functions.get_block_poll_chat_user(chat_id, user_id)[5])))
    text_pardon = text_pardon.replace('{users_need}', str(users_to_block))
    keyboard.add(types.InlineKeyboardButton(text=text_block,
                                            callback_data="['menu_block', 'block']"))
    keyboard.add(types.InlineKeyboardButton(text=text_pardon,
                                            callback_data="['menu_block', 'pardon']"))
    return keyboard