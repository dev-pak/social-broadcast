import vk
from math import ceil
from storage import storage
from simple_settings import settings


def main(message, link=None, members=storage.all()):

    if link:
        link = link.split('w=')[1]

    session = vk.Session(settings.vk_token)
    api = vk.API(session)
    count = len(members)
    for offset in range(ceil(count / 100)):
        api.messages.send(user_ids=members[offset * 100:(offset + 1) * 100], message=message, attachment=link, version=5.73)


def subscribe(user_id):
    if storage.set(user_id):
        return 'Ты подписался на рассылку. Но это не точно'
    else:
        return 'Я очень польщен, но дважды подписаться на рассылку нельзя'


def unsubscribe(user_id):
    if storage.delete(user_id):
        return 'Ты отписался от рассылки, я на тебя обиделся'
    else:
        return 'Неплохая попытка, но нельзя отписаться, не подписавшись'

