from flask import Flask, render_template, request, send_from_directory, url_for
from FileHandler import FileHandler
import json
import os
from werkzeug.datastructures import FileStorage


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('speechRecognition.html')


@app.route('/asr/', methods=['POST'])
def asr():
    res = []
    for f in request.files:
        if f.startswith('audio_blob') and FileHandler.check_format(request.files[f]):

            response_code, filename, response = FileHandler.get_recognized_text(request.files[f])

            if response_code == 0:
                response_audio_url = url_for('media_file', filename=filename)
            else:
                response_audio_url = None

            res.append({
                'response_audio_url': response_audio_url,
                'response_code': response_code,
                'response': response,
            })
    return json.dumps({'r': res}, ensure_ascii=False)


@app.route('/media/<path:filename>', methods=['GET'])
def media_file(filename):
    return send_from_directory('./Records', filename, as_attachment=False)


@app.route('/loc/', methods=['POST'])
def loc():
    get_data = request.get_json(force=True)
    filename = get_data['filename']
    res = []
    audio_path = os.path.join('./Audio', filename)
    with open(audio_path, 'rb') as f:
        blob = FileStorage(f)

        response_code, filename, response = FileHandler.get_recognized_text(blob)

        if response_code == 0:
            response_audio_url = url_for('media_file', filename=filename)
        else:
            response_audio_url = None

        res.append({
            'response_audio_url': response_audio_url,
            'response_code': response_code,
            'response': response,
        })
    return json.dumps({'r': res}, ensure_ascii=False)
