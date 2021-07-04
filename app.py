import os
from flask import Flask, request, redirect, url_for, render_template,flash
from werkzeug.utils import secure_filename
from utils.filters import *

app = Flask(__name__, static_url_path="/static")
UPLOAD_FOLDER ="static/uploads/"
DOWNLOAD_FOLDER = "static/downloads/"
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

# APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'YourSecretKey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size to 2mb
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            if request.form['action'] == 'Sobel':
                apply_sobel_filter(filename)
            elif request.form['action'] == 'Laplace':
                apply_laplace_filter(filename)
            elif request.form['action'] == 'Hist Balance':
                apply_histogram_balance(filename)
            data={
                "processed_img":'static/downloads/'+filename,
                "uploaded_img":'static/uploads/'+filename
            }
            return render_template("index.html",data=data) 
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)