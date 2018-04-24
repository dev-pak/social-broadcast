from unittest import TestCase, main
from app.server import RequestSchema


class ValidationTest(TestCase):

    def test_alright(self):
        message = {"message": "vaca",
                   "link": "https://vk.com/skinsdeathmatch?w=wall-151563291_14436",
                   "dispatchers": ["vk"]}

        validation = RequestSchema().validate(message)
        self.assertEqual(validation, {})

    def test_invalid_link(self):
        message = {"message": "vaca",
                   "link": "https://vk.com",
                   "dispatchers": ["vk"]}

        validation = RequestSchema().validate(message)
        self.assertEqual(validation, {"link": ["Not a valid URL."]})






if __name__ == '__main__':
    main()
