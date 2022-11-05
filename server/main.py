import os
import numpy as np

from PIL import Image ,ImageOps
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
	label = -1
	storage_status = "Not Saved!"

	# HTTP Error Handling
	if "file" not in request.files and request.files["file"] != "":
		response = {"Message": "No file to be uploaded"}
		response["status_code"] = 400
		return response

	# Process input result and obtain classification result
	file = request.files["file"]
	image_to_save = Image.open(file)
	image_to_classify = image_to_save.convert('L')
	image_to_classify = ImageOps.invert(image_to_classify)
	image_to_classify = image_to_classify.resize((28,28))
	image_to_classify = np.array(image_to_classify)
	image_to_classify = np.expand_dims(image_to_classify, 0)
	image_to_classify = classifier.preprocess_data(custom_data=image_to_classify, input=True)
	predict_results = classifier.model.predict(image_to_classify)
	label = np.argmax(predict_results)


	# Save file according the classification results
	filename = secure_filename(file.filename)
	category_path = os.path.join(app.config['base_folder'], str(label))
	folders = os.listdir(app.config["base_folder"])
	if str(label) not in folders:
		os.mkdir(category_path)
	image_to_save.save(os.path.join(category_path, filename))
	storage_status = 'Saved!'

	response = {"predict_label": str(label), "storage_status": storage_status}
	response["status_code"] = 201
	return response


if __name__ == "__main__":
	app.run(host="localhost", port=7878)
