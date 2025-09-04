from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from flask_socketio import SocketIO, emit
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import shutil
import os
import json
from wtforms.validators import InputRequired
import pipeline_manager


app = Flask(__name__)
app.config["SECRET_KEY"] = "scretkey"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["PROCESS_FOLDER"] = "process"

socketio = SocketIO(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROCESS_FOLDER"], exist_ok=True)
app.config["CURR_PROCESSED_FILES"] = []

class UploadFileForm(FlaskForm):
    file = FileField("file", validators=[InputRequired()])
    submit = SubmitField("UploadFile")

@app.route('/', methods=["GET","POST"])
def index():
    form = UploadFileForm()
    return render_template('index.html', form=form, items=app.config["CURR_PROCESSED_FILES"])

@app.route('/file-process', methods=['POST'])
def file_process():
    files_to_process = []
    for key in request.files:
        file = request.files[key]
        files_to_process.append(file)

    pipe_man = pipeline_manager.WebManager()
    app.config["CURR_PROCESSED_FILES"] = pipe_man.process_files(files_to_process, app.config["CURR_PROCESSED_FILES"], app.config.get("PROCESS_FOLDER"), app.config.get("UPLOAD_FOLDER"))

    return jsonify({
        'success': True,
        'message': 'Files processed successfully',
        'files': app.config["CURR_PROCESSED_FILES"]
    })


@app.route('/get_files')
def get_files():
    files = []

    # Get files from your current uploaded files config
    for file_info in app.config["CURR_PROCESSED_FILES"]:
        files.append({
            'name': file_info['filename'] ,
            'ext': '.' + file_info['filename'].split('.')[-1],
            'size': file_info.get('size', 'Unknown'),
            'info': file_info  # Include full info if needed
        })
    return jsonify(files)

@app.route('/file-upload', methods=["POST"])
def file_upload():
    print("Request form:", request.form)
    user = request.form.get('user')
    render_selected_raw = request.form.get('render_selected', '[]')
    print("Raw render_selected:", render_selected_raw)
    try:
        render_selected = set(json.loads(render_selected_raw))
    except Exception as e:
        print("JSON load error:", e)
        render_selected = set()

    print("Parsed render_selected:", render_selected)
    user = request.form.get("user", "default_user")

    render_selected = set(request.form.getlist("render_selected"))
    upload_folder = app.config.get("upload_folder", "uploads")  # or whatever you use
    base_dir = os.path.abspath(os.path.dirname(__file__))        # ensure base_dir is set

    render_full_paths = set()
    for filename in render_selected:
        full_path = os.path.join(base_dir, upload_folder, filename)
        if os.path.exists(full_path):
            render_full_paths.add(full_path)
        else:
            print(f"⚠️ File not found for rendering: {full_path}")

    pipe_man = pipeline_manager.WebManager()
    processed_files = []

    for file in app.config["CURR_PROCESSED_FILES"]:
        processed_files.append(file['filename_no_ext'] + file['file_extension'])

    process_folder = app.config.get("PROCESS_FOLDER", "files")
    upload_folder = app.config.get("UPLOAD_FOLDER", "files")

    for file in request.files.getlist("file"):
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(process_folder, filename)
            file.save(save_path)
            uploaded_files.append(save_path)

    moved_files = []
    for file in processed_files:
        file_name = file
        old_path = os.path.join(BASE_DIR, process_folder, file_name)
        new_path = os.path.join(BASE_DIR, upload_folder, file_name)
        shutil.move(str(old_path), str(new_path))
        moved_files.append(new_path)

    # print(app.config["UPLOAD_FOLDER"], moved_files, "penis")
    result = pipe_man.save_file(moved_files, upload_folder, user)
    app.config["CURR_PROCESSED_FILES"] = []

    pipe_man.render(render_full_paths, upload_folder)
    # return redirect(url_for('index'))
    return jsonify(success=True)

@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    filename = request.args.get('name')
    print(app.config["CURR_PROCESSED_FILES"])
    for file in app.config["CURR_PROCESSED_FILES"]:
        if file['filename'] == filename:
            app.config["CURR_PROCESSED_FILES"].remove(file)
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
