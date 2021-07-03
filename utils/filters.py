import numpy as np
import cv2
import os

UPLOAD_FOLDER ="static/uploads/"
DOWNLOAD_FOLDER = "static/downloads/"

def apply_sobel_filter(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
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

    cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, filename),grad)

def apply_laplace_filter(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    kernel_size = 3
    ddepth = cv2.CV_16S
    image = cv2.imread(path)
    image = cv2.GaussianBlur(image, (3,3), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(gray, ddepth, ksize=kernel_size)

    cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, filename),dst)

def apply_histogram_balance(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.equalizeHist(image)
    cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, filename),image)