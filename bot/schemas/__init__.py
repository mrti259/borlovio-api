from .user_schema import UserSchema

class Schemas:
    def __init__(self, connection):
        self.connection = connection

    @property
    def users(self):
        return UserSchema(self.connection)