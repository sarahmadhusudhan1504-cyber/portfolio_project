from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)   # 👈 THIS IS THE MAGIC LINE

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/portfolio.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    name = data["name"]
    email = data["email"]
    message = data["message"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
