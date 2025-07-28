from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scretkey'

class UploadFileForm(FlaskForm):
    file = FileField("file")
    submit = SubmitField("UploadFile")

@app.route('/', methods=["GET","POST"])
def index():
    form = UploadFileForm()
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)