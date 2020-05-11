import logging
import os

from flask import Flask, jsonify, render_template, request, session
import numpy as np

from config import RAVDESS_EMOTION
from utils import (
    calculate_mel_frequency_cepstral_coefficients,
    get_net_from_server,
    get_prompt,
    send_update_to_server
)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')

@app.route("/", methods=["GET"])
def index():
    session["prompt"] = get_prompt()
    return render_template("index.html", prompt=session["prompt"].get("emotion"))


@app.route("/api/v1/process-audio", methods=["POST"])
def process_audio():
    f = request.files.get("audio_data")
    f.save("/tmp/tmp.wav")
    prompt = session.pop("prompt", None)
    mfccs = [calculate_mel_frequency_cepstral_coefficients(
        "/tmp/tmp.wav", 40)]
    val = prompt.get("val")
    if len(mfccs) > 0 and val:
        logging.info(mfccs)
        mfccs = np.expand_dims(np.asarray(mfccs), axis=2)
        val = np.asarray([prompt.get("val")])
    net = get_net_from_server()
    net.fit(mfccs, None, val, None, 1, 1)
    send_update_to_server(net)
    return jsonify({"success": True})

@app.route("/api/v1/predict", methods=["POST"])
def predict():
    f = request.files.get("audio_data")
    f.save("/tmp/tmp_pred.wav")
    mfccs = [calculate_mel_frequency_cepstral_coefficients(
        "/tmp/tmp_pred.wav", 40)]
    if len(mfccs) > 0:
        logging.info(mfccs)
        mfccs = np.expand_dims(np.asarray(mfccs), axis=2)
    net = get_net_from_server()
    print(net.model.get_weights())
    pred = net.predict(mfccs)
    label_input = f"{(pred[0]+1):02d}"
    label = RAVDESS_EMOTION[label_input]
    return label

if __name__ == "__main__":
    app.run(threaded=False)
