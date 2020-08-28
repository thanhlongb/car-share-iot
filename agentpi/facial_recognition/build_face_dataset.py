from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True)
ap.add_argument("-m", "--model", required=True)
ap.add_argument("-c", "--confidence", type=float, default=0.5)
ap.add_argument("-o", "--output", required=True)
args = vars(ap.parse_args())

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 0

while True:
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width=400)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))
 
    net.setInput(blob)
    detections = net.forward()
 
    for i in range(0, detections.shape[2]):
	    confidence = detections[0, 0, i, 2]

	    if confidence < args["confidence"]:
		    continue

	    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
	    (startX, startY, endX, endY) = box.astype("int")
 
	    text = "{:.2f}%".format(confidence * 100)
	    y = startY - 10 if startY - 10 > 10 else startY + 10
	    cv2.rectangle(frame, (startX, startY), (endX, endY),
	    	(0, 0, 255), 2)
	    cv2.putText(frame, text, (startX, y),
	    	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("k"):
    	p = os.path.sep.join([args["output"], "{}.png".format(
    		str(total).zfill(5))])
    	cv2.imwrite(p, orig)
    	total += 1

    elif key == ord("q"):
    	break

print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()