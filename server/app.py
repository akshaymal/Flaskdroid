import os
import tensorflow as tf
import tensorflow_datasets as tfds

from flask import Flask
from dl_model import DLModel

classifier = None
# classifier1 = None
# classifier2 = None
# classifier3 = None
# classifier4 = None
# classifiercomb = None

# BOTTOM LEFT
model_folder_name = "tl_model"
# model1_folder_name = "tl_model"
# model2_folder_name = "tr_model"
# model3_folder_name = "bl_model"
# model4_folder_name = "br_model"
# modelcomb_folder_name = "comb_model"


#
# app = Flask(__name__)
# base_folder = str(os.getcwd()) + "/../../images/"
# app.config['base_folder'] = base_folder

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    base_folder = os.path.join(os.getcwd(), "images")

    model_path = os.path.join(os.getcwd(), model_folder_name)
    # model1_path = os.path.join(os.getcwd(), model1_folder_name)
    # model2_path = os.path.join(os.getcwd(), model2_folder_name)
    # model3_path = os.path.join(os.getcwd(), model3_folder_name)
    # model4_path = os.path.join(os.getcwd(), model4_folder_name)
    # modelcomb_path = os.path.join(os.getcwd(), modelcomb_folder_name)

    if not (os.path.exists(base_folder)):
        os.mkdir(base_folder)
    app.config['base_folder'] = base_folder

    with app.app_context():
        # (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

        global classifier
        # global classifier1
        # global classifier2
        # global classifier3
        # global classifier4
        # global classifiercomb

        # classifier = tf.keras.models.load_model(model_path)
        # classifier = DLModel()

        classifier = tf.keras.models.load_model(model_path)
        # classifier1 = tf.keras.models.load_model(model1_path)
        # classifier2 = tf.keras.models.load_model(model2_path)
        # classifier3 = tf.keras.models.load_model(model3_path)
        # classifier4 = tf.keras.models.load_model(model4_path)
        # classifiercomb = tf.keras.models.load_model(modelcomb_path)

        # classifier.input_data(x_train, y_train, x_test, y_test, (28, 28, 1))
        # classifier.preprocess_data()
        # classifier.train(model_path)
        # classifier.test(model_path)

        return app
