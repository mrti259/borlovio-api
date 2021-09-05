class Bot:
    def __init__(self):
        self.clear_active_users()
        self.actions = {
            "": self.default,
            "start": self.start,
            "forbidden": self.forbidden,
        }

    def clear_active_users(self):
        self._active_users = {}

    def load_actions(self, new_actions):
        self.actions.update(new_actions)

    def is_user_active(self, user_id):
        return user_id in self._active_users

    def sign_in(self, user_id, auth=False, action="forbidden", name=""):
        self._active_users[user_id] = {"auth": auth, "action": action, name:""}

    def is_user_authorize(self, user_id):
        return self.is_user_active(user_id) and self._active_users[user_id]["auth"] is True

    def load_user(self, user_id):
        return self.sign_in(user_id, auth=True, action="start")

    def update_user_action(self, user_id, action=None):
        if not action:
            return self._active_users[user_id]["action"]
        self._active_users[user_id]["action"] = action

    def ask_for_input(self, user_id):
        if not self.is_user_active(user_id):
            self.sign_in(user_id)
        return self.actions[self._active_users[user_id]["action"]]

    def reply_for(self, user_id, action):
        if not self.is_user_active(user_id):
            self.sign_in(user_id)
        if not action in self.actions:
            action = ""
        return self.actions[action]

    def forbidden(self, *args):
        pass

    def start(self, *args):
        pass

    def default(self, *args):
        pass