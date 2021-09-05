from unittest import TestCase
from config import Config

from bot import Bot

class TestBot(TestCase):
    def __init__(self, _):
        super().__init__(_)
        self._user_id = 1
        self._bot = Bot()
        self._actions = {
            "say_hi": lambda x: "Hi",
            "do_something": self._do_something,
            "did_something": lambda x: "Did something!"
        }

    def _do_something(self, user_id):
        self._bot.update_user_action(user_id, "did_something")

    def setUp(self):
        self._bot.clear_active_users()

    def test_01_user_is_not_active(self):
        self.assertFalse(self._bot.is_user_active(self._user_id))

    def test_02_user_is_active(self):
        self._bot.sign_in(self._user_id)
        self.assertTrue(self._bot.is_user_active(self._user_id))

    def test_03_user_is_not_authorize(self):
        self._bot.sign_in(self._user_id)
        self.assertFalse(self._bot.is_user_authorize(self._user_id))

    def test_04_user_is_authorize(self):
        self._bot.load_user(self._user_id)
        self.assertTrue(self._bot.is_user_authorize(self._user_id))

    def test_05_no_auth_user_ask_for_input_returns_forbbiden_action(self):
        self._bot.sign_in(self._user_id)
        self.assertEqual(self._bot.ask_for_input(self._user_id), self._bot.forbidden)

    def test_06_auth_user_ask_for_input_returns_start_action(self):
        self._bot.load_user(self._user_id)
        self.assertEqual(self._bot.ask_for_input(self._user_id), self._bot.start)

    def test_07_auth_user_reply_for_start_replies_for_command(self):
        self._bot.load_actions(self._actions)
        self._bot.load_user(self._user_id)
        self._bot.ask_for_input(self._user_id)(self._user_id)
        self.assertEqual(self._bot.reply_for(self._user_id, "say_hi"), self._actions["say_hi"])

    def test_08_user_can_reply_anything(self):
        self._bot.load_actions(self._actions)
        self.assertEqual(self._bot.reply_for(self._user_id, "any"), self._bot.default)

    def test_09_user_signs_in_when_interacts(self):
        self._bot.reply_for(self._user_id, "any")
        self.assertTrue(self._bot.is_user_active(self._user_id))

    def test_10_auth_user_can_change_action(self):
        self._bot.load_actions(self._actions)
        self._bot.load_user(self._user_id)
        self._bot.reply_for(self._user_id, "do_something")(self._user_id)
        self.assertEqual(self._bot.ask_for_input(self._user_id), self._actions["did_something"])
