from flask_restx import fields
from ..utils.extensions import api


user_model = api.model(
    "Student",
    {
        "id": fields.Integer,
        "name": fields.String,
    },
)

