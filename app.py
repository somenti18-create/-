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
            coupon_url  TEXT NOT NULL DEFAULT '',
            used        INTEGER DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        # 旧DBにcoupon_urlカラムがなければ追加
        cols = [row[1] for row in conn.execute("PRAGMA table_info(coupons)")]
        if 'coupon_url' not in cols:
            conn.execute("ALTER TABLE coupons ADD COLUMN coupon_url TEXT NOT NULL DEFAULT ''")

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
            "INSERT INTO coupons (code, prize_id, prize_name, prize_desc, prize_image, prize_color, coupon_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (code, result["id"], result["name"], result["description"], result.get("image", ""), result.get("color", "#333"), result.get("coupon_url", ""))
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
