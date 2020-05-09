import os

from flask import Flask, jsonify, render_template, request

from utils.audio import calculate_mel_frequency_cepstral_coefficients


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/v1/process-audio", methods=["POST"])
def process_audio():
    f = request.files.get("audio_data")
    f.save("static/tmp/tmp.wav")
    mfccs = calculate_mel_frequency_cepstral_coefficients("static/tmp/tmp.wav", 40)
    print(mfccs)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run()
