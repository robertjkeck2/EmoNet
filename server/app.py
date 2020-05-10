import os

from flask import Flask, jsonify, request

from config import BASE_MODEL_PATH
from model import EmoNet

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
model = EmoNet()


@app.route("/api/v1/receive-updates", methods=["POST"])
def receive_updates():
    return jsonify({"success": True})


@app.route("/api/v1/send-model", methods=["POST"])
def send_model():
    device = {
        "net": model.from_file(BASE_MODEL_PATH),
    }
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run()
