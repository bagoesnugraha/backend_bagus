
import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "project_baru"
}
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}