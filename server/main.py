import os

from flask import Flask, jsonify, request, send_from_directory
import numpy as np

from config import BASE_MODEL_PATH, RAVDESS_EMOTION
from model import EmoNet
from utils import average_weights, load_dataset

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')
model = EmoNet()
all_updates = {"updates": []}


@app.route("/api/v1/receive-update", methods=["POST"])
def receive_updates():
    f = request.files.get("file")
    f.save("/tmp/tmp.h5")
    net = model.from_file("/tmp/tmp.h5")
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


@app.route("/api/v1/test-model/<dataset>", methods=["POST"])
def test_model(dataset):
    X_test, _, y_test, _ = load_dataset(40, None, dataset=dataset)
    emonet = model.from_file("data/base_model.h5")
    score, acc = emonet.model.evaluate(X_test, y_test,
                                       batch_size=10)
    return jsonify({"score": score, "acc": acc})


@app.route("/api/v1/predict", methods=["POST"])
def predict():
    request_json = request.get_json()
    raw_mfccs = request_json.get("mfccs")
    emonet = model.from_file("data/base_model.h5")
    mfccs = np.expand_dims(raw_mfccs, axis=0)
    mfccs = np.expand_dims(mfccs, axis=2)
    pred = emonet.predict(mfccs)
    label_input = f"{(pred[0]+1):02d}"
    label = RAVDESS_EMOTION[label_input]
    return jsonify({"label": label, "val": int(pred[0]), "mfccs": raw_mfccs})


if __name__ == "__main__":
    app.run(threaded=False)
