from flask import Flask, render_template, request
import random
import hashlib

app = Flask(__name__)

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

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
