class Amorcito:
    def __init__(self):
        self.clear_active_users()
        self.on_action = {
            "forbidden": self.forbidden,
            "start": self.start,
        }

    def clear_active_users(self):
        self._active_users = {}

    def load_actions(self, actions):
        self._actions = actions

    def is_user_active(self, id):
        return id in self._active_users

    def sign_in(self, user_id, auth=False, action="forbidden"):
        self._active_users[user_id] = {"auth": auth, "action": action}

    def is_user_authorize(self, user_id):
        return self.is_user_active(user_id) and self._active_users[user_id]["auth"] is True

    def load_user(self, user_id):
        return self.sign_in(user_id, auth=True, action="start")

    def ask_for_input(self, user_id):
        return self.on_action[self._active_users[user_id]["action"]](user_id)

    def reply_for(self, user_id, action):
        return self._actions[action](user_id)

    def forbidden(self, user_id):
        return "No estas autorizado"

    def start(self, user_id):
        return "Hola!"