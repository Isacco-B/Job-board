from flask_restx import fields
from ..utils.extensions import api


login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)
register_model = api.model(
    "Register",
    {
        "name": fields.String(required=True, description="User name"),
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
        "confirm_password": fields.String(
            required=True, description="Confirm user password"
        ),
    },
)
reset_model = api.model(
    "Reset", {"email": fields.String(required=True, description="User email")}
)
new_password_model = api.model(
    "NewPassword",
    {
        "password": fields.String(required=True, description="User password"),
        "confirm_password": fields.String(
            required=True, description="Confirm user password"
        ),
    },
)
