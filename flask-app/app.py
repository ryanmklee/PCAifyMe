import os
from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image Only!'), FileRequired(u'Choose a file!')])
    submit = SubmitField(u'Upload')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            name = filename.filename
            photos.save(filename, name=name)
        success = True
    else:
        success = False
    return render_template('index.html', form=form, success=success)


@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('manage.html', files_list=files_list)


@app.route('/open/<filename>')
def open_file(filename):
    file_url = photos.url(filename)
    print(file_url)
    return render_template('main.html', file_url=file_url)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = photos.path(filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))

@app.route('/photos', methods=['GET'])
def view_images():
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    pictures = []
    for p in files_list:
        photo_name = photos.url(p)
        pictures.append(photo_name)
    return render_template('photos.html', pictures=pictures)

@app.route('/api/photos', methods=['GET'])
def get_images():
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    pictures = []
    for p in files_list:
        photo_name = photos.url(p)
        pictures.append(photo_name)
    return json.dumps(pictures)

if __name__ == '__main__':
    app.run(debug=True)