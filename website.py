from flask import Flask, render_template, request, jsonify
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

class UploadFileForm(FlaskForm):
    file = FileField("file", validators=[InputRequired()])
    submit = SubmitField("UploadFile")

@app.route('/', methods=["GET","POST"])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(
            os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config["UPLOAD_FOLDER"],
            secure_filename(file.filename)
            )
        )
        return "File has been uploaded."
    return render_template('index.html', form=form)

@app.route('/file-process', methods=["POST"])
def file_process():
    uploaded_files = request.files.getlist('file')
    pipe_man = pipeline_manager.WebManager()

    process_folder = app.config.get("PROCESS_FOLDER", "files")
    abs_process_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), process_folder)
    os.makedirs(abs_process_folder, exist_ok=True)  # Ensure folder exists

    for file in uploaded_files:
        filename = secure_filename(file.filename)
        save_path = os.path.join(process_folder, filename)  # <-- THIS is relative, should use abs_process_folder
        print(save_path)
        file.save(save_path)

    print('done')
    ret = pipe_man.save_file(app, uploaded_files, 'Mats')
    return jsonify(ret)

# @app.route('/file-upload', methods=["GET", "POST"])
# def file_upload():
#     print('uploading')
    # processed_files = []
    #
    # process_folder = app.config.get("PROCESS_FOLDER", "files")
    # upload_folder = app.config.get("UPLOAD_FOLDER", "files")
    # print('process folder', process_folder)
    # for file in process_folder:
    #     old_path = os.path.join(upload_folder, str(file))
    #     new_path = os.path.join(process_folder, str(file))
    #
    #     shutil.move(old_path, new_path)
    #     processed_files.append(new_path)


if __name__ == "__main__":
    app.run(debug=True)