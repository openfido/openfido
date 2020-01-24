from flask import Flask, render_template
import os

UPLOAD_FOLDER = './uploads'
# GLM_FOLDER = './glm_files'

app = Flask(__name__)
app.secret_key = "secret key"
# app.config['GLM_FOLDER'] = GLM_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
