# File: app/controller/admin_controller.py (FINAL GABUNGAN + PRODUK/UPLOAD)

# --- IMPOR FLASK DASAR DAN UPLOAD ---
from flask import jsonify, request, current_app 
from werkzeug.utils import secure_filename 
import os 
from datetime import datetime 
import bcrypt

# --- IMPOR MODEL ---
from app.models.user_model import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user
)
from app.models.content_model import ContentModel 
from app.models.product_model import ProductModel # <-- MODEL PRODUK

# ================================
# 🖼️ HELPER FUNCTION UNTUK UPLOAD 🖼️
# ================================
def allowed_file(filename):
    """Memeriksa apakah ekstensi file diizinkan berdasarkan config"""
    # Mengakses config dari app.py
    if 'ALLOWED_EXTENSIONS' not in current_app.config:
        return False
        
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# ================================
# DASHBOARD ADMIN (TELAH DIKOREKSI + DEBUGGING)
# ================================
def admin_dashboard():
    try:
        # 1. Hitung Total User
        users = get_all_users()
        total_users = len(users)
        
        # 2. Hitung Total Konten
        contents = ContentModel.get_all_contents() 
        total_contents = len(contents)
        
        # 🚨 BARIS DEBUGGING BARU 🚨
        print(f"DEBUG: Data contents dari model (len): {total_contents}")
        # 🚨 AKHIR BARIS DEBUGGING 🚨
        
        # 3. Hitung AR Users (Asumsi 0 atau dihitung secara terpisah)
        total_ar_users = 0 
        
        # Logika Produk DIHILANGKAN dari dashboard
        
        return jsonify({
            "success": True,
            "message": "Dashboard admin loaded",
            "total_users": total_users,
            "total_contents": total_contents, # <-- Data Konten yang Hilang KINI ADA
            "total_ar_users": total_ar_users
        }), 200

    except Exception as e:
        # Menangani kegagalan koneksi database atau error model
        return jsonify({
            "success": False, 
            "message": f"Gagal memuat data dashboard: {str(e)}"
        }), 500
        
# ... (Sisa fungsi CRUD User, Konten, Produk, dan Upload Image tetap sama) ...
# ================================
# ✅ FUNGSI ADMIN USER (CRUD) ✅
# ================================
def admin_get_users():
    try:
        users = get_all_users() 
        return jsonify({"success": True, "data": users}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal mengambil daftar pengguna: {str(e)}"}), 500

def admin_get_user_detail(user_id):
    try:
        user = get_user_by_id(user_id) 
        if user:
            return jsonify({"success": True, "data": user}), 200
        else:
            return jsonify({"success": False, "message": "Pengguna tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def admin_create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user') 
    
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Data wajib (username, email, password) tidak lengkap."}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        create_user(username, email, hashed_password, role) 
        return jsonify({"success": True, "message": "Pengguna berhasil dibuat"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 409

def admin_update_user(user_id):
    data = request.get_json()
    
    if 'password' in data and data['password']:
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        rows = update_user(user_id, **data) 
        if rows > 0:
            updated_user = get_user_by_id(user_id) 
            return jsonify({"success": True, "message": "Pengguna berhasil diperbarui", "data": updated_user}), 200
        else:
            return jsonify({"success": False, "message": "User tidak ditemukan atau tidak ada perubahan"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ================================
# 🚀 API UNTUK MANAJEMEN KONTEN 🚀
# ================================

def admin_get_all_contents():
    try:
        contents = ContentModel.get_all_contents()
        return jsonify({"success": True, "data": contents}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal mengambil data konten: {str(e)}"}), 500

def admin_create_content():
    data = request.get_json()
    if not data.get('title') or not data.get('author') or not data.get('published_at') or not data.get('body'):
        return jsonify({"success": False, "message": "Judul, Penulis, Isi Konten, dan Tanggal Terbit wajib diisi."}), 400
        
    try:
        new_content_data = ContentModel.create_content(data)
        if new_content_data:
            return jsonify({"success": True, "message": "Konten berhasil dibuat", "data": new_content_data}), 201
        else:
            return jsonify({"success": False, "message": "Konten gagal dibuat (ID tidak ditemukan setelah INSERT)."}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal membuat konten: {str(e)}. Periksa format data."}), 500

def admin_update_content(content_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Tidak ada data yang dikirim"}), 400
    try:
        rows_affected = ContentModel.update_content(content_id, data)
        if rows_affected > 0:
            return jsonify({"success": True, "message": "Konten berhasil diperbarui"}), 200
        else:
            return jsonify({"success": False, "message": "Konten tidak ditemukan atau tidak ada perubahan"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal memperbarui konten: {str(e)}"}), 500

def admin_delete_content(content_id):
    try:
        rows_affected = ContentModel.delete_content(content_id)
        if rows_affected > 0:
            return jsonify({"success": True, "message": "Konten berhasil dihapus"}), 204
        else:
            return jsonify({"success": False, "message": "Konten tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal menghapus konten: {str(e)}"}), 500


# ================================
# 📦 API UNTUK MANAJEMEN PRODUK (KATALOG/PENJELASAN) 📦
# ================================
def admin_get_all_products():
    try:
        products = ProductModel.get_all_products()
        return jsonify({"success": True, "data": products}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal mengambil data katalog: {str(e)}"}), 500

def admin_create_product():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('description'):
        return jsonify({"success": False, "message": "Nama dan Penjelasan wajib diisi."}), 400
        
    try:
        new_product_data = ProductModel.create_product(data)
        if new_product_data:
            return jsonify({"success": True, "message": "Item Katalog berhasil dibuat", "data": new_product_data}), 201
        else:
            return jsonify({"success": False, "message": "Item Katalog gagal dibuat (DB error)."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal membuat Item Katalog: {str(e)}"}), 500

def admin_update_product(product_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Tidak ada data yang dikirim"}), 400

    try:
        rows_affected = ProductModel.update_product(product_id, data)
        if rows_affected > 0:
            updated_product = ProductModel.get_product_by_id(product_id)
            return jsonify({"success": True, "message": "Item Katalog berhasil diperbarui", "data": updated_product}), 200
        else:
            return jsonify({"success": False, "message": "Item Katalog tidak ditemukan atau tidak ada perubahan"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal memperbarui Item Katalog: {str(e)}"}), 500

def admin_delete_product(product_id):
    try:
        rows_affected = ProductModel.delete_product(product_id)
        if rows_affected > 0:
            return jsonify({"success": True, "message": "Item Katalog berhasil dihapus"}), 204
        else:
            return jsonify({"success": False, "message": "Item Katalog tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal menghapus Item Katalog: {str(e)}"}), 500

def admin_upload_product_image(product_id):
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Tidak ada file"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "message": "Tidak ada file yang dipilih"}), 400
        
    if file and allowed_file(file.filename):
        product = ProductModel.get_product_by_id(product_id)
        if not product:
            return jsonify({"success": False, "message": "Produk tidak ditemukan, tidak bisa upload."}), 404

        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"product_{product_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            file.save(save_path)
            public_url = f"/static/uploads/{unique_filename}" 
            
            # Update database
            ProductModel.update_product_image_url(product_id, public_url)
            
            return jsonify({
                "success": True, 
                "message": "Gambar berhasil diunggah", 
                "image_url": public_url
            }), 200
            
        except Exception as e:
            return jsonify({"success": False, "message": f"Gagal menyimpan: {str(e)}"}), 500
            
    else:
        return jsonify({"success": False, "message": "Tipe file tidak diizinkan"}), 400