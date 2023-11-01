import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from notebooks import main

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'notebooks/run_data')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('select_files.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        af = request.files['audio_file']
        af_filename = secure_filename(af.filename)
        print(af_filename)

        AUDIO_FILE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], af_filename)
        app.config['AUDIO_FILE_PATH'] = AUDIO_FILE_PATH
        af.save(app.config['AUDIO_FILE_PATH'])

        print(app.config['AUDIO_FILE_PATH'])

        pred_output = main.process_files(str(AUDIO_FILE_PATH))
    return render_template("result.html",LABEL=pred_output)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
