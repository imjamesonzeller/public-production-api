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