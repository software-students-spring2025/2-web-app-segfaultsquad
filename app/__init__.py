import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from .auth import init_login_manager
from .routes import main as main_blueprint



load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    app.config['db'] = client.get_default_database()

    init_login_manager(app)
    app.register_blueprint(main_blueprint)

    return app
