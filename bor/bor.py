class Bor:
    def __init__(self, database):
        self.database = database

    def status_for(self, media, res):
        response = self.query(media)

        if "Completed" in response:
            return res.has_seen(media)
        
        if "In progress" in response:
            return res.is_watching(media)
        
        if "Not started" in response:
            return res.wants_to_watch(media)
        
        return res.does_not_know(media) 
    
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