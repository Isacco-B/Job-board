from ..utils.extensions import db
import enum
import uuid
import bcrypt
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from .job_model import Job


class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class User(db.Model):
    """User Model for storing user related details"""

    __tablename__ = "user"
    id = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_verified = db.Column(db.DateTime())
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    profile = db.relationship(
        "Profile", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    jobs = db.relationship(Job, backref="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10))

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def __repr__(self):
        return f"User(name={self.name!r}, email={self.email!r})"


class Profile(db.Model):
    """Profile Model for storing user profile details"""

    __tablename__ = "profile"
    id = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        SQLAlchemyUUID(as_uuid=True),
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    profile_picture = db.Column(db.String())
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime())
    gender = db.Column(db.Enum(Gender))
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
