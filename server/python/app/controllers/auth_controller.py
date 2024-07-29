from flask_restx import Resource, Namespace
from ..serializers.auth_serializer import login_model, register_model
from ..serializers.user_serializer import user_model
from ..models.user_model import User, Profile
from ..utils.extensions import db

api = Namespace("api/auth", description="Auth related operations")


@api.route("/sign-up")
class RegisterApi(Resource):
    @api.expect(register_model)
    def post(self):
        user = User(name=api.payload["name"], email=api.payload["email"]) # type: ignore
        user.set_password(api.payload["password"])
        db.session.add(user)
        db.session.commit()
        return { "message": "user created" }, 201


@api.route("/sign-in")
class LoginApi(Resource):
    @api.expect(login_model)
    def post(self):
        pass


@api.route("/logout")
class LogoutApi(Resource):
    def post(self):
        pass


@api.route("/refresh")
class RefreshApi(Resource):
    def get(self):
        pass


@api.route("/reset")
class ResetApi(Resource):
    def post(self):
        pass


@api.route("/new-password/<token>")
class NewPasswordApi(Resource):
    def post(self):
        pass


@api.route("/new-verification/<token>")
class NewVerificationApi(Resource):
    def post(self):
        pass
