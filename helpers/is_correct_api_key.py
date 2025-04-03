import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('CORRECT_API_KEY')

def is_correct_api_key(request) -> bool:
    given_api_key = request.headers.get('x-api-key')
    return given_api_key == API_KEY