import os

from flask import Flask, jsonify, request, send_from_directory

from config import BASE_MODEL_PATH
from model import EmoNet
from utils import average_weights

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
model = EmoNet()
all_updates = []


@app.route("/api/v1/receive-update", methods=["POST"])
def receive_updates():
    f = request.files.get("file")
    f.save("data/tmp.h5")
    net = model.from_file("data/tmp.h5")
    all_updates.append(net)
    if len(all_updates) > 10:
        w_avg = average_weights(all_updates)
        all_updates = []
        old_net = model.from_file("data/base_model.h5")
        old_net.model.set_weights(w_avg)
        old_net.save("data/base_model.h5")
    return jsonify({"success": True})


@app.route("/api/v1/send-model", methods=["POST"])
def send_model():
    return send_from_directory("data",
                               "base_model.h5", as_attachment=True)


if __name__ == "__main__":
    app.run(port=8000)
