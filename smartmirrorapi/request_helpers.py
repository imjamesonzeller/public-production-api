from smartmirrorapi.notion_request_objects import Request, RequestResponse, Task
from smartmirrorapi.cal_events import get_upcoming_API
from datetime import datetime

def request_to_notion() -> RequestResponse:
    # MAKE ACTUAL REQUEST TO NOTION
    new_request = Request()

    DBID = "383875b3347e4089b7c69a123b96cd81"
    NOTIONSECRET = "secret_7gs8QoqA9WSauuq5OZbpFlT78OuxKeUhEsR4ingxfys"

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

    new_request.setFilter(filter)
    response = new_request.request()

    return response

def format_due_date(due_date):
    date_obj = datetime.fromisoformat(due_date)
    return date_obj.strftime('%A, %B %d')

def notion_parser(response: RequestResponse) -> list[Task]:
    # TAKE NOTION REQUEST AND PARSE
    tasks = []

    for result in response["results"]:
        name = result["properties"]["Name"]["title"][0]["text"]["content"]

        due_date = result["properties"]["Due Date"]["date"]
        if due_date:
            due_date = due_date["start"]
            due_date = format_due_date(due_date)
        else:
            due_date = "No Due Date"

        priority = result["properties"]["Priority"]["select"]
        if priority:
            priority = priority["name"]
        else:
            priority = "No Priority Assigned"
        
        task = Task(name, due_date, priority)
        tasks.append(task)
    
    return tasks

def get_tasks():
    notion_request = request_to_notion()
    parsed = notion_parser(notion_request)
    task_dicts = [task.to_dict() for task in parsed]

    return task_dicts

def get_upcoming_events():
    events = get_upcoming_API()
    events_dict = [event.to_dict() for event in events]

    return events_dict