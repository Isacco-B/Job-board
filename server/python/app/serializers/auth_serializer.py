from flask_restx import fields
from ..utils.extensions import api


login_model = api.model("Login", {"email": fields.String, "password": fields.String})
register_model = api.model(
    "Register",
    {
        "name": fields.String,
        "email": fields.String,
        "password": fields.String,
        "confirm_password": fields.String,
    },
)
reset_model = api.model("Reset", {"email": fields.String})
new_password_model = api.model(
    "NewPassword", {"password": fields.String, "confirm_password": fields.String}
)
