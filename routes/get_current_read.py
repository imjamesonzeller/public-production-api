from flask import Blueprint, jsonify, Response
from models import CurrentRead

get_current_read_bp = Blueprint('get_current_read', __name__)

@get_current_read_bp.route('/get_current_read', methods=['GET'])
def get_current_read_route() -> Response:
    current_read = CurrentRead()
    result = { 'attrs': current_read.attrs }
    return jsonify(result)