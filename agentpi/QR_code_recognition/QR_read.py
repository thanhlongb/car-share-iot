from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2

print("[INFO] starting video stream...")
vs = VideoStream(src = 0).start()
time.sleep(2.0)

found = set()

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width = 400)

	barcodes = pyzbar.decode(frame)

	for barcode in barcodes:
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		if barcodeData not in found:
			print("[FOUND] Type: {}, Data: {}".format(barcodeType, barcodeData))
			found.add(barcodeData)
	
	time.sleep(1)

print("[INFO] cleaning up...")
vs.stop()