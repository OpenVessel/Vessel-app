# OpenVessel

[OpenVessel](http://openvessel.org/) is an open-source Flask app that segments out portions of DICOM files using machine learning hosted on celery workers, and displays the result as a 3D objects using VTK. 

## Installation

### On Windows 

#### Get the repository
```  
git clone https://github.com/OpenVessel/Vessel-app.git
```

#### Make the Virtual Environment (Optional)
```
python3 -m venv vessel_env  
vessel_env\Script\activate   
```  

#### Install requirements
```
pip3 install -r requirements.txt
```


#### Installing VTK
One of the main dependencies for the project is a tool called VTK, short for *The Visualization Toolkit*. It allows us to render 3D images of DICOM files.

[Directions to install VTK on Windows](https://vtk.org/Wiki/VTK/Building/Windows)

#### Installing Redis

Our machine learning happens on various workers with the help of celery. Celery is included in requirements.txt, however it needs a Redis server to work off of. 

[Directions to install Redis](https://redis.io/download)

Once you have Redis installed, you need to point to the the URL that the Redis broker is located at.

Open config.py and find these lines 

```
class Config: 

	...
	 
     ### Celery Workers ##########  
    CELERY_BROKER_URL='redis://localhost:6379/0'  
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
```
Change the *redis://localhost:6379/0* to whatever port your Redis server is running on.

### On MacOS

#### Get the repo  
```  
git clone https://github.com/OpenVessel/Vessel-app.git 
```

#### Make the Virtual Environment (Optional)
```
python3 -m venv vessel_env  
source vessel_env/Script/activate   
```  

#### Install requirements
```
pip3 install -r requirements.txt
```

#### Installing VTK
One of the main dependencies for the project is a tool called VTK, short for *The Visualization Toolkit*. It allows us to render 3D images of dicom files. 

```
brew install vtk
```

#### Installing Redis

Our machine learning happens on various workers with the help of celery. Celery is included in requirements.txt, however it needs a Redis server to work off of. 

Install Redis
```
brew install redis
```

Once you have Redis installed, you need to point to the the URL that the Redis broker is located at.

Open config.py and find these lines 

```
class Config:  

	...

     ### Celery Workers ##########  
    CELERY_BROKER_URL='redis://localhost:6379/0'  
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
```
Change the *redis://localhost:6379/0* to whatever port your Redis server is running on.

## Running the App

### Initialize the database

We use Flask-SQLAlchemy to connect to our SQLite database, and Flask-Migrate by _Miguel Grinberg_ to update the database as we make changes. 

In order to run the Flask app you need to have a database. 
First make your current working directory the Back-end folder in the repo. 
```
cd Vessel-app/vessel_app/Back-end
```
Run these commands to initialize the database.

```
flask db init
flask db migrate
flask db upgrade
```
### Running the Flask app

Make sure you are in the Back-end directory then run
```
flask run
```
and the website will run on a local port for you!
