from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
class Config(object):
    """set parameters"""
    # set URL
    user = ''
    password = ''
    database = ''
    app.config['SQLALCHEMY_DATABASE_URI'] = ''



# set parameters
app.config.from_object(Config)
app.config['SECRET_KEY'] = '123456'

'''create sqlalchemy object'''
db = SQLAlchemy(app)