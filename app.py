import random
from flask import Flask, render_template, jsonify
from config import PRIZES

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", prizes=PRIZES)


@app.route("/spin", methods=["POST"])
def spin():
    weights = [p["weight"] for p in PRIZES]
    result  = random.choices(PRIZES, weights=weights, k=1)[0]
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
