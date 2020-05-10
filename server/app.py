import os

from flask import Flask, jsonify, request, send_from_directory

from config import BASE_MODEL_PATH
from model import EmoNet
from utils import average_weights

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
model = EmoNet()
all_updates = {"updates": []}


@app.route("/api/v1/receive-update", methods=["POST"])
def receive_updates():
    f = request.files.get("file")
    f.save("data/tmp.h5")
    net = model.from_file("data/tmp.h5")
    all_updates["updates"].append(net)
    if len(all_updates["updates"]) > 10:
        w_avg = average_weights(all_updates["updates"])
        all_updates["updates"] = []
        old_net = model.from_file("data/base_model.h5")
        old_net.model.set_weights(w_avg)
        old_net.save("data/base_model.h5")
    return jsonify({"success": True})


@app.route("/api/v1/send-model", methods=["POST"])
def send_model():
    return send_from_directory("data",
                               "base_model.h5", as_attachment=True)


if __name__ == "__main__":
    app.run(threaded=False, port=8000)
