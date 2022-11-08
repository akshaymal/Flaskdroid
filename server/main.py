import os
import numpy as np

from PIL import Image ,ImageOps
from app import init_app
from flask import request
from werkzeug.utils import secure_filename
import cv2
# import imutils
# from imutils.perspective import four_point_transform

from matplotlib import pyplot as plt

app = init_app()
np.set_printoptions(suppress=True)


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


	open_cv_image = np.array(image_to_save)

	if len(open_cv_image.shape) > 2:
		gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
	else:
		gray = open_cv_image
	open_cv_image_resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
	(thresh, gray) = cv2.threshold(open_cv_image_resized, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cv2.imwrite("images/normal.jpg", open_cv_image)
	cv2.imwrite("images/resized.jpg", open_cv_image_resized)
	cv2.imwrite("images/thresh.jpg", thresh)
	cv2.imwrite("images/gray.jpg", gray)


	# image_to_classify = image_to_save.convert('L')
	# # image_to_classify = ImageOps.invert(image_to_classify)
	# image_to_classify = image_to_classify.resize((28,28))
	# open_cv_image_to_classify = np.array(image_to_classify)
	# cv2.imwrite("images/check.jpg", open_cv_image_to_classify)
	# image_to_classify = np.array(image_to_classify)
	# image_to_classify = np.expand_dims(image_to_classify, 0)
	# image_to_classify = classifier.preprocess_data(custom_data=image_to_classify, input=True)
	# predict_results = classifier.model.predict(image_to_classify)

	# check 
	gray = np.expand_dims(gray, 0)
	gray_im = classifier.preprocess_data(custom_data=gray, input=True)
	predict_results = classifier.model.predict(gray_im)

	label = np.argmax(predict_results)
	print("Prediction:")
	print(predict_results*100, label)


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
	app.run(host="192.168.0.51", port=8080)
