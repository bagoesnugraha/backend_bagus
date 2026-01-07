from flask import Blueprint, request, jsonify
import requests
import os

petani_ai_bp = Blueprint("petani_ai", __name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@petani_ai_bp.route("/petani-ai", methods=["POST"])
def petani_ai_chat():
    # 1️⃣ Validasi API key
    if not OPENROUTER_API_KEY:
        return jsonify({
            "error": "API key OpenRouter belum diset"
        }), 500

    # 2️⃣ Ambil pesan user
    data = request.get_json()
    message = data.get("message") if data else None

    if not message:
        return jsonify({
            "error": "Pesan tidak boleh kosong"
        }), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Agriminds Petani AI"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah Petani AI, asisten ahli pertanian dan beras. "
                    "Jawab pertanyaan dengan bahasa sederhana dan mudah dipahami petani."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        # 3️⃣ Cek status OpenRouter
        if response.status_code != 200:
            return jsonify({
                "error": "Gagal mendapatkan respon dari AI",
                "detail": response.text
            }), 500

        result = response.json()

        # 4️⃣ Validasi isi response
        if "choices" not in result or not result["choices"]:
            return jsonify({
                "error": "Respon AI tidak valid"
            }), 500

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Terjadi kesalahan koneksi ke AI",
            "detail": str(e)
        }), 500
