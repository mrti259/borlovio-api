from .schema import Schema

class User:
    def __init__(self, user_id, auth=False, action=""):
        self.user_id = user_id
        self.auth = auth
        self.action = action if action else "IndexController" if auth else "forbidden"

class UserSchema(Schema):
    def get(self, user_id):
        return User(user_id, True).__dict__

    def save(self, user):
        return user