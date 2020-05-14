
app.config['SECRET_KEY'] = 'ffb3986d5d75c04081caa3d7fb94c205'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Sd40dash2@localhost/Vessel-test' 
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH= os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.dcm',
    DROPZONE_MAX_FILE_SIZE=5,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_MULTIPLE=True,
    DROPZONE_PARALLEL_UPLOADS = 3 
)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + 'static/uploads_files'
ALLOWED_EXTENSIONS = {'dcm'}
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ALLOWED_EXTENSIONS