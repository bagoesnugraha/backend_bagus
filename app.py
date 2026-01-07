from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH

from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.admin_routes import admin_bp
from app.routes.content_routes import content_bp
from app.routes.petani_ai_routes import petani_ai_bp

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True
    )

    # ===== REGISTER ROUTES =====
    app.register_blueprint(admin_bp, url_prefix="/api/web/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(content_bp, url_prefix="/api/v1")
    app.register_blueprint(petani_ai_bp, url_prefix="/api/v1")  # ✅ INI WAJIB

    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

app = create_app()

if __name__ == "__main__":
    print(f"Server berjalan. Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("-" * 50)
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
