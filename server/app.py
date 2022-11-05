import os
import tensorflow as tf

from flask import Flask
from dl_model import DLModel

classifier = None
#
# app = Flask(__name__)
# base_folder = str(os.getcwd()) + "/../../images/"
# app.config['base_folder'] = base_folder

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    base_folder = str(os.getcwd()) + "/images/"
    app.config['base_folder'] = base_folder

    with app.app_context():
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        global classifier
        classifier = DLModel()
        classifier.input_data(x_train, y_train, x_test, y_test, (28, 28, 1))
        classifier.preprocess_data()
        classifier.train()

        return app