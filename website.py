from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
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

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROCESS_FOLDER"], exist_ok=True)
app.config["CURR_UPLOADED_FILES"] = []

class UploadFileForm(FlaskForm):
    file = FileField("file", validators=[InputRequired()])
    submit = SubmitField("UploadFile")

@app.route('/', methods=["GET","POST"])
def index():
    form = UploadFileForm()
    print('curr', app.config["CURR_UPLOADED_FILES"])
    return render_template('index.html', form=form, items=app.config["CURR_UPLOADED_FILES"])

@app.route('/file-process', methods=['POST'])
def file_process():
    files_to_process = []
    for key in request.files:
        files_to_process.append(request.files.get(key))

    pipe_man = pipeline_manager.WebManager()

    process_folder = app.config.get("PROCESS_FOLDER", "files")
    abs_process_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), process_folder)
    os.makedirs(abs_process_folder, exist_ok=True)  # Ensure folder exists

    for file in files_to_process:
        filename = secure_filename(file.filename)
        save_path = os.path.join(process_folder, filename)  # <-- THIS is relative, should use abs_process_folder
        print(save_path)
        file.save(save_path)

    app.config["CURR_UPLOADED_FILES"] = pipe_man.get_process_info(app, files_to_process)
    print('uploaded files', app.config["CURR_UPLOADED_FILES"])
    return jsonify(app.config["CURR_UPLOADED_FILES"])

@app.route('/file-upload', methods=["POST"])
def file_upload():
    pipe_man = pipeline_manager.WebManager()
    uploaded_files = []

    process_folder = app.config.get("PROCESS_FOLDER", "files")
    upload_folder = app.config.get("UPLOAD_FOLDER", "files")

    for file in request.files.getlist("file"):
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(process_folder, filename)
            file.save(save_path)
            uploaded_files.append(save_path)

    moved_files = []
    for file_path in uploaded_files:
        filename = os.path.basename(file_path)
        new_path = os.path.join(upload_folder, filename)
        shutil.move(file_path, new_path)
        moved_files.append(new_path)

    result = pipe_man.save_file(app, moved_files, 'Mats')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)