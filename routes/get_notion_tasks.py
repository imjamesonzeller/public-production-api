from flask import Blueprint, jsonify, request, abort, Response
from helpers import is_correct_api_key
from models import NotionTasksRequest

get_notion_tasks_bp = Blueprint('get_notion_tasks', __name__)

@get_notion_tasks_bp.route('/get_notion_tasks', methods=['GET', 'OPTIONS'])
def get_notion_tasks_route() -> Response:
    if request.method == 'OPTIONS':
        return '', 200
    
    if not is_correct_api_key(request):
        abort(403)
    
    notion_tasks_request = NotionTasksRequest()
    tasks = notion_tasks_request.tasks
    return jsonify(tasks)