import os
import ast
import config
import database
from langs import langs

def check_system():
    if os.path.exists(config.database_way) == False:
        if os.mkdir(config.database_way) == True:
            pass
        else:
            return 0
    else:
        if database.check_table_users() == 1:
            if database.check_table_block_polls() == 1:
                print('System is ok. Start Bot')
                return 1
    return 0

def get_lang_message(lang, message_chapter, message_id):
    if lang == 'RU':
        return langs.RU[message_chapter][message_id]
    elif lang == 'UA':
        return langs.UA[message_chapter][message_id]

def get_lang_chat(chat_id):
    return database.get_chat_lang(chat_id)

def get_lock_status_chat(chat_id):
    return database.get_chat_lock_status(chat_id)

def get_chat_users_limit(chat_id):
    return database.get_chat_users_limit(chat_id)

def get_block_poll_chat_user(chat_id, user_id):
    data = database.get_block_poll_chat_user(chat_id, user_id)
    if data == 0:
        return 0
    else:
        return data[0], data[1], data[2], data[3], ast.literal_eval(data[4]), ast.literal_eval(data[5])

def get_block_poll_chat_message(chat_id, message_id):
    data = database.get_block_poll_chat_message(chat_id, message_id)
    if data == 0:
        return 0
    else:
        return data[0], data[1], data[2], data[3], ast.literal_eval(data[4]), ast.literal_eval(data[5])

def add_new_block_poll(chat_id, user_id, user_ban):
    return database.add_new_block_poll(chat_id, user_id, user_ban)

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

def update_message_id_block_polls(chat_id, user_id, message_id):
    return database.update_block_poll_message_id(chat_id, user_id, message_id)

def update_vote(chat_id, message_id, data, status, user_id):
    if status == 1:
        array_block = ast.literal_eval(str(data[4]))
        array_block.append(user_id)
        vote_ban = ast.literal_eval(str(data[2])) + 1
        return database.update_vote_block(chat_id, message_id, vote_ban, array_block)
    elif status == 2:
        array_pardon = ast.literal_eval(str(data[5]))
        array_pardon.append(user_id)
        vote_pardon = ast.literal_eval(str(data[3])) + 1
        return database.update_vote_pardon(chat_id, message_id, vote_pardon, array_pardon)

def delete_block_poll(chat_id, user_id):
    return database.delete_block_poll(chat_id, user_id)