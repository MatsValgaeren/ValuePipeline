from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

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

@app.route('//file-upload', methods=["POST"])
def file_upload():
    uploaded_files = request.files.getlist('file')
    saved_files = []
    for file in uploaded_files:
        if file:
            filename = file.filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            saved_files.append(filename)

    return jsonify({'message': 'Files uploaded successfully', 'files': saved_files})

if __name__ == "__main__":
    app.run(debug=True)