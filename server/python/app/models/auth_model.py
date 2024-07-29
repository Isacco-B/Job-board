from ..utils.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID


class VerificationToken(db.Model):
    id = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(50))
    expires = db.Column(db.DateTime())


class PasswordResetToken(db.Model):
    id = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(50))
    expires = db.Column(db.DateTime())
