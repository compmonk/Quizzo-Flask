from datetime import datetime
from os import error
from pprint import pprint
from MySQLdb.cursors import Cursor

from flask import Flask, jsonify, render_template, request, session
from flask_mysqldb import MySQL
from werkzeug.utils import redirect


app = Flask(__name__)
app.secret_key = "5uP3r53Cr3T#"
app.config['MYSQL_HOST'] = '34.93.65.193'
app.config['MYSQL_USER'] = 'db-user'
app.config['MYSQL_PASSWORD'] = 'Pass@123'
app.config['MYSQL_DB'] = 'quizzo'

mysql = MySQL(app)


question = {
    "id": 1,
    "question": "What is the capital of India ?",
    "A": "Delhi",
    "B": "Mumbai",
    "C": "Koklata",
    "D": "Chennai"
}

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
        form = request.form
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email='{0}'".format(form.get("email", "")))
            user = cursor.fetchone()
            if user:
                session["user"] = {"id": user[0], "first_name": user[1], "last_name": user[2], "email": user[3]}
            cursor.close()

            return redirect("/game")
        except error:
            return jsonify(error)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        form = request.form
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email) VALUES ('{0}', '{1}', '{2}')".format(
                form.get("first_name", ""), 
                form.get("last_name", ""), 
                form.get("email", "")))
            mysql.connection.commit()

            cursor.execute("SELECT * FROM users WHERE email='{0}'".format(form.get("email", "")))
            user = cursor.fetchone()
            if user:
                session["user"] = {"id": user[0], "first_name": user[1], "last_name": user[2], "email": user[3]}
            cursor.close()

            return redirect("/game")
        except error:
            return jsonify(error)


@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "GET":
        if session.get("user"):
            return render_template("game.html", question=question)
        else:
            return redirect("/login")
    elif request.method == "POST":
        pprint(request.form)
        return jsonify(request.form)


@app.route("/logout")
def logout():
    if request.method == "GET":
        session["user"] = None
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
