from flask import session, redirect, render_template
from database import db
from app.models.notification import Notification
from app.models.comment import Comment
from app.models.user import User


def create_notification(
    user_id,
    actor_id,
    notification_type,
    target_type,
    target_id,
    message
):

    if user_id == actor_id:
        return

    existing_notification = Notification.query.filter_by(
        user_id=user_id,
        actor_id=actor_id,
        notification_type=notification_type,
        target_type=target_type,
        target_id=target_id
    ).first()

    if existing_notification:
        return

    notification = Notification(
        user_id=user_id,
        actor_id=actor_id,
        notification_type=notification_type,
        target_type=target_type,
        target_id=target_id,
        message=message
    )

    db.session.add(notification)


def delete_notification(
    user_id,
    actor_id,
    notification_type,
    target_type,
    target_id
):

    notification = Notification.query.filter_by(
        user_id=user_id,
        actor_id=actor_id,
        notification_type=notification_type,
        target_type=target_type,
        target_id=target_id
    ).first()

    if notification:
        db.session.delete(notification)


def get_unread_notification_count(user_id):

    return Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).count()


def register_notification_routes(app):

    @app.route("/notifications")
    def notifications():

        if "user_id" not in session:
            return redirect("/login")

        notifications = Notification.query.filter_by(
            user_id=session["user_id"]
        ).order_by(
            Notification.created_at.desc()
        ).all()

        unread_count = get_unread_notification_count(
            session["user_id"]
        )

        return render_template(
            "notifications.html",
            notifications=notifications,
            unread_count=unread_count
        )


    @app.route("/notifications/read-all")
    def read_all_notifications():

        if "user_id" not in session:
            return redirect("/login")

        notifications = Notification.query.filter_by(
            user_id=session["user_id"],
            is_read=False
        ).all()

        for notification in notifications:
            notification.is_read = True

        db.session.commit()

        return redirect("/notifications")


    @app.route("/notifications/<int:notification_id>/open")
    def open_notification(notification_id):

        if "user_id" not in session:
            return redirect("/login")

        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=session["user_id"]
        ).first()

        if not notification:
            return "Notification not found", 404

        notification.is_read = True
        db.session.commit()

        if notification.target_type == "post":
            return redirect(f"/posts/{notification.target_id}")

        if notification.target_type == "comment":
            comment = Comment.query.get(notification.target_id)

            if comment:
                return redirect(
                    f"/posts/{comment.post_id}#comment-{comment.id}"
                )

            return redirect("/notifications")

        if notification.target_type == "user":
            actor = User.query.get(notification.actor_id)

            if actor:
                return redirect(f"/profile/{actor.username}")

            return redirect("/notifications")

        return redirect("/notifications")