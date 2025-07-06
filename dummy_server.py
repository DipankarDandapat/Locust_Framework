
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({"status": "ok"})

@app.route("/data", methods=["POST"])
def data():
    return jsonify(request.json), 200

@app.route("/")
def homepage():
    return "Welcome to the homepage!"

@app.route("/item")
def item():
    return f"Item ID: {request.args.get("id")}"

@app.route("/about")
def about():
    return "About Us"

@app.route("/contact")
def contact():
    return "Contact Us"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


