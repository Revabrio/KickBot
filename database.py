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