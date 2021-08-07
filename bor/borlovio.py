from abc import ABC, abstractmethod
from .bor import Bor

class BLV(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def ask_for_input(self):
        pass

    @abstractmethod
    def answer_for(self, media):
        pass

    @abstractmethod
    def has_seen(self, media):
        pass

    @abstractmethod
    def is_watching(self, media):
        pass

    @abstractmethod
    def wants_to_watch(self, media):
        pass

    @abstractmethod
    def does_not_know(self, media):
        pass

class BorLoVio(BLV):
    def __init__(self, database):
        self.bor = Bor(database)

    def start(self):
        return "Hola! Decime el nombre de una serie o película y te responderé!"

    def stop(self):
        return "Bye!"

    def ask_for_input(self):
        return "Qué te gustaría preguntar si vi?"

    def answer_for(self, media):
        return self.bor.status_for(media, self)

    def has_seen(self, media):
        return f"Si, vi {media}!"

    def is_watching(self, media):
        return f"Ahora estoy viendo {media} :D"

    def wants_to_watch(self, media):
        return f"No, no vi {media}, pero la tengo pendiente :)"

    def does_not_know(self, media):
        return f"No, no vi {media} :("