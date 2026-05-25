from flask import Flask
from config import Config
from database import db

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
from app.routes.auth import register_routes

register_routes(app)

with app.app_context():
    from app.models.user import User
    db.create_all()

@app.route("/")
def home():
    return "BasakWall is running."

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
