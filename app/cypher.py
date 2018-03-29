from hashlib import sha256
from json import loads
from simple_settings import settings


def encrypt(body):
    text = order(loads(body))
    text += settings.private
    text = text.encode('utf-8')
    return sha256(text).hexdigest()


def order(body):
    k_v_list = []
    body = sorted(body.items(), key=lambda x: x[0])
    for element in body:
        temp = element[1]
        if isinstance(element[1], dict):
            temp = order(element[1])
        if isinstance(element[1], list):
            temp = ";".join(element[1])
        k_v_list.append(element[0]+'='+temp)
    text = '&'.join(k_v_list)
    return text
