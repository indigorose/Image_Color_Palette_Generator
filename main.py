import os
from colorthief import ColorThief

from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask import Flask, render_template, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import SubmitField

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOADED_FILES_ALLOW'] = ['.jpg', '.png', '.gif']
app.config['UPLOADED_FILES_DEST'] = './static/uploads'
app.config['SECRET_KEY'] = os.urandom(24)

photos = UploadSet('photos', IMAGES, default_dest=lambda x: app.config['UPLOADED_FILES_DEST'])
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed.'),
            FileRequired('File filed should not be empty.')
        ]
    )
    submit = SubmitField('Upload Image')


palette = []


def rgb_to_hex(color):
    return f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'


def color_palette(path):
    ct = ColorThief(path)
    ct_palette = ct.get_palette(color_count=10)
    hex_palette = []
    for color in ct_palette:
        hex_palette.append(rgb_to_hex(color))
    print(hex_palette)
    return hex_palette


@app.route('/static/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_FILES_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload():
    global palette
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        print(filename)
        file_path = os.path.join('static/uploads/' + filename)
        palette = color_palette(file_path)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url, palette=palette)


if __name__ == '__main__':
    app.run(debug=True)



# import cv2 as cv
# from sklearn.cluster import KMeans
# from werkzeug.utils import secure_filename
# Color Thief testing

# ct = ColorThief('rose.jpeg')
# dominant_color = ct. get_color(quality=1)
# print(dominant_color)
# print(type(dominant_color))
#
# palette = ct.get_palette(color_count=10)
# print(palette)
# print(type(palette))

# Open Cv and k-means testing
# read the image
# img = cv.imread('rose.jpeg')
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# dim = (500, 300)
# # resize images
# img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
# # K-Means testing
# clt = KMeans(n_clusters=10)
# clt.fit(img.reshape(-1, 3))
# color_array = clt.cluster_centers_
# for array in color_array:
#     new_array = [round(num) for num in array]
#     img_array.append(new_array)
# print(img_array)
