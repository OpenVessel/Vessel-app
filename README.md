# OpenVessel

  

[OpenVessel](http://openvessel.org/) is an open-source Flask app that segments out portions of DICOM files using machine learning hosted on celery workers, and displays the result as a 3D objects using VTK.

  

### Installation

  

## On Windows

  

### Get the repository

```

git clone https://github.com/OpenVessel/Vessel-app.git

```

  

### Make the Virtual Environment (Optional)

```

python3 -m venv vessel_env

vessel_env\Script\activate

```

  

### Install requirements

```

pip3 install -r requirements.txt

```

### Set up JavaScript/EMCAScript

If you do not have **npm** and **nodeJS**, follow this guide:
[Directions to install npm](https://www.npmjs.com/get-npm)

Then, type this in the terminal starting at the Vessel-app

```

cd Back-end\vessel_app\static

npm install

npm run build 

```

To run JavaScript for debugging, run

```

npm run watch

```
  

### Installing VTK

One of the main dependencies for the project is a tool called VTK, short for *The Visualization Toolkit*. It allows us to render 3D images of DICOM files.

  

[Directions to install VTK on Windows](https://vtk.org/Wiki/VTK/Building/Windows)

  

### Installing Redis

  

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

  

## On MacOS


### Get the repo

```

git clone https://github.com/OpenVessel/Vessel-app.git

```

### Make the Virtual Environment (Optional)

```

python3 -m venv vessel_env

source vessel_env/bin/activate

```

### Install requirements

```

pip3 install -r requirements.txt

```

### Set up JavaScript/EMCAScript

If you do not have **npm** and **nodeJS**, follow this guide:
[Directions to install npm](https://www.npmjs.com/get-npm)

Then, type this in the terminal starting at the Vessel-app

```

cd Back-end/vessel_app/static

npm install

npm run build 

```

To run JavaScript for debugging, run

```

npm run watch

```

### Installing VTK

One of the main dependencies for the project is a tool called VTK, short for *The Visualization Toolkit*. It allows us to render 3D images of dicom files.

  

In this subsection, you will learn how to install **VTK** and it's dependancies for **macOS**.

#### Requirements:

1. Homebrew

2. Python 3.X

3. CMake

#### 1. Installing Homebrew

If you don't have **Homebrew** installed on your Mac, install it by going to [Homebrew's website](https://brew.sh) or by entering the command below in your **Terminal**.
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

#### 2. Installing VTK using Homebrew

Now, we'll use Homebrew to install VTK.

Enter the following into your Terminal.
```
brew install vtk
```

#### 3. Install CMake

Install Kitware's CMake tool to download VTK's dependancies.

Go [here](https://cmake.org/download/) to get the latest version.

#### 4. Downloading VTK dependancies

Follow the steps below to download everything you'll need to run VTK.

 1. Open CMake

 2. Go to Tools > How to Install for Command Line Use

 3. Click on "How to Install for Command Line Use"

 4. Follow the instructions in the dialogue box that opens

#### 5. Check that you did the above steps correctly.

To make sure that everything has gone smoothly, enter the following in the **Terminal**.
```
which cmake
```
If this works correctly, enter the following to make sure you have the latest version installed.

```
cmake --version
```

#### Installing Redis

Our machine learning happens on various workers with the help of celery. Celery is included in requirements.txt, however it needs a Redis server to work off of.

In order to install Redis for MacOS enter the following commands into a command prompt:
```

brew install redis

brew services start redis

brew services stop redis

brew services restart redis

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

### Start celery

1. Make a new terminal

2. Go into the virtual environment

3. cd into Back_end

5. Run the command:
```

celery -A vessel_app.file_pipeline.celery_tasks.celery worker --loglevel=info -P gevent

```


### Run the Flask app

  

Make sure you are in the Back-end directory then run

```
flask run
```

and the website will run on a local port for you!

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
source vessel_env/bin/activate   
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
