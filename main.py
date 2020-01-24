# docker run -itv $(pwd)/uploads:/test_files slacgismo/gridlabd:latest

import os
import urllib.request
import json
import sys
import getopt
import shutil
import glob
from app import app
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['json', 'csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert')
def upload_form():
    return render_template('convert.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        uploadFiles = glob.glob('./uploads/*')
        for f in uploadFiles:
            os.remove(f)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(filename + ' successfully uploaded')
            os.system('docker pull slacgismo/gridlabd:develop')
            os.system('docker run -itv $(pwd)/uploads:/test_files --entrypoint=/bin/bash slacgismo/gridlabd:develop gridlabd ../test_files/' + filename)
            # --entrypoint=/bin/bash <imagename>
            glmFile = glob.glob('./uploads/*.glm')
            glmFile = glmFile[0].split("/")[-1:][0]
            # file.save(os.path.join(app.config['UPLOAD_FOLDER']
            return redirect(url_for('download', filename = glmFile))
        else:
            flash('Allowed file types are json')
            return redirect('/convert')


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)


# gridlabd test.glm -o t.json
# gridlabd test.glm -o t.png
# gridlabd test.glm -o test.glm
# gridlabd V test.glm
# -D glm_save_options = MINIMAL ( dropdown menu with all the different options)
