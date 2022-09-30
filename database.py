import config
import sqlite3
conn = sqlite3.connect(config.database_way, check_same_thread=False)

def check_table_users():
    c = conn.cursor()
    try:
        c.execute(
            'CREATE TABLE chats (chat_id INTEGER UNIQUE NOT NULL, lang_id STRING NOT NULL DEFAULT RU, lock INTEGER DEFAULT (1), bot_is_admin INTEGER NOT NULL DEFAULT (0), users_limit  INTEGER NOT NULL DEFAULT (10))')
        print('Table chats successfully created')
    except:
        print('Table chats exist')
    return 1

def check_table_block_polls():
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE block_polls (chat_id INTEGER, user_id INTEGER, vote_ban INTEGER, vote_pardon INTEGER, vote_ban_array TEXT, vote_pardon_array TEXT, message_id INTEGER)')
        print('Table block_polls successfully created')
    except:
        print('Table block_polls exist')
    return 1

def check_chat_add(chat_id):
    c = conn.cursor()
    try:
        c.execute('SELECT 1 FROM chats WHERE chat_id =?', (chat_id,))
        rows = c.fetchall()
        if not rows:
            return 0
        else:
            return 1
    except:
        return -1

def add_new_chat(chat_id):
    c = conn.cursor()
    try:
        c.execute('INSERT INTO chats (chat_id) VALUES (?)',(chat_id,))
        conn.commit()
        return 1
    except:
        return -1

def add_new_block_poll(chat_id, user_id, user_ban):
    c = conn.cursor()
    try:
        vote_ban_array = [user_ban]
        vote_pardon_array = [user_id]
        c.execute('INSERT INTO block_polls (chat_id, user_id, vote_ban, vote_pardon, vote_ban_array, vote_pardon_array) VALUES (?, ?, ?, ?, ?, ?)',(chat_id, user_id, 1, 1, str(vote_ban_array), str(vote_pardon_array),))
        conn.commit()
        return 1
    except:
        return -1

def get_block_poll_chat_user(chat_id, user_id):
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM block_polls WHERE chat_id =? and user_id =?', (chat_id, user_id,))
        rows = c.fetchall()
        if rows:
            return rows[0]
        elif not rows:
            return 0
    except:
        return -1

def get_block_poll_chat_message(chat_id, message_id):
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM block_polls WHERE chat_id =? and message_id =?', (chat_id, message_id,))
        rows = c.fetchall()
        if rows:
            return rows[0]
        elif not rows:
            return 0
    except:
        return -1

def get_chat_lang(chat_id):
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM chats WHERE chat_id =?', (chat_id,))
        rows = c.fetchall()
        return rows[0][1]
    except:
        return -1

def get_chat_lock_status(chat_id):
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM chats WHERE chat_id =?', (chat_id,))
        rows = c.fetchall()
        return rows[0][2]
    except:
        return -1

def get_chat_users_limit(chat_id):
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM chats WHERE chat_id =?', (chat_id,))
        rows = c.fetchall()
        return rows[0][4]
    except:
        return -1

def change_lang_chat(chat_id, lang_id):
    c = conn.cursor()
    try:
        c.execute('UPDATE chats SET lang_id =? WHERE chat_id =?', (lang_id, chat_id,))
        conn.commit()
        return 1
    except:
        return -1

def change_lock_status(chat_id, lock_status):
    c = conn.cursor()
    try:
        c.execute('UPDATE chats SET lock =? WHERE chat_id =?', (lock_status, chat_id,))
        conn.commit()
        return 1
    except:
        return -1

def change_limit_chat(chat_id, limit):
    c = conn.cursor()
    try:
        c.execute('UPDATE chats SET users_limit =? WHERE chat_id =?', (limit, chat_id,))
        conn.commit()
        return 1
    except:
        return -1

def update_block_poll_message_id(chat_id, user_id, message_id):
    c = conn.cursor()
    try:
        c.execute('UPDATE block_polls SET message_id =? WHERE chat_id =? and user_id =?', (message_id, chat_id, user_id,))
        conn.commit()
        return 1
    except:
        return -1

def update_vote_block(chat_id, message_id, vote_ban, vote_ban_array):
    c = conn.cursor()
    try:
        c.execute('UPDATE block_polls SET vote_ban_array =? WHERE chat_id =? and message_id =?',
                  (str(vote_ban_array), chat_id, message_id,))
        c.execute('UPDATE block_polls SET vote_ban =? WHERE chat_id =? and message_id =?',
                  (str(vote_ban), chat_id, message_id,))
        conn.commit()
        return 1
    except:
        return -1

def update_vote_pardon(chat_id, message_id, vote_pardon, vote_pardon_array):
    c = conn.cursor()
    try:
        c.execute('UPDATE block_polls SET vote_pardon_array =? WHERE chat_id =? and message_id =?',
                  (str(vote_pardon_array), chat_id, message_id,))
        c.execute('UPDATE block_polls SET vote_pardon =? WHERE chat_id =? and message_id =?',
                  (str(vote_pardon), chat_id, message_id,))
        conn.commit()
        return 1
    except:
        return -1

def delete_block_poll(chat_id, user_id):
    c = conn.cursor()
    try:
        c.execute('DELETE FROM block_polls WHERE chat_id =? and user_id =?',
                  (chat_id, user_id,))
        conn.commit()
        return 1
    except:
        return -1