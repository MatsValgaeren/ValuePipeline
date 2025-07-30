from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import file_utils


app = Flask(__name__)
app.config["SECRET_KEY"] = "scretkey"
app.config["UPLOAD_FOLDER"] = "files"

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

@app.route('/file-upload', methods=["POST"])
def file_upload():
    uploaded_files = request.files.getlist('file')
    isd = file_utils.save_file(app, uploaded_files, 'Mats')
    print(isd)
    return jsonify(isd)

if __name__ == "__main__":
    app.run(debug=True)