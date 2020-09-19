import time
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils

def get_QR_encryption():
	"""
	Detect and get decoded message from QR code

    :return: decoded message
    """
	print("[INFO] starting camera...")
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
		