import os

from flask import Flask, jsonify, render_template, request, session
import numpy as np

from utils import (
    calculate_mel_frequency_cepstral_coefficients,
    get_net_from_server,
    get_prompt,
    send_update_to_server
)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    session["prompt"] = get_prompt()
    return render_template("index.html", prompt=session["prompt"].get("emotion"))


@app.route("/api/v1/process-audio", methods=["POST"])
def process_audio():
    f = request.files.get("audio_data")
    f.save("static/tmp/tmp.wav")
    prompt = session.pop("prompt", None)
    mfccs = [calculate_mel_frequency_cepstral_coefficients(
        "static/tmp/tmp.wav", 40)]
    val = prompt.get("val")
    if len(mfccs) > 0 and val:
        mfccs = np.expand_dims(np.asarray(mfccs), axis=2)
        val = np.asarray([prompt.get("val")])
    net = get_net_from_server()
    net.fit(mfccs, None, val, None, 1, 1)
    send_update_to_server(net)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(threaded=False)
