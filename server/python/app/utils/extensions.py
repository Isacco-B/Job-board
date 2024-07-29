from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate

api = Api(
    version="1.0.0",
    title="Job Board API",
    description="Job Board API",
    license="MIT",
    doc="/docs",
)

db = SQLAlchemy()
migrate = Migrate()
