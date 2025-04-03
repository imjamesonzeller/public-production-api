from flask import Flask
from flask_cors import CORS

from routes.generate_word_search import generate_word_search_bp
from routes.get_current_read import get_current_read_bp
from routes.get_notion_tasks import get_notion_tasks_bp
from routes.get_upcoming_events import get_upcoming_events_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(get_current_read_bp)
app.register_blueprint(generate_word_search_bp)
app.register_blueprint(get_notion_tasks_bp)
app.register_blueprint(get_upcoming_events_bp)

def main() -> None:
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()