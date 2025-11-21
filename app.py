from flask import Flask
from flask_cors import CORS
from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp
from app.routes.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Tambahkan URL prefix
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
