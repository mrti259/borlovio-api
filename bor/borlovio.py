from abc import ABC, abstractmethod
from .bor import Bor

class BLV(ABC):
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