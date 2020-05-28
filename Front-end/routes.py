from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///site.db'
#db = SQLAlchemy(app)

#class User(db.Model):
#    id = db.Column (db.Integer, primary_key=True)
#    username = db.Column (db.String(20), unique=True, nullable=False)
#    first_name = db.Column (db.String(20), unique=False, nullable=False)
#    last_name = db.Column (db.String(20), unique=False, nullable=False)

#    image_file = db.Column(db.String(20), nullable=False, default='static/img/default.jpg')
#    hospital_name = db.Column (db.String(20), unique=False, nullable=False)
#    email_id = db.Column (db.String(20), unique=True, nullable=False)
#    password = db.Column (db.String(20), nullable=False)

    #def __repr__(self):
        #return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
@app.route('/')
def home(): 
    return render_template ('layout.html')

@app.route('/login')
def login():
    return render_template ('login.html')

@app.route('/register')
def register():
    return render_template ('register.html')

if __name__ == "__main__":
	app.run(debug=True)