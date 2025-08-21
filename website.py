from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from flask_socketio import SocketIO, emit
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import shutil
import os
from wtforms.validators import InputRequired
import pipeline_manager


app = Flask(__name__)
app.config["SECRET_KEY"] = "scretkey"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["UPLOAD_FOLDER"] = "files"
app.config["PROCESS_FOLDER"] = "process"

socketio = SocketIO(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROCESS_FOLDER"], exist_ok=True)
app.config["CURR_UPLOADED_FILES"] = []

class UploadFileForm(FlaskForm):
    file = FileField("file", validators=[InputRequired()])
    submit = SubmitField("UploadFile")

@app.route('/', methods=["GET","POST"])
def index():
    form = UploadFileForm()
    print('ind curr', app.config["CURR_UPLOADED_FILES"])
    return render_template('index.html', form=form, items=app.config["CURR_UPLOADED_FILES"])

@app.route('/file-process', methods=['POST'])
def file_process():
    files_to_process = []
    for key in request.files:
        file = request.files[key]
        print(file.filename)
        files_to_process.append(file.filename)

    pipe_man = pipeline_manager.WebManager()
    print(files_to_process, app.config["CURR_UPLOADED_FILES"], app.config.get("PROCESS_FOLDER"), app.config.get("UPLOAD_FOLDER"))
    uploaded_files = pipe_man.process_files(files_to_process, app.config["CURR_UPLOADED_FILES"], app.config.get("PROCESS_FOLDER"), app.config.get("UPLOAD_FOLDER"))

    return jsonify({
        'success': True,
        'message': 'Files processed successfully',
        'files': uploaded_files
    })

    # return render_template('index.html', form=UploadFileForm(), items=app.config["CURR_UPLOADED_FILES"])


@app.route('/get_files')
def get_files():
    files = []

    # Get files from your current uploaded files config
    for file_info in app.config["CURR_UPLOADED_FILES"]:
        files.append({
            'name': file_info['filename_no_ext'] + file_info['file_extension'],
            'size': file_info.get('size', 'Unknown'),
            'info': file_info  # Include full info if needed
        })

    return jsonify(files)

@app.route('/file-upload', methods=["POST"])
def file_upload():
    pipe_man = pipeline_manager.WebManager()
    processed_files = []

    for file in app.config["CURR_UPLOADED_FILES"]:
        processed_files.append(file['filename_no_ext'] + file['file_extension'])

    process_folder = app.config.get("PROCESS_FOLDER", "files")
    upload_folder = app.config.get("UPLOAD_FOLDER", "files")

    # for file in request.files.getlist("file"):
    #     if file and file.filename:
    #         filename = secure_filename(file.filename)
    #         save_path = os.path.join(process_folder, filename)
    #         file.save(save_path)
    #         uploaded_files.append(save_path)

    moved_files = []
    for file_name in processed_files:
        old_path = os.path.join(BASE_DIR, process_folder, file_name)
        new_path = os.path.join(BASE_DIR, upload_folder, file_name)
        shutil.move(str(old_path), str(new_path))
        print(old_path)
        moved_files.append(new_path)

    result = pipe_man.save_file(app.config["UPLOAD_FOLDER"], moved_files, 'Mats')

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
