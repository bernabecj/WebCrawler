import os
from flask import Flask
from flask_admin import Admin
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    from .main import main as main_blueprint
    from .routes import routes as routes_blueprint

    # Register blueprints safely
    if "main" not in app.blueprints:
        app.register_blueprint(main_blueprint)

    if "routes" not in app.blueprints:
        app.register_blueprint(routes_blueprint)

    # Create a new Admin instance inside create_app to avoid reuse issues
    admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")

    return app
