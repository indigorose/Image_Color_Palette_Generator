import cv2 as cv
# import numpy as np
# import matplotlib.pyplot as plt
# import PIL
from sklearn.cluster import KMeans
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField


app = Flask(__name__)


# File upload
class MyForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')


# read the image
img = cv.imread('rose.jpeg')
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
dim = (500, 300)

# resize images
img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

# K-Means testing
clt = KMeans(n_clusters=10)
clt.fit(img.reshape(-1, 3))
color_array = clt.cluster_centers_
for array in color_array:
    new_array = [round(num) for num in array]
    print(new_array)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

