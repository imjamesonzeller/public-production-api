from models import Response

class RequestResponse(Response):
    def __init__(self, response: dict):
        super().__init__(response)

        self.pageids: str = []
        results = self["results"]
        for result in results:
            self.pageids.append(result["id"])

    def __str__(self):
        return str(dict(self))
    
    def names_to_list(self) -> list:
        """
        Returns a list of the titles/names of each database item from the RequestResponse object.
        """
        namelist = []

        results = self["results"]
        for result in results:
            name = result["properties"]["Name"]["title"][0]["text"]["content"]
            namelist.append(name)

        return namelist