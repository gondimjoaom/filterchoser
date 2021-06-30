import os
from flask import Flask, request, redirect, url_for, render_template,flash
from werkzeug.utils import secure_filename
import numpy as np
import cv2

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

@app.route('/', methods=['GET', 'POST'])
def index():
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
            process_file(os.path.join(UPLOAD_FOLDER, filename), filename)
            data={
                "processed_img":'static/downloads/'+filename,
                "uploaded_img":'static/uploads/'+filename
            }
            return render_template("index.html",data=data)  
    return render_template('index.html')

def process_file(path, filename):
    apply_sobel_filter(path, filename)

def apply_sobel_filter(path, filename):
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S
    image = cv2.imread(path)
    image = cv2.GaussianBlur(image, (3,3), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    cv2.imwrite(f"{DOWNLOAD_FOLDER}{filename}",grad)

if __name__ == '__main__':
    app.run()