import random, sqlite3, uuid, os
from flask import Flask, render_template, jsonify, request, abort
from config import PRIZES, STAFF_PIN

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'coupons.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS coupons (
            code        TEXT PRIMARY KEY,
            prize_id    TEXT NOT NULL,
            prize_name  TEXT NOT NULL,
            prize_desc  TEXT NOT NULL,
            prize_image TEXT NOT NULL,
            prize_color TEXT NOT NULL,
            used        INTEGER DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

init_db()


@app.route("/")
def index():
    return render_template("index.html", prizes=PRIZES)


@app.route("/spin", methods=["POST"])
def spin():
    weights = [p["weight"] for p in PRIZES]
    result  = random.choices(PRIZES, weights=weights, k=1)[0]

    code = uuid.uuid4().hex[:6].upper()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO coupons (code, prize_id, prize_name, prize_desc, prize_image, prize_color) VALUES (?, ?, ?, ?, ?, ?)",
            (code, result["id"], result["name"], result["description"], result.get("image", ""), result.get("color", "#333"))
        )

    return jsonify({**result, "coupon_code": code})


@app.route("/coupon/<code>")
def coupon_page(code):
    code = code.upper()
    with get_db() as conn:
        coupon = conn.execute(
            "SELECT * FROM coupons WHERE code = ?", (code,)
        ).fetchone()
    if not coupon:
        abort(404)
    return render_template("coupon.html", coupon=coupon)


@app.route("/redeem", methods=["POST"])
def redeem():
    data = request.get_json()
    code = (data.get("code") or "").upper()
    pin  = data.get("pin") or ""

    if pin != STAFF_PIN:
        return jsonify({"success": False, "message": "PINが違います"}), 403

    with get_db() as conn:
        coupon = conn.execute(
            "SELECT * FROM coupons WHERE code = ?", (code,)
        ).fetchone()
        if not coupon:
            return jsonify({"success": False, "message": "無効なコードです"}), 404
        if coupon["used"]:
            return jsonify({"success": False, "message": "このクーポンはすでに使用済みです"}), 409
        conn.execute("UPDATE coupons SET used = 1 WHERE code = ?", (code,))

    return jsonify({"success": True, "message": "受け取り完了！"})


if __name__ == "__main__":
    app.run(debug=True)
