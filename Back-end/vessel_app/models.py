from datetime import datetime #import date sumbitted
from vessel_app import db, login_manager
from flask_login import UserMixin

#extensions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#https://www.youtube.com/watch?v=44PvX0Yv368&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=5
## User class has attributes 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False )
    image_file = db.Column(db.LargeBinary, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    dicom = db.relationship('Dicom', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}')"


class UserReact(db.Model, UserMixin):

    __tablename__ = 'UserReact'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False )
    firstname = db.Column(db.String(120), unique=False, nullable=False )
    lastname = db.Column(db.String(120), unique=False, nullable=False )
    image_file = db.Column(db.LargeBinary, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    dicom = db.relationship('Dicom', backref='dicom', lazy=True)
    ContactInfo = db.relationship('ContactInfo', backref='contactinfo', lazy=True)
    Verify = db.relationship('Verify', backref='verify', lazy=True)

    def __repr__(self):
        return f"UserReact('{self.username}','{self.email}', '{self.image_file}')"
class ContactInfo(db.Model, UserMixin):

    __tablename__ = 'ContactInfo'

    id = db.Column(db.Integer, primary_key=True)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    username = db.Column(db.String(30), unique=True, nullable=False )
    phonenumber = db.Column(db.String(120), unique=True, nullable=False)
    residentialaddress = db.Column(db.String(120), unique=False, nullable=False )
    state = db.Column(db.String(120), unique=False, nullable=False )
    city = db.Column(db.String(120), unique=False, nullable=False )
    zipcode = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('UserReact.id'), nullable=False)

    def __repr__(self):
        return f"ContactInfo('{self.date_uploaded}')"


class Verify(db.Model, UserMixin):

    __tablename__ = 'Verify'

    id = db.Column(db.Integer, primary_key=True)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    username = db.Column(db.String(30), unique=True, nullable=False )
    ssn = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.String(120), unique=False, nullable=False )
    citizenship = db.Column(db.String(120), unique=False, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('UserReact.id'), nullable=False)

    def __repr__(self):
        return f"Verify('{self.date_uploaded}')"


class Checkpoint(db.Model):

    __tablename__ = 'Checkpoint'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False )
    userMade = db.Column(db.Boolean, default=False, nullable=False)
    userContactInfo = db.Column(db.Boolean, default=False, nullable=False)
    userVerify = db.Column(db.Boolean, default=False, nullable=False)
    def __repr__(self):
        return f"Checkpoint('{self.username}')"


class AuthTable(db.Model):

    __tablename__ = 'AuthTable'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False )
    AccessCode = db.Column(db.Boolean, default=False, nullable=False)
    userconsent = db.Column(db.Boolean, default=False, nullable=False)
    ssnReal = db.Column(db.Boolean, default=False, nullable=False)
    idReal = db.Column(db.Boolean, default=False, nullable=False)
    passportReal = db.Column(db.Boolean, default=False, nullable=False)
    def __repr__(self):
        return f"AuthTable('{self.username}')"

class DicomMetaData(db.Model):

    __tablename__ = 'DicomMetaData'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    study_date = db.Column(db.Integer, nullable=True)
    study_id = db.Column(db.Integer, nullable=True)
    modality = db.Column(db.String(200), nullable=False)
    file_count = db.Column(db.Integer, nullable=True) 
    session_id = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.LargeBinary, nullable=False)
    # categories = db.relationship('Dicom', back_populates='dicommetadata')
    # formData = db.relationship('DicomFormData', secondary=association_table )
    # formData = db.relationship('DicomFormData', uselist=True, backref='DicomMetaData', lazy=True) #uselist one to one relationship

    def __repr__(self):
        return f"DicomMetaData('{self.date_uploaded}', '{self.study_id}', '{self.study_date}', '{self.study_date}'  )"

class Dicom(db.Model):
    
    __tablename__ = 'dicom'
    ## data unqine id 
    id = db.Column(db.Integer, primary_key=True)  
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userReact_id = db.Column(db.Integer, db.ForeignKey('UserReact.id'), nullable=True)
    dicom_stack = db.Column(db.LargeBinary, nullable=False)
    thumbnail = db.Column(db.LargeBinary, nullable=False)
    file_count = db.Column(db.Integer, nullable=True) 
    session_id = db.Column(db.String(200), nullable=False)
    formData = db.relationship('DicomFormData', uselist=True, backref='author', lazy=True) #uselist one to one relationship
    

    def __repr__(self):
        return f"Dicom('{self.date_uploaded}')"

class Dicom2(db.Model):
    __bind_key__ = '2nd_db'
    ## data unqine id 
    id = db.Column(db.Integer, primary_key=True) 
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    dicom_stack = db.Column(db.LargeBinary, nullable=False)
    session_id = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f"Dicom('{self.date_uploaded}')"




class DicomFormData(db.Model):
    __tablename__ = 'DicomFormData'
    id = db.Column(db.Integer, primary_key=True)  
    session_id = db.Column(db.String(200), db.ForeignKey('dicom.session_id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    study_name = db.Column(db.String(300), nullable=False) 
    description = db.Column(db.String(1000), nullable=False)
    
    # metadata_id = db.Column(db.Integer, db.ForeignKey(DicomMetaData.id), nullable=False)
    # session_id = db.Column(db.String(200), db.ForeignKey('DicomMetaData.session_id'), nullable=False)
    def __repr__(self):
        return f"DicomFormData('{self.study_name}', '{self.description}')"


class FalseForm(db.Model):
    __tablename__ = 'FalseForm'
    id = db.Column(db.Integer, primary_key=True)  
    session_id = db.Column(db.String(200), db.ForeignKey('dicom.session_id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    study_name = db.Column(db.String(300), nullable=False) 
    description = db.Column(db.String(1000), nullable=False)
    
    # metadata_id = db.Column(db.Integer, db.ForeignKey(DicomMetaData.id), nullable=False)
    # session_id = db.Column(db.String(200), db.ForeignKey('DicomMetaData.session_id'), nullable=False)
    def __repr__(self):
        return f"FalseForm('{self.study_name}', '{self.description}')"

class FalseDicom(db.Model):
    
    __tablename__ = 'FalseDicom'
    ## data unqine id 
    id = db.Column(db.Integer, primary_key=True)  
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    temp_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dicom_stack = db.Column(db.LargeBinary, nullable=False)
    file_count = db.Column(db.Integer, nullable=True) 
    session_id = db.Column(db.String(200), nullable=False)
    # formData = db.relationship('FalseForm', uselist=True, backref='author', lazy=True) #uselist one to one relationship
    

    def __repr__(self):
        return f"FalseDicom('{self.date_uploaded}')"




class Object_3D(db.Model):
    ## data unqine id 
    id = db.Column(db.Integer, primary_key=True)  
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    object_3D = db.Column(db.LargeBinary, nullable=False)
    session_id = db.Column(db.String(200), nullable=False)
    #formData = db.relationship('DicomFormData', backref='author', lazy=True)
    session_id_3d = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Object_3D('{self.date_uploaded}')"


class Cidtable(db.Model):
    ## data unqine id 
    id = db.Column(db.Integer, primary_key=True)  
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    session_id = db.Column(db.String(200), nullable=False)
    cid = db.Column(db.String(200), nullable=False)
    #formData = db.relationship('DicomFormData', backref='author', lazy=True)
    cold_storage_id = db.Column(db.String(200), nullable=False) ## cold_storage just retain the session IDs is listed out for the user to collect data

    def __repr__(self):
        return f"Cidtable('{self.date_uploaded}')"


# class Save_csrf_token(db.Model):
#     __bind_key__ = 'redis_db'
#     id = db.Column(db.Integer, primary_key=True)  
#     csrf_token = db.Column(db.Integer)
#     date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    
#     def __repr__(self):
#         return f"save_csrf_token('{self.date_uploaded}')"

    __str__ = __repr__