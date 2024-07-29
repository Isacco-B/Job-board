from flask_restx import Resource, reqparse
from ..utils.extensions import api

register_schema = reqparse.RequestParser()
register_schema.add_argument(
    "name", type=str, required=True, help="Name is required!"
)
register_schema.add_argument(
    "email", type=str, required=True, help="Email is required!"
)
register_schema.add_argument(
    "password", type=str, required=True, help="Password is required!"
)
register_schema.add_argument(
    "confirm_password", type=str, required=True, help="Confirm Password is required!"
)
