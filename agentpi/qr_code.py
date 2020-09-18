from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2

def get_QR_encryption():
	print("[INFO] starting video stream...")
	vs = VideoStream(src = 0).start()
	time.sleep(2.0)
	tstart = time.time()
	while True:
		tend = time.time()
		if tend - tstart > 20:
			vs.stop()
			return ''

		frame = vs.read()
		frame = imutils.resize(frame, width = 400)

		barcodes = pyzbar.decode(frame)
		for barcode in barcodes:
			barcodeData = barcode.data.decode("utf-8")
			vs.stop()
			return barcodeData
		