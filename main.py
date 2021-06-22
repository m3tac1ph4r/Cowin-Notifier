import os
import sys
import helper
import logging
import telebot
import decouple
from decouple import config


API_KEY = decouple.config("API_KEY")
HELP_FILE = "assets/help.msg"
CREDIT_FILE = "assets/credit.msg"


bot = telebot.TeleBot(API_KEY)
telebot.logger.setLevel(logging.DEBUG)
# /help command
@bot.message_handler(commands=["start","help"])
def help(message):
    help_text = open(HELP_FILE).read()
    bot.send_message(message.chat.id, help_text)
    helper.command_click(message.chat.id)

# /credits command
@bot.message_handler(commands=["credits"])
def credit(message):
    credit_text = open(CREDIT_FILE).read()
    bot.send_message(message.chat.id, credit_text)


# /notify-start command
@bot.message_handler(commands=["notify-start"])
def notify_start(message):
    state=helper.state_click(message.chat.id)
    district=helper.district_click(message.chat.id,state)
    age=helper.age_click(message.chat.id)
    with open("assets/post_message") as f:
        data=str(f.read())
        data=str(data)
        bot.send_message(message.chat.id,data)

# /notify-stop command
@bot.message_handler(commands=["notify-stop"])
def notify_stop(message):
    helper.delete_user(message.chat.id)
    s="Thank you for using Cowin Notifier"
    bot.send_message(message.chat.id, s)

# /vaxinfo
@bot.message_handler(commands=["vaxinfo"])
def vaxinfo(message):
    state = helper.state_click(message.chat.id)
    district=helper.district_click(message.chat.id,state)
    age=helper.age_click(message.chat.id)
    helper.immediate_vax_info(message.chat.id, state, district, age)
    helper.delete_user(message.chat.id)


#this will handle all other messages
def handle_messages(messages):
    for message in messages:
        result=helper.filter_message(message.chat.id,message.text)



bot.set_update_listener(handle_messages)
bot.polling()
