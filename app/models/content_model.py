# File: app/models/content_model.py
# Final Version with Raw SQL + Mobile Support

from app.db import get_db_connection
from datetime import datetime


class ContentModel:

    # =========================
    # Helper Query Executor
    # =========================
    @staticmethod
    def execute_query(query, values=None, fetch_all=False, commit=False):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            if commit:
                db.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                return cursor.rowcount
            else:
                data = cursor.fetchall() if fetch_all else cursor.fetchone()
                return data
        finally:
            cursor.close()
            db.close()

    # =========================
    # Helper: Get Content by ID
    # =========================
    @staticmethod
    def get_content_by_id(content_id):
        query = """
            SELECT 
                id, title, author, category, status, 
                published_at, content 
            FROM contents 
            WHERE id = %s
        """
        return ContentModel.execute_query(query, (content_id,), fetch_all=False)

    # =========================
    # 1. READ ALL (ADMIN)
    # =========================
    @staticmethod
    def get_all_contents():
        query = """
            SELECT 
                id, title, author, category, status, published_at 
            FROM contents 
            ORDER BY created_at DESC
        """
        contents = ContentModel.execute_query(query, fetch_all=True)
        return contents or []

    # =========================
    # 2. CREATE (ADMIN)
    # =========================
    @staticmethod
    def create_content(data):
        query = """
            INSERT INTO contents 
                (title, author, category, description, content, status, published_at)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('title'),
            data.get('author'),
            data.get('category'),
            data.get('description', ''),
            data.get('body', ''),
            data.get('status', 'Draft'),
            data.get('published_at')
        )

        last_id = ContentModel.execute_query(query, values, commit=True)

        if last_id:
            return ContentModel.get_content_by_id(last_id)
        return None

    # =========================
    # 3. UPDATE (ADMIN)
    # =========================
    @staticmethod
    def update_content(content_id, data):
        query = """
            UPDATE contents SET 
                title = %s,
                author = %s,
                category = %s,
                description = %s,
                content = %s,
                status = %s,
                published_at = %s,
                updated_at = NOW()
            WHERE id = %s
        """
        values = (
            data.get('title'),
            data.get('author'),
            data.get('category'),
            data.get('description', ''),
            data.get('body', ''),
            data.get('status', 'Draft'),
            data.get('published_at'),
            content_id
        )

        return ContentModel.execute_query(query, values, commit=True)

    # =========================
    # 4. DELETE (ADMIN)
    # =========================
    @staticmethod
    def delete_content(content_id):
        query = "DELETE FROM contents WHERE id = %s"
        return ContentModel.execute_query(query, (content_id,), commit=True)

    # =========================
    # 5. READ FOR MOBILE (PUBLIC)
    # =========================
    @staticmethod
    def get_contents_mobile():
        query = """
            SELECT 
                id,
                title,
                description,
                content,
                author,
                category,
                published_at
            FROM contents
            WHERE status = 'Published'
            ORDER BY published_at DESC
        """
        contents = ContentModel.execute_query(query, fetch_all=True)
        return contents or []
