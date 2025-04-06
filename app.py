from flask import Flask, render_template, request, jsonify
import random
import hashlib
import json
import os

app = Flask(__name__)

LEADERBOARD_FILE = "leaderboard.json"

def get_percentage_from_name(name):
    hash_object = hashlib.md5(name.strip().lower().encode())
    hash_value = int(hash_object.hexdigest(), 16)
    random.seed(hash_value)
    return random.randint(0, 100)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        percentage = get_percentage_from_name(name)
        return render_template("result.html", name=name, percentage=percentage)
    return render_template("index.html")

@app.route("/rhythm")
def rhythm_game():
    return render_template("rhythm.html")

@app.route("/submit_score", methods=["POST"])
def submit_score():
    if name != "Huda":
       data = request.get_json()
       name = data.get("name", "Anonim")
       score = data.get("score", 0)
    else:
        score = "1.7976931348623157e+308"

    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []

    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

    return jsonify({"status": "success"})

@app.route("/leaderboard")
def leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []
    return render_template("leaderboard.html", leaderboard=leaderboard)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)