import requests

class RequestFailure(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class NotionDBRequest:
    def __init__(self):
        self.dbid: str = ""
        self.headers = {
            "Authorization": '',
            "Content-Type": 'application/json; charset=utf-8',
            "Notion-Version": '2022-06-28'
        } 

    def config(self, dbid: str, apisecret: str) -> None:
        self.dbid = dbid
        self.headers["Authorization"] = f"Bearer {apisecret}"

class Response(dict): pass

class RequestResponse(Response):
    def __init__(self, response: dict):
        super().__init__(response)

        self.pageids = []
        results = self["results"]
        for result in results:
            self.pageids.append(result["id"])

    def __str__(self):
        return str(dict(self))
    
    def namesToList(self) -> list:
        """
        Returns a list of the titles/names of each database item from the RequestResponse object.
        """
        namelist = []

        results = self["results"]
        for result in results:
            name = result["properties"]["Name"]["title"][0]["text"]["content"]
            namelist.append(name)

        return namelist
    
class Request(NotionDBRequest):
    def __init__(self):
        super().__init__()
        self.response: dict = {}
        self.filter: dict = {}

    def __str__(self):
        return str(self.response)

    def setFilter(self, filter: dict) -> None:
        """
        Sets the filter for the pages to be returned.
        \n Follow the Notion API guide for setting filters OR view examples at \n
        https://jamesonzeller.com/docs/notiondbrequest/db-query-filter \n
        https://developers.notion.com/reference/post-database-query-filter
        """
        self.filter = filter

    def request(self) -> RequestResponse:
        """
        Get the dictionary response. Actually sends request to API.
        """
        self.response = requests.post(url=f"https://api.notion.com/v1/databases/{self.dbid}/query", 
                                 headers=self.headers, 
                                 json=self.filter)
        
        if self.response.status_code == 200:
            self.response = RequestResponse(self.response.json())
            return self.response
        else:
            status_code = self.response.status_code
            self.response = {}
            raise RequestFailure(f"Request Error! Status Code: {status_code}")
        
class Task():
    def __init__(self, name, due_date, priority):
        self.name = name
        self.due_date = due_date
        self.priority = priority

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "due_date": self.due_date,
            "priority": self.priority,
        }
    
class Event():
    def __init__(self, name, date, trueStart):
        self.name = name
        self.date = date
        self.trueStart = trueStart

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "date": self.date,
        }
    
    def __lt__(self, obj):
        return ((self.trueStart) < (obj.trueStart))

    def __gt__(self, obj):
        return ((self.trueStart) > (obj.trueStart))

    def __le__(self, obj):
        return ((self.trueStart) <= (obj.trueStart))

    def __ge__(self, obj):
        return ((self.trueStart) >= (obj.trueStart))

    def __eq__(self, obj):
        return (self.trueStart == obj.trueStart)