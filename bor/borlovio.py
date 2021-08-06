from .bor import Bor

class BorLoVio:
    def __init__(self, database):
        self.bor = Bor(database)
    
    def answer_for(self, media):
        return self.bor.status_for(media, self)

    def has_seen(self, media):
        return f"Si, vi {media}!"

    def is_watching(self, media):
        return f"No, pero estoy viendo {media} :D"

    def wants_to_watch(self, media):
        return f"No, no vi {media}, pero la tengo pendiente :)"

    def does_not_know(self, media):
        return f"No, no vi {media} :("