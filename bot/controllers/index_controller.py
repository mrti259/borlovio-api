from . import Controller

class IndexController(Controller):
    def _filter_actions(self, suffix):
        return filter(lambda action: action.endswith(suffix) and self.__class__.__name__ != action, self._bot.actions)

    def _remove_suffix(self, actions, suffix):
        return map(lambda action: action.replace(suffix, ""), actions)

    def index(self, user_id, message, xbot):
        suffix = "Controller"
        options = list(self._remove_suffix(self._filter_actions(suffix), suffix))

        def nxt(msg):
            text = msg.text
            if text in options:
                self._bot.actions[text + suffix](user_id, msg, xbot)
            else:
                self._bot.default(user_id, msg, xbot)

        xbot.send_message_with_options_and_next_step_handler(user_id, "Que querés ver?", options, nxt)