from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "./backend/users.db"

@app.route("/send", methods=["POST"])
def send_money():
    data = request.get_json()
    finger_id = data.get("finger_id")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE finger_id=?", (finger_id,))
    row = cur.fetchone()

    if not row:
        return jsonify({"status": "fail", "message": "User not found"}), 404

    balance = row[0]
    fare = 150

    if balance >= fare:
        new_balance = balance - fare
        cur.execute("UPDATE users SET balance=? WHERE finger_id=?", (new_balance, finger_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "new_balance": new_balance})
    else:
        return jsonify({"status": "fail", "message": "Insufficient balance"})

if __name__ == "__main__":
    app.run(port=8000)
