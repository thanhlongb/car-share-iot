from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

RECOGNIZER_URL = 'facial_recognition/output/recognizer.pickle'
LABEL_ENCODER_URL = 'facial_recognition/output/le.pickle'

def train_model(encodings_data):
    # print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(encodings_data["names"])

    # print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(encodings_data["encodings"], labels)

    f = open(RECOGNIZER_URL, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()
    
    f = open(LABEL_ENCODER_URL, "wb")
    f.write(pickle.dumps(le))
    f.close()