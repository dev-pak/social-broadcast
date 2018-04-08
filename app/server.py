from flask import Flask
from flask import request
from flask import jsonify
from marshmallow import Schema, fields, validates, ValidationError
from simple_settings import settings
from cypher import encrypt
import dispatchers.vk_bot
import dispatchers.discord_bot
import dispatchers.tele_bot


app = Flask(__name__)


class RequestSchema(Schema):
    message = fields.String(required=True)

    @validates('message')
    def validate_message(self, value):
        if len(value) > 1000:
            raise ValidationError('Too long text message')

    link = fields.URL()

    @validates('link')
    def validate_link(self, value):
        if settings.url not in value:
            raise ValidationError('Invalid link')

    dispatchers = fields.List(fields.String())

    @validates('dispatchers')
    def validate_dispatchers(self, value):
        if value != [] and list(set(value) & {'vk', 'telegram', 'discord'}) == []:
            raise ValidationError('Unexpected dispatchers')

    if settings.encryption:
        sign = fields.String(required=True)


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
    validation = RequestSchema().validate(message)

    print(validation)

    if validation != {}:
        return jsonify(validation)

    if 'X-Forwarded-For' in request.headers:
        ip = request.headers.getlist('X-Forwarded-For')[0]
    elif 'X-Real-Ip' in request.headers:
        ip = request.headers.getlist('X-Real-Ip')[0]
    else:
        ip = request.remote_addr

    if ip not in settings.ip:
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

    if not settings.vk_bot:
        return jsonify('ok')

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
    return jsonify('ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
