from flask import Flask
from flask_cors import CORS
from app.db import get_db_connection
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "rahasia_banget_bagus"

    # Aktifkan CORS supaya HP & Laptop bisa akses
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Test database connection
    try:
        conn = get_db_connection()
        conn.close()
        print("Database Connected!")
    except Exception as e:
        print("Database Error:", e)

    # Register routes
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
