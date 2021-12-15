from datetime import datetime
from os import error
from pprint import pprint
from MySQLdb.cursors import Cursor

from flask import Flask, jsonify, render_template, request, session, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

#  Do not change
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
        "time": datetime.now().isoformat()
    })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    pass


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
    pass

@app.route("/leaderboard")
def leaderboard():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY score DESC, questions_played")
    scores = []
    for user in cursor.fetchall():
        scores.append({
            "name": "{} {}".format(user[1], user[2]),
            "email": user[3],
            "questions_played": user[4],
            "score": user[5],
            "total": round(user[5] / user[4] * 100.0, 2)
        })
    return render_template("leaderboard.html", scores=scores)


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
