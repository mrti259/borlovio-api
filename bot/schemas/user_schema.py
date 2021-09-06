from .schema import Model, Schema

class User(Model):
    def __init__(self, name="", user_id="", auth="", action=""):
        super().__init__()
        self.name = name
        self.user_id = user_id
        self.auth = auth
        self.action = action

    @property
    def name(self):
        return self.properties["name"]["title"][0]["plain_text"]

    @name.setter
    def name(self, _name):
        self.properties.update({"name": {"title": [{"text": {"content": _name}}]}})

    @property
    def user_id(self):
        return self.properties["chat_id"]["rich_text"][0]["plain_text"]

    @user_id.setter
    def user_id(self, _user_id):
        self.properties.update({"chat_id": {"rich_text": [{"text": {"content": str(_user_id)}}]}})

    @property
    def auth(self):
        return self.properties["authorize"]["checkbox"]

    @auth.setter
    def auth(self, _auth):
        self.properties.update({"authorize": {"checkbox": _auth}})

    @property
    def action(self):
        return self.properties["action"]["select"]["name"]

    @action.setter
    def action(self, _action):
        self.properties.update({"action": {"select": {"name": _action}}})


class UserSchema(Schema):
    def __init__(self, client, database_id):
        super().__init__(client, database_id, User)

    def get(self, user_id):
        user = {
            "user_id": user_id,
            "auth": False,
            "action": "forbidden",
            "name": ""
        }

        res = self.query(filter={
            "property": "chat_id",
            "text": {
                "equals": str(user_id)
            }
        })

        for r in res:
            user["auth"]  = r.auth
            user["action"] = r.action
            user["name"] = r.name

        return user