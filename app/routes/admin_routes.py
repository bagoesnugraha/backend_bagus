
from flask import Blueprint, request, jsonify
from app.utils.jwt_utils import verify_jwt
from app.controller.admin_controller import (
    # FUNGSI USER 
    admin_dashboard,
    admin_get_users,
    admin_get_user_detail,
    admin_create_user,
    admin_update_user,
    
    # FUNGSI KONTEN 
    admin_get_all_contents,
    admin_create_content,
    admin_update_content,
    admin_delete_content,
    
    #  FUNGSI PRODUK
    admin_get_all_products,
    admin_create_product,
    admin_update_product,
    admin_delete_product,
    
    #  UPLOAD GAMBAR 
    admin_upload_product_image 
)

admin_bp = Blueprint("admin_bp", __name__)

def protected(f):
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token tidak ditemukan"}), 401

        decoded = verify_jwt(token)
        if "error" in decoded:
            return jsonify({"message": decoded["error"]}), 401

        if decoded.get("role") != "admin":
            return jsonify({"message": "Akses ditolak"}), 403

        request.user = decoded
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper

admin_bp.route("/dashboard", methods=["GET"])(protected(admin_dashboard))
admin_bp.route("/users", methods=["GET"])(protected(admin_get_users))
admin_bp.route("/users/<int:user_id>", methods=["GET"])(protected(admin_get_user_detail))
admin_bp.route("/users", methods=["POST"])(protected(admin_create_user))
admin_bp.route("/users/<int:user_id>", methods=["PUT"])(protected(admin_update_user))

@admin_bp.route("/contents", methods=["GET", "POST"])
def handle_contents():
    if request.method == "GET":
        return admin_get_all_contents() 
    elif request.method == "POST":
        return admin_create_content() 

# UPDATE CONTENT &  DELETE CONTENT

@admin_bp.route("/contents/<int:content_id>", methods=["PUT", "DELETE"])
def handle_content_by_id(content_id):
    if request.method == "PUT":
        return admin_update_content(content_id) 
    elif request.method == "DELETE":
        return admin_delete_content(content_id)

#  GET ALL PRODUCTS 
@admin_bp.route("/products", methods=["GET", "POST"])
def handle_products():
    if request.method == "GET":
        return admin_get_all_products() 
    elif request.method == "POST":
        return admin_create_product() 

#  UPDATE & DELETE PRODUCT
@admin_bp.route("/products/<int:product_id>", methods=["PUT", "DELETE"])
# @protected # <--- Hapus jika ingin menguji tanpa token
def handle_product_by_id(product_id):
    if request.method == "PUT":
        return admin_update_product(product_id) 
    elif request.method == "DELETE":
        return admin_delete_product(product_id) 

# 5. UPLOAD GAMBAR PRODUK
@admin_bp.route("/products/<int:product_id>/image", methods=["POST"])
# @protected # <--- Hapus jika ingin menguji tanpa token
def handle_product_image_upload(product_id):
    return admin_upload_product_image(product_id)