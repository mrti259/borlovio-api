from abc import ABC, abstractclassmethod

class XBot(ABC):
    @abstractclassmethod
    def send_message(self, user_id, message):
        pass

    @abstractclassmethod
    def send_message_with_next_step_handler(self, user_id, message):
        pass

    @abstractclassmethod
    def send_message_with_options_and_next_step_handler(self, user_id, message):
        pass