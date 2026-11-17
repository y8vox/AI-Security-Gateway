from flask import Flask
from flask_cors import CORS
from .routes import api
from .database import init_db


def create_app(testing=False):
    app = Flask(__name__)
    app.config.update(TESTING=testing)
    CORS(app)
    app.register_blueprint(api, url_prefix="/api")
    init_db()
    return app
