# File: app/models/product_model.py (FINAL SKEMA NON-JUALAN)

from app.db import get_db_connection 
from datetime import datetime
import mysql.connector 

# --- Helper Query Execution (Biarkan fungsi ini jika sudah bekerja) ---
def execute_query(query, values=None, fetch_all=False, commit=False):
    # ... (Sama seperti kode Anda sebelumnya untuk koneksi dan eksekusi) ...
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        if commit:
            conn.commit()
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            return cursor.rowcount 
        else:
            data = cursor.fetchall() if fetch_all else cursor.fetchone()
            return data
            
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        if conn and commit:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# --- Model Kelas Produk (Katalog/Penjelasan) ---
class ProductModel:

    # Kolom disesuaikan dengan skema database (tanpa price, stock, unit)
    PRODUCT_FIELDS = "id, name, category, status, description, image_url, created_at"

    # 1. READ ALL PRODUCTS
    @staticmethod
    def get_all_products():
        query = f"SELECT {ProductModel.PRODUCT_FIELDS} FROM products ORDER BY created_at DESC"
        products = execute_query(query, fetch_all=True)
        return products or []

    # Helper: Get One Product
    @staticmethod
    def get_product_by_id(product_id):
        query = f"SELECT {ProductModel.PRODUCT_FIELDS} FROM products WHERE id = %s"
        return execute_query(query, (product_id,), fetch_all=False)

    # 2. CREATE PRODUCT (TAMBAH)
    @staticmethod
    def create_product(data):
        query = """
            INSERT INTO products (name, category, description, status)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            data.get('name'), 
            data.get('category', 'Umum'),
            data.get('description', ''),
            data.get('status', 'Draft')
        )
        
        last_id = execute_query(query, values, commit=True)
        
        if last_id:
            return ProductModel.get_product_by_id(last_id)
        return None

    # 3. UPDATE PRODUCT (EDIT) - VERSI KOREKSI DINAMIS
    @staticmethod
    def update_product(product_id, data):
        fields = []
        values = []

        # Mapping field frontend ke kolom DB (HANYA KOLOM YANG ADA)
        field_mapping = {
            'name': 'name',
            'category': 'category',
            'description': 'description',
            'status': 'status',
        }

        for frontend_key, db_column in field_mapping.items():
            if frontend_key in data:
                fields.append(f"{db_column} = %s")
                values.append(data[frontend_key])

        if not fields:
            return 0 

        fields.append("updated_at = NOW()") 
        values.append(product_id)
        
        sql = f"UPDATE products SET {', '.join(fields)} WHERE id=%s"
        return execute_query(sql, tuple(values), commit=True)


    # 4. DELETE PRODUCT (HAPUS)
    @staticmethod
    def delete_product(product_id):
        query = "DELETE FROM products WHERE id = %s"
        return execute_query(query, (product_id,), commit=True)

    # 5. UPDATE IMAGE URL (Digunakan oleh Controller Upload)
    @staticmethod
    def update_product_image_url(product_id, image_url):
        query = """
            UPDATE products SET 
                image_url = %s, updated_at = NOW()
            WHERE id = %s
        """
        return execute_query(query, (image_url, product_id), commit=True)