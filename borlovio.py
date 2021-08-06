class Bor:
    def __init__(self, database):
        self.database = database
    
    def request(self, media):
        return self.database.query({
            "filter": {
                "property": "title",
                "text": {
                    "equals": media
                }
            }
        })

    def query(self, media):
        response = self.request(media)

        if response.status_code != 200:
            return []
        
        return [r["properties"]["Status"]["select"]["name"] for r in response.json()["results"]]

    def status(self, media):
        response = self.query(media)
        return response[0] if len(response) else "Unknown"
    
    def hasSeen(self, media):
        return self.status(media) == "Completed"