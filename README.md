# Book Rate - A book reviews app

> Book Rate gives you an elegant UI to scroll through and search through book lists with the idea of providing reliable information about a book.

## Steps to get the application running
### Requirements
1. python3 with pip
2. an internet connection

### steps
1. create a virtual environment
    - `python -m venv venv`
    - `.\venv\Scripts\activate`
    - `pip install -r requirements.txt`
2. set the necessary environmental variables
    - `set FLASK_APP=app.py`


### info the herokupostgresql database might lag sometimes to resolve this create a new database and set the env variable as DATABASE_URL
    . you do not need to create the tables your self but make sure to open a terminal window in the directory of the project and set the FLASK_APP env variable and activate the virtual environment the 
    1. db_execute.py -> this is for building the database
    3. python import.py

after these steps you will be able to run by using the command "flask run" the program with no problem!


















