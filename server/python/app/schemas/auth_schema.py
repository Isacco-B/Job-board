from marshmallow import Schema, fields, ValidationError, validate, validates_schema

password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$"


class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.Length(min=1, error="Email cannot be empty"),
        error_messages={"required": "Email is required", "invalid": "Invalid email"},
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Password cannot be empty"),
        error_messages={"required": "Password is required"},
    )


class RegisterSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Name cannot be empty"),
        error_messages={"required": "Name is required"},
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(min=1, error="Email cannot be empty"),
        error_messages={"required": "Email is required", "invalid": "Invalid email"},
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Regexp(
                password_regex,
                error="Password must contain at least one uppercase letter, one lowercase letter, one number, one special character and between 8 and 24 characters",
            ),
        ],
        error_messages={"required": "Password is required"},
    )
    confirm_password = fields.Str(
        required=True, error_messages={"required": "Confirm password is required"}
    )

    @validates_schema
    def validate_confirm_password(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError(
                "Passwords do not match", field_names=["confirm_password"]
            )


class ResetSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.Length(min=1, error="Email cannot be empty"),
        error_messages={"required": "Email is required", "invalid": "Invalid email"},
    )


class NewPasswordSchema(Schema):
    password = fields.Str(
        required=True,
        validate=[
            validate.Regexp(
                password_regex,
                error="Password must contain at least one uppercase letter, one lowercase letter, one number, one special character and between 8 and 24 characters",
            ),
        ],
        error_messages={"required": "Password is required"},
    )
    confirm_password = fields.Str(
        required=True, error_messages={"required": "Confirm password is required"}
    )

    @validates_schema
    def validate_confirm_password(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError(
                "Passwords do not match", field_names=["confirm_password"]
            )
