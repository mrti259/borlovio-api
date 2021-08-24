from unittest import TestCase
from config import Config

class TestAmorcito(TestCase):
    def __init__(self, _):
        super().__init__(_)
        self._user_id = 1
        self._amorcito = Config().amorcito()
        self._actions = {
            "say_hi": lambda x: "Hi"
        }

    def setUp(self):
        self._amorcito.clear_active_users()

    def test_user_is_not_active(self):
        self.assertFalse(self._amorcito.is_user_active(self._user_id))

    def test_user_is_active(self):
        self._amorcito.sign_in(self._user_id)
        self.assertTrue(self._amorcito.is_user_active(self._user_id))

    def test_user_is_not_authorize(self):
        self._amorcito.sign_in(self._user_id)
        self.assertFalse(self._amorcito.is_user_authorize(self._user_id))

    def test_user_is_authorize(self):
        self._amorcito.load_user(self._user_id)
        self.assertTrue(self._amorcito.is_user_authorize(self._user_id))

    def test_no_auth_user_ask_for_input_returns_forbbiden_action(self):
        self._amorcito.sign_in(self._user_id)
        self.assertEqual(self._amorcito.ask_for_input(self._user_id), self._amorcito.forbidden(self._user_id))

    def test_auth_user_ask_for_input_returns_start_action(self):
        self._amorcito.load_user(self._user_id)
        self.assertEqual(self._amorcito.ask_for_input(self._user_id), self._amorcito.start(self._user_id))

    def test_auth_user_reply_for_start_replies_for_command(self):
        self._amorcito.load_actions(self._actions)
        self._amorcito.load_user(self._user_id)
        self._amorcito.ask_for_input(self._user_id)
        self.assertEqual(self._amorcito.reply_for(self._user_id, "say_hi"), self._actions["say_hi"](self._user_id))