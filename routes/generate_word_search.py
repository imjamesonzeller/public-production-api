from flask import Blueprint, jsonify, request, Response
from helpers import random_words
from models import WordSearch
from werkzeug.exceptions import BadRequest

generate_word_search_bp = Blueprint('generate_word_search', __name__)

@generate_word_search_bp.route('/generate_word_search', methods=['POST', 'GET'])
def generate_word_search_route() -> Response:
    if request.method == 'GET':
        words = random_words()
    else:
        try:
            data = request.get_json()
            words = data.get('words', [])
        except BadRequest:
            words = random_words()

        if not words:
            words = random_words()
    
    grid = WordSearch(words)
    result = { 'search': grid.generate_word_search(), 'words': grid.words }

    return jsonify(result)