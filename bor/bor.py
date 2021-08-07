class Bor:
    def __init__(self, database):
        self.database = database

    def status_for(self, media, blv):
        response = self.query(media)

        if "Completed" in response:
            return blv.has_seen(media)

        if "In progress" in response:
            return blv.is_watching(media)

        if "Not started" in response:
            return blv.wants_to_watch(media)

        return blv.does_not_know(media)

    def request(self, media):
        return self.database.query({
            "filter": {
                "and": [
                    {
                        "property": "title",
                        "text": {
                            "equals": media
                        }
                    },
                    {
                        "property": "Status",
                        "select": {
                            "is_not_empty": True
                        }
                    }
                ]
            }
        })

    def query(self, media):
        response = self.request(media)

        if response.status_code != 200:
            return []

        return [r["properties"]["Status"]["select"]["name"] for r in response.json()["results"]]