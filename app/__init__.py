import os
from flask import Flask
from .database import init_db

# Absolute path to project root (one level above this file's directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static')
    )
    app.secret_key = 'bibliotheque_secret_key_2026'

    with app.app_context():
        init_db()

    from .routes.books import books_bp
    from .routes.chatbot import chatbot_bp
    app.register_blueprint(books_bp)
    app.register_blueprint(chatbot_bp)

    return app
