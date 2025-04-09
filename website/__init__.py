import os
from flask import Flask
from flask_admin import Admin
from dotenv import load_dotenv


# Load environment variables from .env file production or development
load_dotenv(dotenv_path=".env")

app = Flask(__name__)
admin = Admin()


def create_app(debug=False):
    # Llave secreta
    app.debug = debug
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    from .main import main as main_blueprint
    from .routes import routes as routes_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(routes_blueprint)

    admin.init_app(app)
    return app
