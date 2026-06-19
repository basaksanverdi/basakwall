from database import db
from datetime import datetime, timezone


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    notification_type = db.Column(
        db.String(50),
        nullable=False
    )

    target_type = db.Column(
        db.String(50),
        nullable=False
    )

    target_id = db.Column(
        db.Integer,
        nullable=False
    )

    message = db.Column(
        db.String(255),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[user_id]
    )

    actor = db.relationship(
        "User",
        foreign_keys=[actor_id]
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "actor_id",
            "notification_type",
            "target_type",
            "target_id",
            name="unique_notification"
        ),
    )