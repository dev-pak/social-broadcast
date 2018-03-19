from flask import Flask
from flask import request
from json import loads
from simple_settings import settings
import vk_bot
import discord_bot
import tele_bot

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400


class GetError(Exception):
    text = 'Ошибка входных данных'


@app.route("/")
def index():
    return 'Flask is running'


@app.route("/send", methods=['POST'])
def send():
    if 'message' not in request.form:
        raise InvalidUsage

    message = request.form.get('message')
    parsed = request.form.get('parsed')

    if  settings.discord:
        discord_bot.main(message)
    if settings.telegram:
        tele_bot.main(message)
    if settings.vk:
        vk_bot.main(message, parsed)
    return 'ok'


@app.route("/get", methods=['POST'])
def get():
    message = loads(request.data)

    if message['type'] == 'confirmation':
        return settings.confirmation_token

    message = message['object']
    members = [message['user_id']]
    text = None
    if message['body'] == '/sub':
        text = vk_bot.subscribe(message['user_id'])
    elif message['body'] == '/unsub':
        text = vk_bot.unsubscribe(message['user_id'])
    elif message['body'] == '/help':
        text = '/sub для подписки\n' \
               '/unsub для отписки\n' \
               'На этом мои полномочия все'
    if text:
        vk_bot.main(message=text, members=members)
    return 'ok'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888)
