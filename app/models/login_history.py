from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class LoginHistory(db.Model):

    __tablename__ = "login_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    login_time = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Europe/Istanbul")
        )
    )

    logout_time = db.Column(
        db.DateTime,
        nullable=True
    )

    ip_address = db.Column(
        db.String(100),
        nullable=True
    )

    user = db.relationship(
        "User",
        backref="login_history"
    )