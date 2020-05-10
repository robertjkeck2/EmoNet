import os

from flask import Flask, jsonify, request, send_from_directory

from config import BASE_MODEL_PATH
from model import EmoNet
from utils import average_weights, load_dataset

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


@app.route("/api/v1/test-model", methods=["POST"])
def test_model():
    X_test, _, y_test, _ = load_dataset(40, None, dataset="SAVEE")
    emonet = model.from_file("data/base_model.h5")
    score, acc = emonet.model.evaluate(X_test, y_test,
                                       batch_size=10)
    return jsonify({"score": score, "acc": acc})


if __name__ == "__main__":
    app.run(threaded=False, port=8000)
