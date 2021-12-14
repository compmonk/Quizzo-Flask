from datetime import datetime
from pprint import pprint

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


@app.route("/status")
def status():
    return jsonify({
        "success": True,
        "time": datetime.now().isoformat()
    })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        pprint(request.form)
        return jsonify(request.form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        pprint(request.form)
        return jsonify(request.form)


@app.route("/game", methods=["GET", "POST"])
def game():
    question = {
        "id": 1,
        "question": "What is the capital of India ?",
        "A": "Delhi",
        "B": "Mumbai",
        "C": "Koklata",
        "D": "Chennai"
    }

    if request.method == "GET":
        return render_template("game.html", question=question)
    elif request.method == "POST":
        pprint(request.form)
        return jsonify(request.form)


if __name__ == "__main__":
    app.run(debug=True)
