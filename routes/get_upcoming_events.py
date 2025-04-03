from flask import Blueprint, jsonify, request, abort, Response
from models import CalEventsRequest
from helpers import is_correct_api_key

get_upcoming_events_bp = Blueprint('get_upcoming_events', __name__)

@get_upcoming_events_bp.route('/get_upcoming_events', methods=['GET', 'OPTIONS'])
def get_upcoming_events_route() -> Response:
    if request.method == 'OPTIONS':
        return '', 200
    
    if not is_correct_api_key(request):
        abort(403)

    cal_events_request = CalEventsRequest()
    tasks = cal_events_request.events
    return jsonify(tasks)