from unittest import TestCase, main
from json import dumps
from app.cypher import encrypt, order


class CypherTest(TestCase):

    body1 = {'key1': 'value1', 'key3': 'value3', 'key2': {'key2': 'value2', 'key1': 'value1'}}
    body2 = {"message": "baca", "link": "", "dispatchers": ["vk", "discord", "telegram"]}

    def test_ordering(self):
        self.assertEqual(order(self.body1), 'key1=value1&key2=key1=value1&key2=value2&key3=value3')
        self.assertEqual(order(self.body2), 'dispatchers=vk;discord;telegram&link=&message=baca')

    def test_encryption(self):
        text = dumps(self.body1)
        self.assertEqual(encrypt(text), '5804c819d1b675d46c8fcc2d91981cdcc32e0b7ba53358c34b640c076243e39b')
        text = dumps(self.body2)
        self.assertEqual(encrypt(text), '013252888b60d65346b8631acd6e6301d06a046a9775a8bbc5666056e0343226')


if __name__ == "__main__":
    main()
