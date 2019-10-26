# news24-FlaskApp
my very first web App built with Flask frame work

This is  simple and basic new blogging app implemented with flask and MySQL. 
to run this app successfully, you need to do the following. 
create tables with columns as corresponds with database.py in app directory.
Enter into the flask virtual environment by  
$python3 -m venv venv
$. venv/bin/activate
then export FLASK_APP
$export FLASK_APP=run.py
$flask run

with this you'll be running the app on a development server, localhost:5000/

with pycharm, edit run configuration to run app.

also, you should have installed mysql on the system.
$sudo apt-get install mysql
$sudo apt-get install mysql-server libmysqlclient-dev
