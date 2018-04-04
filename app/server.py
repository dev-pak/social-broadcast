from flask import Flask
from flask import request
from flask import jsonify
from flask_marshmallow import Marshmallow, fields
from simple_settings import settings
from cypher import encrypt
import dispatchers.vk_bot
import dispatchers.discord_bot
import dispatchers.tele_bot


app = Flask(__name__)
#ma = Marshmallow(app)


#class RequestSchema(ma.Schema):
#   message = fields.Str(required=True)
#    link = fields.UrlFor()
#    dispatchers = fields.List(fields.Str)
#    if settings.encryption:
#        sign = fields.Str(required=True)


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

    message = request.get_json()
    #validation = RequestSchema.validate(message)

    #if validation is not {}:
    #    return jsonify(validation)

    if 'X-Forwarded-For' in request.headers:
        ip = request.headers.getlist('X-Forwarded-For')[0]
    elif 'X-Real-Ip' in request.headers:
        ip = request.headers.getlist('X-Real-Ip')[0]
    else:
        ip = request.remote_addr

    if not ip in settings.ip:
        return jsonify('Forbidden')

    if settings.encryption:
        if message['sign'] != encrypt(message):
            return jsonify('Forbidden')

    text = message['message']
    try:
        link = message['link']
    except KeyError:
        link = None

    response = {}

    if 'discord' in message['dispatchers']:
        response.update({"discord": dispatchers.discord_bot.main(text, link)})
    if 'telegram' in message['dispatchers']:
        response.update({"telegram": dispatchers.tele_bot.main(text, link)})
    if 'vk' in message['dispatchers']:
        response.update({"vk": dispatchers.vk_bot.main(text+ending, link)})
    return jsonify(response)


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
