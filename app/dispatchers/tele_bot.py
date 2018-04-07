import telebot
from simple_settings import settings


def main(message, link=None, channel=settings.tele_channel):
    bot = telebot.TeleBot(settings.tele_token)
    if link:
        message += '\n' + link
    bot.send_message(channel, message)
    return 'ok'
