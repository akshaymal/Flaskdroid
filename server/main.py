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
	cv2.imwrite("images/normal.jpg", open_cv_image)

	# image_to_classify = image_to_save.convert('L')
	# # image_to_classify = ImageOps.invert(image_to_classify)
	# image_to_classify = image_to_classify.resize((28,28))
	# open_cv_image_to_classify = np.array(image_to_classify)
	# cv2.imwrite("images/check.jpg", open_cv_image_to_classify)
	# image_to_classify = np.array(image_to_classify)
	# image_to_classify = np.expand_dims(image_to_classify, 0)
	# image_to_classify = classifier.preprocess_data(custom_data=image_to_classify, input=True)
	# predict_results = classifier.model.predict(image_to_classify)


	# prep
	cv2.imwrite("images/gray_1_org.jpg", gray)
	# contrast and brightness adjust
	adjusted = cv2.convertScaleAbs(gray, alpha=3.0, beta=0)
	cv2.imwrite("images/gray_2_adj.jpg", adjusted)
	# thresholding into binary image
	(thresh, gray) = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cv2.imwrite("images/gray_3_thresh.jpg", gray)
	# making background black and digit white
	number_of_white_pix = np.sum(gray >= 128)
	number_of_black_pix = np.sum(gray < 128)
	if number_of_black_pix < number_of_white_pix:
		gray = (255-gray)
	# Closing operator
	kernel = np.ones((10, 10), np.uint8)
	gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
	cv2.imwrite("images/gray_4_closed.jpg", gray)
	# Resizing into 224x224
	gray = cv2.resize(gray, (224, 224), interpolation=cv2.INTER_AREA)
	(thresh, gray) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cv2.imwrite("images/gray_5_resized.jpg", gray)
	cv2.imwrite("images/thresh.jpg", thresh)

	# dilating 
	kernel = np.ones((2, 2), np.uint8)
	gray = cv2.dilate(gray, kernel, iterations=1)
	cv2.imwrite("images/gray_6_dilated.jpg", gray)

	contours, hierarchy  = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	c = max(contours, key = cv2.contourArea)
	x,y,w,h = cv2.boundingRect(c)
	foreground = gray[y:y+h,x:x+w]
	if h > w:
		out_h = 20
		out_w = (20 * w) // h
		topBorder = 4
		botBorder = 4
		leftBorder = 14 - (out_w // 2)
		rightBorder = 14 - (out_w // 2)
	else:
		out_h = (20 * h) // w
		out_w = 20
		topBorder = 14 - (out_h // 2)
		botBorder = 14 - (out_h // 2)
		leftBorder = 4
		rightBorder = 4
	dim = (out_w, out_h)
	
	foreground = cv2.resize(foreground, dim, interpolation = cv2.INTER_AREA)
	cv2.imwrite("images/fore.jpg", foreground)
	gray = cv2.copyMakeBorder(
                 foreground,
				 topBorder,
				 botBorder,
				 leftBorder,
				 rightBorder,
                 cv2.BORDER_CONSTANT, 
                 value=0
              )
	gray = cv2.resize(gray, (224, 224), interpolation=cv2.INTER_AREA)
	cv2.imwrite("images/gray_final.jpg", gray)

	# TO REMOVE
	rgbimage = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

	rgbimage = np.expand_dims(rgbimage, 0)
	gray_im = classifier.preprocess_data(custom_data=rgbimage, input=True)
	predict_results = classifier.model.predict(gray_im)

	label = np.argmax(predict_results)
	print("Prediction:")
	print(predict_results*100)
	print("Label:")
	print(label)


	# Save file according the classification results
	filename = secure_filename(file.filename)
	category_path = os.path.join(app.config['base_folder'], str(label))
	folders = os.listdir(app.config["base_folder"])
	if str(label) not in folders:
		os.mkdir(category_path)
	image_to_save.save(os.path.join(category_path, filename))
	storage_status = 'Saved!'

	response = {"predict_label": str(label), "storage_status": storage_status, "confidence": predict_results.tolist()[0]}
	response["status_code"] = 201
	return response


if __name__ == "__main__":
	app.run(host="192.168.0.216", port=8080)
