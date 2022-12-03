import os
import tensorflow as tf
import tensorflow_datasets as tfds

from flask import Flask
from dl_model import DLModel

classifier = None
model_folder_name = "model_zoo"
#
# app = Flask(__name__)
# base_folder = str(os.getcwd()) + "/../../images/"
# app.config['base_folder'] = base_folder

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    base_folder = os.path.join(os.getcwd(), "images")
    model_path = os.path.join(os.getcwd(), model_folder_name)
    if not (os.path.exists(base_folder)):
        os.mkdir(base_folder)
    app.config['base_folder'] = base_folder

    with app.app_context():
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        global classifier
        classifier = DLModel()
        classifier.input_data(x_train, y_train, x_test, y_test, (28, 28, 1))
        classifier.preprocess_data()
        classifier.train(model_path)
        classifier.test(model_path)

        return app