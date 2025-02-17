from imutils import paths
import face_recognition
import pickle
import cv2
import os
import imutils

DATASET_URL = 'app/facial_recognition/dataset/'
ENCODINGS_URL = 'app/facial_recognition/output/encodings.pickle'
DETECTION_METHOD = 'cnn'

def encode():
	"""
	encode all faces from images in the dataset to
	128-dimension vectors using provided cnn model.
    """
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(DATASET_URL))
	knownEncodings = []
	knownNames = []

	for (i, imagePath) in enumerate(imagePaths):
		print("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb,
			model=DETECTION_METHOD)

		encodings = face_recognition.face_encodings(rgb, boxes)

		for encoding in encodings:
			knownEncodings.append(encoding)
			knownNames.append(name)

	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(ENCODINGS_URL, "wb")
	f.write(pickle.dumps(data))
	f.close()
	print('[INFO] Done encoding faces!')
