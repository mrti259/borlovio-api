from abc import ABC, abstractmethod

class Controller(ABC):
    def __init__(self, bot):
        self._bot = bot
        self._user_dict = {}

    @classmethod
    def load_actions_on(cls, bot):
        def name(controller):
            return controller.__name__

        for sub in cls.__subclasses__():
            bot.load_actions({
                name(sub): sub(bot).index
            })

    @abstractmethod
    def index(self, user_id, message, xbot):
        pass

    def exito(self, user_id, message, xbot):
        xbot.send_message(user_id, "Listo!")

    def fallo(self, user_id, message, xbot):
        xbot.send_message(user_id, "No se pudo completar la acción")