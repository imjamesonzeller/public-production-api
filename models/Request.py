import requests
from models import NotionDBRequest, RequestResponse, RequestFailure

class Request(NotionDBRequest):
    def __init__(self):
        super().__init__()
        self.response: dict = {}
        self.filter: dict = {}

    def __str__(self):
        return str(self.response)

    def set_filter(self, filter: dict) -> None:
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