import ast
import config
import telebot
import functions
import keyboards
from telebot import types,util

bot = telebot.TeleBot(config.bot_token)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.chat.type == 'private':
        text = functions.get_lang_message('RU', 'technical_messages', 'welcome_message_private')
        bot.reply_to(message, text, parse_mode="Markdown")
    else:
        if message.text == '/start':
            text = functions.get_lang_message('RU', 'technical_messages', 'welcome_message_chat')
            bot.reply_to(message, text, parse_mode="Markdown")
        else:
            text = functions.get_lang_message('RU', 'technical_messages', 'bot_commands')
            bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['language'])
def send_welcome(message):
    if message.chat.type != 'private':
        if functions.check_if_user_is_admin(message.from_user.id, bot.get_chat_administrators(message.chat.id)) == 1:
            if functions.check_is_bot_admin_in_chat(bot.get_me(), bot.get_chat_administrators(message.chat.id)) == 1:
                text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages', 'choose_lang')
                bot.send_message(message.chat.id, text=text, reply_markup=keyboards.lang_keyboard(), parse_mode="Markdown")
            else:
                text = functions.get_lang_message('RU', 'technical_messages', 'welcome_message_chat')
                bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['lock'])
def send_welcome(message):
    if message.chat.type != 'private':
        if functions.check_if_user_is_admin(message.from_user.id, bot.get_chat_administrators(message.chat.id)) == 1:
            if functions.check_if_user_is_admin(bot.get_me(), bot.get_chat_administrators(message.chat.id)) == 1:
                if functions.get_lock_status_chat(message.chat.id) == 0:
                    if functions.update_lock_status(message.chat.id, 1) == 1:
                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'lock_status', 'lock_off')
                        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
                elif functions.get_lock_status_chat(message.chat.id) == 1:
                    if functions.update_lock_status(message.chat.id, 0) == 1:
                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'lock_status', 'lock_on')
                        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
            else:
                text = functions.get_lang_message('RU', 'technical_messages', 'welcome_message_chat')
                bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['limit'])
def send_welcome(message):
    if message.chat.type != 'private':
        if functions.check_if_user_is_admin(message.from_user.id, bot.get_chat_administrators(message.chat.id)) == 1:
            if functions.check_if_user_is_admin(bot.get_me(), bot.get_chat_administrators(message.chat.id)) == 1:
                limit = message.text.replace('/limit ', '')
                if limit.isnumeric() == True:
                    if functions.update_limit_chat(message.chat.id, limit) == 1:
                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'limit',
                                                          'limit_change')
                        text = text.replace('{limit}', str(limit))
                        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
            else:
                text = functions.get_lang_message('RU', 'technical_messages', 'welcome_message_chat')
                bot.reply_to(message, text, parse_mode="Markdown")

@bot.my_chat_member_handler()
def my_chat_m(message: types.ChatMemberUpdated):
    new = message.new_chat_member
    if new.status == "member":
        if functions.add_new_chat(message.chat.id) != 0:
            text = functions.get_lang_message('RU', 'technical_messages', 'welcome_message_chat')
            bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if (call.data.startswith("['menu_language'")):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        user_choose_lang_id = ast.literal_eval(call.data)[1]
        if user_choose_lang_id == 'RU':
            if functions.update_chat_lang(chat_id=call.message.chat.id, lang_id='RU') == 1:
                text = functions.get_lang_message('RU', 'technical_messages',
                                                  'lang_successfully_changed')
                bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        elif user_choose_lang_id == 'UA':
            if functions.update_chat_lang(chat_id=call.message.chat.id, lang_id='UA') == 1:
                text = functions.get_lang_message('UA', 'technical_messages',
                                                  'lang_successfully_changed')
                bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

def main():
    if functions.check_system() == 1:
        bot.infinity_polling()

if __name__ == "__main__":
    main()