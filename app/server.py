from flask import Flask
from flask import request
from simple_settings import settings
from cypher import encrypt
import dispatchers.vk_bot
import dispatchers.discord_bot
import dispatchers.tele_bot

app = Flask(__name__)


class BadRequest(Exception):
    status_code = 400

class Forbidden(Exception):
    status_code = 403

class GetError(Exception):
    text = 'Ошибка входных данных'


@app.route("/")
def index():
    return 'Flask is running'


@app.route("/send", methods=['POST'])
def send():

    ending = '\nДля отписки от рассылки напиши /unsub'

    if 'X-Forwarded-For' in request.headers:
        ip = request.headers.getlist('X-Forwarded-For')[0]
    elif 'X-Real-Ip' in request.headers:
        ip = request.headers.getlist('X-Real-Ip')[0]
    else:
        ip = request.remote_addr

    if not ip in settings.ip:
        raise Forbidden

    message = request.get_json()

    if settings.encryption:
        if message['sign'] != encrypt(message):
            raise Forbidden

    text = message['message']
    try:
        link = message['link']
    except KeyError:
        pass

    if 'discord' in message['dispatchers']:
        dispatchers.discord_bot.main(text, link)
    if 'telegram' in message['dispatchers']:
        dispatchers.tele_bot.main(text, link)
    if 'vk' in message['dispatchers']:
        dispatchers.vk_bot.main(text+ending, link)
    return 'ok'


@app.route("/get", methods=['POST'])
def get():
    message = request.get_json()

    if message['type'] == 'confirmation':
        return settings.confirmation_token

    message = message['object']
    members = [message['user_id']]
    text = None
    if message['body'] == '/sub':
        text = dispatchers.vk_bot.subscribe(message['user_id'])
    elif message['body'] == '/unsub':
        text = dispatchers.vk_bot.unsubscribe(message['user_id'])
    elif message['body'] == '/help':
        text = '/sub для подписки\n' \
               '/unsub для отписки\n' \
               'На этом мои полномочия все'
    if text:
        dispatchers.vk_bot.main(message=text, members=members)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
