from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/api/v1/process-audio/', methods=['POST'])
def process_audio():
    raw_audio = request.form.get('raw_audio')
    if raw_audio:
        return jsonify({
            "success": True,
        })
    else:
        return jsonify({
            "error": "Unable to process audio input."
        })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(threaded=True, port=8000)
