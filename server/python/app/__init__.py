from flask import Flask

from .utils.extensions import api, db, migrate
from .secrets import DATABASE_URL

from .controllers.auth_controller import api as auth_api


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api.add_namespace(auth_api)

    return app
