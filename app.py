from flask import Flask
app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'SUPER SECRET'
from routes import *




