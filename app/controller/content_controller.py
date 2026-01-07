from flask import jsonify
from app.models.content_model import ContentModel

def get_content_mobile():
    data = ContentModel.get_contents_mobile()
    return jsonify({
        "status": "success",
        "data": data
    }), 200
