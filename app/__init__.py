from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app.config['SECRET_KEY'] = 'SECRET_KEY'

from app import database
from app import routes
