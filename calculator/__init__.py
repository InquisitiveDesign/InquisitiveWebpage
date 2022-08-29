from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = '471964c08066039057be602f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///design.db'

db = SQLAlchemy(app)

from calculator import bearingroute
