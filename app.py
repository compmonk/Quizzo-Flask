from datetime import datetime
from os import error
from pprint import pprint
from MySQLdb.cursors import Cursor

from flask import Flask, jsonify, render_template, request, session, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "5uP3r53Cr3T#"
app.config['MYSQL_HOST'] = '34.93.65.193'
app.config['MYSQL_USER'] = 'db-user'
app.config['MYSQL_PASSWORD'] = 'Pass@123'
app.config['MYSQL_DB'] = 'quizzo'

mysql = MySQL(app)

@app.route("/status")
def status():
    return jsonify({
        "success": True,
        "time": datetime.now().isoformat(),
        "user": session.get("user")
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
                pprint(user)
                session["user"] = {
                    "id": user[0], 
                    "first_name": user[1], 
                    "last_name": user[2], 
                    "email": user[3],
                    "questions_played": user[4],
                    "score": user[5]
                    }
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
            pprint(user)
            if user:
                session["user"] = {
                    "id": user[0], 
                    "first_name": user[1], 
                    "last_name": user[2], 
                    "email": user[3],
                    "questions_played": user[4],
                    "score": user[5]
                    }
            cursor.close()

            return redirect("/game")
        except error:
            return jsonify(error)


@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "GET":
        if session.get("user"):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM questions WHERE id={0}".format(session["user"]["questions_played"] + 1))
            question = cursor.fetchone()
            if question:
                session["question"] = {
                    "id": question[0], 
                    "question": question[1], 
                    "A": question[2], 
                    "B": question[3], 
                    "C": question[4], 
                    "D": question[5], 
                    "answer": question[6]
                    }
            cursor.close()
            return render_template("game.html")
        else:
            return redirect("/login")
    elif request.method == "POST":
        form = request.form
        try:
            # session["user"]["questions_played"] = session["user"]["questions_played"] + 1
            session["user"]["questions_played"] += 1
            session["user"]["score"] += int(form["answer"] == session["question"]["answer"])
            session.modified = True

            cursor = mysql.connection.cursor()
            query = "UPDATE users SET questions_played = {0}, score = {1} WHERE id={2}".format(
                session["user"]["questions_played"],
                session["user"]["score"],
                session["user"]["id"]
                )
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            return redirect("/game")
        except error:
            return jsonify(error)


@app.route("/logout")
def logout():
    if request.method == "GET":
        session["user"] = None
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
