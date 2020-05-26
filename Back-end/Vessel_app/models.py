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
    
    # user profile image
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ## upload is the main attribute of the user and download in the future 
    ## the upload attribute looks back at the 'Upload' model 
    upload = db.relationship('Upload', backref='author', lazy=True)
  #   dicom = db.relationship('Dicom', backref='user', lazy=True)
    ## methods or magic methods printout
    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}')"
    
class Upload(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
        content = db.Column(db.Text, nullable=False) 
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        
        def __repr__(self):
            return f"upload('{self.title}', '{self.date_uploaded}')"
 
class Dicom(db.Model):
        
        ## data unqine id 
        id = db.Column(db.Integer, primary_key=True) 
        study_name = db.Column(db.String(300) , nullable=False)  
        
        # user id
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

       ## add sumbit button
        #title_of_upload = db.Column(db.String(100), nullable=False)
        ## date uploaded, pixel data
        date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
       
       ## DICOM binaray stack
        dicom_stack = db.Column(db.LargeBinary, nullable=False)
        ## 
       
        def __repr__(self):
            return f"upload( '{self.date_uploaded}')"


