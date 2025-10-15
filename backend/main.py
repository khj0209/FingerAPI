from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "./backend/users.db"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    phone_last4 = data.get("phone_last4")
    finger_id = data.get("finger_id")
    
    if not phone_last4 or not finger_id:
        return jsonify({"status": "fail", "message": "Phone last 4 digits and finger ID required"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check if finger_id already exists
    cur.execute("SELECT finger_id FROM users WHERE finger_id=?", (finger_id,))
    if cur.fetchone():
        conn.close()
        return jsonify({"status": "fail", "message": "User already exists"}), 409
    
    # Insert new user with initial balance 0
    cur.execute("INSERT INTO users (finger_id, phone_last4, balance) VALUES (?, ?, ?)", 
                (finger_id, phone_last4, 0))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": f"{phone_last4}님 환영합니다!"})

@app.route("/balance", methods=["POST"])
def check_balance():
    data = request.get_json()
    finger_id = data.get("finger_id")
    
    if not finger_id:
        return jsonify({"status": "fail", "message": "Finger ID required"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE finger_id=?", (finger_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"status": "fail", "message": "User not found"}), 404
    
    balance = row[0]
    return jsonify({"status": "success", "balance": balance})

@app.route("/charge", methods=["POST"])
def charge_balance():
    data = request.get_json()
    phone_last4 = data.get("phone_last4")
    finger_id = data.get("finger_id")
    amount = data.get("amount")
    
    if not phone_last4 or not finger_id or not amount:
        return jsonify({"status": "fail", "message": "Phone last 4 digits, finger ID and amount required"}), 400
    
    if amount <= 0:
        return jsonify({"status": "fail", "message": "Amount must be positive"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check if user exists and phone_last4 matches
    cur.execute("SELECT balance FROM users WHERE finger_id=? AND phone_last4=?", (finger_id, phone_last4))
    row = cur.fetchone()
    
    if not row:
        conn.close()
        return jsonify({"status": "fail", "message": "User not found or phone number doesn't match"}), 404
    
    current_balance = row[0]
    new_balance = current_balance + amount
    
    cur.execute("UPDATE users SET balance=? WHERE finger_id=?", (new_balance, finger_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "new_balance": new_balance, "message": f"충전된 잔액: {new_balance:,}원"})

@app.route("/send", methods=["POST"])
def send_money():
    data = request.get_json()
    finger_id = data.get("finger_id")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT phone_last4, balance FROM users WHERE finger_id=?", (finger_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"status": "fail", "message": "User not found"}), 404

    phone_last4, balance = row
    fare = 150

    if balance >= fare:
        new_balance = balance - fare
        cur.execute("UPDATE users SET balance=? WHERE finger_id=?", (new_balance, finger_id))
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success", 
            "new_balance": new_balance,
            "message": f"{phone_last4}님 잔액은 {new_balance:,}원입니다!"
        })
    else:
        conn.close()
        return jsonify({"status": "fail", "message": "Insufficient balance"})

if __name__ == "__main__":
    app.run(port=8000)
