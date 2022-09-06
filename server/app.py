import os

from flask import Flask

base_folder = str(os.getcwd())+"/../../images/"

app = Flask(__name__)

app.config['base_folder'] = base_folder