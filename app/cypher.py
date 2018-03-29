from hashlib import sha256
from json import loads, dumps
from simple_settings import settings
import unittest


class CypherTest(unittest.TestCase):

    body = {'key1': 'value1', 'key3': 'value3', 'key2': {'key2': 'value2', 'key1': 'value1'}}

    def test_ordering(self):
        self.assertEqual(order(self.body), 'key1=value1&key2=key1=value1&key2=value2&key3=value3')

    def test_encryption(self):
        text = dumps(self.body)
        self.assertEqual(encrypt(text), '5804c819d1b675d46c8fcc2d91981cdcc32e0b7ba53358c34b640c076243e39b')


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
        k_v_list.append(element[0]+'='+temp)
    text = '&'.join(k_v_list)
    return text


if __name__ == "__main__":
    unittest.main()
