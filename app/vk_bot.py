import vk
from contextlib import redirect_stdout
from math import ceil
from storage import storage
from simple_settings import settings


def main(message, link=None, members=storage.all()):

    if link:
        link = link.split('w=')[1]

    session = vk.Session(settings.vk_token)
    api = vk.API(session)
    count = len(members)
    with open('vk_logs', 'w') as f:
        with redirect_stdout(f):
            for offset in range(ceil(count / 100)):
                response = api.messages.send(user_ids=members[offset * 100:(offset + 1) * 100], message=message, attachment=link, version=5.73)
                #response = api.messages.get(version=5.73)
                print(str(response))


def subscribe(user_id):
    if storage.set(user_id):
        return 'Ты подписался на рассылку. Для отписки напиши /unsub'
    else:
        return 'Я очень польщен, но дважды подписаться на рассылку нельзя'


def unsubscribe(user_id):
    if storage.delete(user_id):
        return 'Ты отписался от рассылки, для подписки напиши /sub'
    else:
        return 'Неплохая попытка, но нельзя отписаться, не подписавшись'

