import ast
import config
import telebot
import functions
import keyboards
from telebot import types,util

bot = telebot.TeleBot(config.bot_token)

@bot.message_handler(commands=['help', 'start'])
def commands_help_start(message):
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
def command_language(message):
    if message.chat.type != 'private':
        if functions.check_if_user_is_admin(message.from_user.id, bot.get_chat_administrators(message.chat.id)) == 1:
            if functions.check_is_bot_admin_in_chat(bot.get_me().id, bot.get_chat_administrators(message.chat.id)) == 1:
                text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages', 'choose_lang')
                bot.send_message(message.chat.id, text=text, reply_markup=keyboards.lang_keyboard(), parse_mode="Markdown")
            else:
                text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages', 'welcome_message_chat')
                bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['lock'])
def command_lock(message):
    if message.chat.type != 'private':
        if functions.check_if_user_is_admin(message.from_user.id, bot.get_chat_administrators(message.chat.id)) == 1:
            if functions.check_if_user_is_admin(bot.get_me().id, bot.get_chat_administrators(message.chat.id)) == 1:
                if functions.get_lock_status_chat(message.chat.id) == 0:
                    if functions.update_lock_status(message.chat.id, 1) == 1:
                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'lock_status', 'lock_off')
                        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
                elif functions.get_lock_status_chat(message.chat.id) == 1:
                    if functions.update_lock_status(message.chat.id, 0) == 1:
                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'lock_status', 'lock_on')
                        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
            else:
                text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages', 'welcome_message_chat')
                bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['limit'])
def command_limit(message):
    if message.chat.type != 'private':
        if functions.check_if_user_is_admin(message.from_user.id, bot.get_chat_administrators(message.chat.id)) == 1:
            if functions.check_if_user_is_admin(bot.get_me().id, bot.get_chat_administrators(message.chat.id)) == 1:
                limit = message.text.replace('/limit ', '')
                if limit.isnumeric() == True:
                    if functions.update_limit_chat(message.chat.id, limit) == 1:
                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'limit',
                                                          'limit_change')
                        text = text.replace('{limit}', str(limit))
                        bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
            else:
                text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages', 'welcome_message_chat')
                bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == config.bot_tag:
        if message.reply_to_message != None:
            if message.reply_to_message.from_user.id != bot.get_me().id:
                if functions.check_if_user_is_admin(bot.get_me().id, bot.get_chat_administrators(message.chat.id)) == 0:
                    if functions.get_lock_status_chat(message.chat.id) == 0:
                        if functions.check_if_user_is_admin(message.reply_to_message.from_user.id,
                                                            bot.get_chat_administrators(message.chat.id)) == 0:
                            try:
                                if functions.get_block_poll_chat_user(message.chat.id, message.reply_to_message.from_user.id) == 0:
                                    if functions.add_new_block_poll(message.chat.id, message.reply_to_message.from_user.id,
                                                                    message.from_user.id) == 1:
                                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id),
                                                                          'block_poll',
                                                                          'user_want_block')
                                        text = text.replace('{user_name}', message.from_user.first_name).replace('{user_link}',
                                                                                                                 message.from_user.username)
                                        text = text.replace('{user_name_block}',
                                                            message.reply_to_message.from_user.first_name).replace(
                                            '{user_link_block}', message.reply_to_message.from_user.username)
                                        message_block = bot.send_message(message.chat.id, text=text,
                                                                         reply_markup=keyboards.block_pardon_keyboard(
                                                                             message.chat.id,
                                                                             message.reply_to_message.from_user.id),
                                                                         parse_mode="Markdown", disable_web_page_preview=True)
                                        if functions.update_message_id_block_polls(message.chat.id, message.reply_to_message.from_user.id, message_block.id) != 1:
                                            bot.delete_message(message.chat.id, message_block.id)
                                            functions.delete_block_poll(message.chat.id, message_block.id)
                            except:
                                pass
                    else:
                        try:
                            if functions.check_if_user_is_admin(message.reply_to_message.from_user.id,
                                                                bot.get_chat_administrators(message.chat.id)) == 0:
                                if functions.get_block_poll_chat_user(message.chat.id, message.reply_to_message.from_user.id) == 0:
                                    if functions.add_new_block_poll(message.chat.id, message.reply_to_message.from_user.id,
                                                                    message.from_user.id) == 1:
                                        text = functions.get_lang_message(functions.get_lang_chat(message.chat.id),
                                                                          'block_poll',
                                                                          'user_want_block')
                                        text = text.replace('{user_name}', message.from_user.first_name).replace('{user_link}',
                                                                                                                 message.from_user.username)
                                        text = text.replace('{user_name_block}',
                                                            message.reply_to_message.from_user.first_name).replace(
                                            '{user_link_block}', message.reply_to_message.from_user.username)
                                        message_block = bot.send_message(message.chat.id, text=text,
                                                                         reply_markup=keyboards.block_pardon_keyboard(
                                                                             message.chat.id,
                                                                             message.reply_to_message.from_user.id),
                                                                         parse_mode="Markdown")
                                        if functions.update_message_id_block_polls(message.chat.id,
                                                                                   message.reply_to_message.from_user.id,
                                                                                   message_block.id) != 1:
                                            bot.delete_message(message.chat.id, message_block.id)
                                            functions.delete_block_poll(message.chat.id, message_block.id)
                        except:
                            pass
                else:
                    text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages',
                                                      'welcome_message_chat')
                    bot.reply_to(message, text, parse_mode="Markdown")

@bot.my_chat_member_handler()
def my_chat_m(message: types.ChatMemberUpdated):
    new = message.new_chat_member
    if new.status == "member":
        if functions.add_new_chat(message.chat.id) != 0:
            text = functions.get_lang_message(functions.get_lang_chat(message.chat.id), 'technical_messages', 'welcome_message_chat')
            bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if (call.data.startswith("['menu_language'")):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        user_choose_lang_id = ast.literal_eval(call.data)[1]
        if user_choose_lang_id == 'RU':
            if functions.update_chat_lang(chat_id=call.message.chat.id, lang_id='RU') == 1:
                text = functions.get_lang_message(functions.get_lang_chat(call.message.chat.id), 'technical_messages',
                                                  'lang_successfully_changed')
                bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        elif user_choose_lang_id == 'UA':
            if functions.update_chat_lang(chat_id=call.message.chat.id, lang_id='UA') == 1:
                text = functions.get_lang_message(functions.get_lang_chat(call.message.chat.id), 'technical_messages',
                                                  'lang_successfully_changed')
                bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif (call.data.startswith("['menu_block'")):
        user_choose_block_pardon = ast.literal_eval(call.data)[1]
        if user_choose_block_pardon == 'block':
            data = functions.get_block_poll_chat_message(call.message.chat.id, call.message.message_id)
            if int(call.from_user.id) in ast.literal_eval(str(data[4])) or int(call.from_user.id) in ast.literal_eval(str(data[5])):
                text = functions.get_lang_message(functions.get_lang_chat(call.message.chat.id), 'block_poll',
                                                  'already_vote')
                bot.answer_callback_query(call.id, text=text, show_alert=True)
            else:
                if functions.update_vote(call.message.chat.id, call.message.message_id, data, 1, call.from_user.id) == 1:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.block_pardon_keyboard(
                                                                     call.message.chat.id,
                                                                     data[1]))
                    data = functions.get_block_poll_chat_message(call.message.chat.id, call.message.message_id)
                    if int(data[2]) >= functions.get_chat_users_limit(call.message.chat.id):
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.del_menu())
                        text = functions.get_lang_message(functions.get_lang_chat(call.message.chat.id), 'block_poll',
                                                  'user_successfully_blocked')
                        user_data = bot.get_chat_member(call.message.chat.id, data[1])
                        text = text.replace('{user_name}', str(user_data.user.first_name)).replace('{user_link}', user_data.user.username)
                        users_blocked = ast.literal_eval(str(data[4]))
                        users_blocked_user = ''
                        for i in range(0, len(users_blocked)):
                            try:
                                user_vote_data = bot.get_chat_member(call.message.chat.id, users_blocked[i])
                                users_blocked_user += f'[{str(user_vote_data.user.first_name)}](https://t.me/{user_vote_data.user.username})'
                                if i != len(users_blocked)-1:
                                    users_blocked_user += ', '
                            except:
                                pass
                        text = text.replace('{users_that_blocked}', users_blocked_user)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode="Markdown", disable_web_page_preview=True)
                        bot.ban_chat_member(call.message.chat.id, user_data.user.id)
                        functions.delete_block_poll(call.message.chat.id, user_data.user.id)
        elif user_choose_block_pardon == 'pardon':
            data = functions.get_block_poll_chat_message(call.message.chat.id, call.message.message_id)
            if int(call.from_user.id) in ast.literal_eval(str(data[4])) or int(call.from_user.id) in ast.literal_eval(
                    str(data[5])):
                text = functions.get_lang_message(functions.get_lang_chat(call.message.chat.id), 'block_poll',
                                                  'already_vote')
                bot.answer_callback_query(call.id, text=text, show_alert=True)
            else:
                if functions.update_vote(call.message.chat.id, call.message.message_id, data, 2,
                                         call.from_user.id) == 1:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=keyboards.block_pardon_keyboard(
                                                      call.message.chat.id,
                                                      data[1]))
                    data = functions.get_block_poll_chat_message(call.message.chat.id, call.message.message_id)
                    if int(data[3]) >= functions.get_chat_users_limit(call.message.chat.id):
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                      reply_markup=keyboards.del_menu())
                        text = functions.get_lang_message(functions.get_lang_chat(call.message.chat.id), 'block_poll',
                                                          'user_successfully_pardon')
                        user_data = bot.get_chat_member(call.message.chat.id, data[1])
                        text = text.replace('{user_name}', str(user_data.user.first_name)).replace('{user_link}',
                                                                                           user_data.user.username)
                        users_pardoned = ast.literal_eval(str(data[5]))
                        users_pardoned_user = ''
                        for i in range(0, len(users_pardoned)):
                            try:
                                user_vote_data = bot.get_chat_member(call.message.chat.id, users_pardoned[i])
                                users_pardoned_user += f'[{str(user_vote_data.user.first_name)}](https://t.me/{user_vote_data.user.username})'
                                if i != len(users_pardoned) - 1:
                                    users_pardoned_user += ', '
                            except:
                                pass
                        text = text.replace('{users_that_pardoned}', users_pardoned_user)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=text, parse_mode="Markdown", disable_web_page_preview=True)
                        functions.delete_block_poll(call.message.chat.id, user_data.user.id)

def main():
    #import ast
    #import database
    #database.add_new_block_poll(-602663528, 1, 2)
    #print(ast.literal_eval(database.get_block_poll(-602663528, 1)[4])[0])
    if functions.check_system() == 1:
       bot.infinity_polling(none_stop=True)

if __name__ == "__main__":
    main()