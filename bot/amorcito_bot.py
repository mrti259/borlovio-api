from .bot import Bot
from .controllers import Controller
from .schemas import Schemas

class AmorcitoBot(Bot):
    def __init__(self, connection):
        super().__init__()
        Controller.load_actions_on(self)
        self.schemas = Schemas(connection)

    def default(self, user_id, message, xbot):
        self.ask_for_input(user_id)(user_id, message, xbot)

    def forbidden(self, user_id, message, xbot):
        xbot.send_message(user_id, "No estas autorizado a usar el bot :(")

    def start(self, user_id, message, xbot):
        xbot.send_message(user_id, "Hola!")
        self.default(user_id, message, xbot)

    def load_user(self, user_id):
        return self.schemas.users.get(user_id)

    def save_user(self, user_id):
        return self.schemas.users.save(self._active_users[user_id])

    def on(self, command, message, xbot):
        user_id = message.chat.id
        if not self.is_user_active(user_id):
            self.sign_in(**self.load_user(user_id))
        self.reply_for(user_id, command)(user_id, message, xbot)