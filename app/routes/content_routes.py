from flask import Blueprint, jsonify
from app.models.content_model import ContentModel

content_bp = Blueprint('content', __name__)

@content_bp.route('/edukasi', methods=['GET'])
def get_all_edukasi_content():
    data_edukasi = ContentModel.get_contents_mobile()

    return jsonify({
        "message": "Data edukasi berhasil diambil.",
        "data": data_edukasi
    }), 200
