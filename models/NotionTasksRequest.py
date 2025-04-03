from models import Request, RequestResponse, Task
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
DBID = os.getenv('DB_ID')
NOTIONSECRET = os.getenv('NOTION_SECRET')

class NotionTasksRequest():
    def __init__(self) -> None:
        notion_request: RequestResponse = self._request_to_notion()
        parsed_notion_request: list[Task] = self._notion_parser(notion_request)
        self._task_dicts: list[dict[str, str]] = [task.to_dict() for task in parsed_notion_request]

    @property
    def tasks(self) -> list[dict[Task]]:
        return self._task_dicts

    def _request_to_notion(self) -> RequestResponse:
        # MAKE ACTUAL REQUEST TO NOTION
        new_request = Request()

        new_request.config(DBID, NOTIONSECRET)

        # FILTER TO ONLY TASKS THAT ARE NOT COMPLETED
        filter = {
            "filter": {
                "property": "Done",
                "checkbox": {
                    "equals": False
                }
            }
        }

        new_request.set_filter(filter)
        response = new_request.request()

        return response
    
    def _format_due_date(self, due_date) -> str:
        date_obj = datetime.fromisoformat(due_date)
        return date_obj.strftime('%A, %B %d')

    def _notion_parser(self, response: RequestResponse) -> list[Task]:
        # TAKE NOTION REQUEST AND PARSE
        tasks = []

        for result in response["results"]:
            name = result["properties"]["Name"]["title"][0]["text"]["content"]

            due_date = result["properties"]["Due Date"]["date"]
            if due_date:
                due_date = due_date["start"]
                due_date = self._format_due_date(due_date)
            else:
                due_date = "No Due Date"

            priority = result["properties"]["Priority"]["select"]
            priority = priority["name"] if priority else "No Priority Assigned"
            
            task = Task(name, due_date, priority)
            tasks.append(task)
        
        return tasks