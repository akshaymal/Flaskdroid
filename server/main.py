import os
import numpy as np

from PIL import Image
from app import init_app
from flask import request
from werkzeug.utils import secure_filename

app = init_app()


@app.route('/upload', methods=['GET'])
def upload_get_request():
    print("Received the GET request")
    response = {"Message": "Received the request"}
    return response


@app.route('/upload', methods=['POST'])
def upload_file():
	"""
	upload_file(): Responsible for accepting a image (hand written digit), classifying it and storing it in the
	appropriate directory.
	"""
	from app import classifier
	label = None
	storage_status = "Not Saved!"


	# HTTP Error Handling
	if "file" not in request.files and request.files["file"] != "":
		response = {"Message": "No file to be uploaded"}
		response["status_code"] = 400
		return response

	# Process input result and obtain classification result
	file = request.files["file"]
	input_image = Image.open(file).convert('L')
	input_image = input_image.resize((28,28))
	np_input_image = np.array(input_image)
	np_input_image = np.expand_dims(np_input_image, 0)
	np_input_image = classifier.preprocess_data(custom_data=np_input_image, input=True)
	predict_results = classifier.model.predict(np_input_image)
	label = np.argmax(predict_results)


	# Save file according the classification results
	filename = secure_filename(file.filename)
	category_path = os.path.join(app.config['base_folder'], str(label))
	folders = os.listdir(app.config["base_folder"])
	if str(label) not in folders:
		os.mkdir(category_path)
	file.save(os.path.join(category_path, filename))
	storage_status = 'Saved!'

	response = {"predict_label": str(label), "storage_status": storage_status}
	response["status_code"] = 201
	return response


if __name__ == "__main__":
    app.run(host="192.168.0.51", port=5000)
