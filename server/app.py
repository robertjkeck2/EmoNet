import os

from flask import Flask, jsonify, request

from model import EmoNet

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
model = EmoNet()


@app.route("/api/v1/receive-updates", methods=["POST"])
def receive_updates():
    return jsonify({"success": True})


@app.route("/api/v1/send-model", methods=["POST"])
def send_model():
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run()
