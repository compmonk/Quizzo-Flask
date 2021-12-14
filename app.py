from datetime import datetime

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


@app.route("/login")
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        pass


@app.route("/signup")
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        pass


if __name__ == "__main__":
    app.run(debug=True)
