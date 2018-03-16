import telebot
from simple_settings import settings


def send(message, channel=settings.tele_channel):
    bot = telebot.TeleBot(settings.tele_token)
    bot.send_message(channel, message)
