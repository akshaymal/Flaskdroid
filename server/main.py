import os
import tensorflow as tf

from app import app
from flask import request
from werkzeug.utils import secure_filename
from dl_model import DLModel

@app.before_first_request
def setup():
	global MODEL
	(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
	MODEL = DLModel()
	MODEL.input_data(x_train, y_train, x_test, y_test, (28,28,1))
	MODEL.preprocess_data()
	MODEL.train()

@app.route('/upload',methods=['GET'])
def upload_get_request():
	print("Received the GET request")
	response = {"Message": "Received the request"}
	return response

@app.route('/upload',methods=['POST'])
def upload_file():
	if "file" not in request.files:
		response = {"Message":"No file to be uploaded"}
		response["status_code"] = 400
		return response

	file = request.files["file"]

	if file:
		filename = secure_filename(file.filename)
		category = request.form["category"]
		category_path = os.path.join(app.config['base_folder'], category)

		folders = os.listdir(app.config["base_folder"])
		if category not in folders:
			os.mkdir(category_path)

		all_files = os.listdir(category_path)
		file.save(os.path.join(category_path, filename))

		response = {"Message":"File uploaded successfully"}
		response["status_code"] = 201

		return response

if __name__ == "__main__":
	app.run(host="192.168.0.51", port=5000)