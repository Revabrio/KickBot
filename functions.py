import os
from langs import langs
import config
import database

def check_system():
    if os.path.exists(config.database_way) == False:
        if os.mkdir(config.database_way) == True:
            pass
        else:
            return 0
    else:
        if database.check_table_users() == 1:
            print('System is ok. Start Bot')
            return 1

def get_lang_message(lang, message_chapter, message_id):
    if lang == 'RU':
        return langs.RU[message_chapter][message_id]
    elif lang == 'UA':
        return langs.UA[message_chapter][message_id]

def get_lang_chat(chat_id):
    return database.get_chat_lang(chat_id)

def get_lock_status_chat(chat_id):
    return database.get_chat_lock_status(chat_id)

def add_new_chat(chat_id):
    if database.check_chat_add(chat_id) == 0:
        if database.add_new_chat(chat_id) == 1:
            return 1
        else:
            return 0
    else:
        return 2

def check_if_user_is_admin(user_id, admins):
    for admin in admins:
        if user_id == admin.user.id:
            return 1
    return 0

def check_is_bot_admin_in_chat(my_id, admins):
    for admin in admins:
        if my_id.id == admin.user.id:
            return 1
    return 0

def update_chat_lang(chat_id, lang_id):
    return database.change_lang_chat(chat_id, lang_id)

def update_lock_status(chat_id, lock_status):
    return database.change_lock_status(chat_id, lock_status)

def update_limit_chat(chat_id, limit):
    return database.change_limit_chat(chat_id, limit)