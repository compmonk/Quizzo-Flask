from datetime import datetime

from flask import Flask, jsonify, render_template

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



if __name__ == "__main__":
    app.run(debug=True)
