import os

from flask import Flask, jsonify, render_template, request, session

from utils import calculate_mel_frequency_cepstral_coefficients, get_prompt


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
    mfccs = calculate_mel_frequency_cepstral_coefficients(
        "static/tmp/tmp.wav", 40)
    print(mfccs)
    print(prompt)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run()
