from telebot import *
from code import classes, base, markups

token = ''
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.from_user.id, 'И чё?\nИ зачем?\nИли ты тут сам себе что-то объяснять собрался?',
                     reply_markup=markups.main_markup)

@bot.callback_query_handler(func=lambda call: call.data[0] == '#')
def handle_day(call):
    pass

@bot.callback_query_handler(func=lambda call: int(call.data) == 1)
def handle_rasp(call):
    bot.send_message(call.message.chat.id,'Хавай свое расписание, мразота...', reply_markup=markups.get_rasp())




bot.polling(none_stop=True)
