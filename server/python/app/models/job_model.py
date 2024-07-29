from ..utils.extensions import db
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID


class Job(db.Model):
    id = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    company = db.Column(db.String(50))
    location = db.Column(db.String(50))
    salary = db.Column(db.Integer)
    remote = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user_id = db.Column(
        SQLAlchemyUUID(as_uuid=True), db.ForeignKey("user.id", ondelete="CASCADE")
    )
