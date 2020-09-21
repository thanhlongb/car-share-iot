import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

RECOGNIZER_PATH = 'facial_recognition/output/recognizer.pickle'
LABEL_ENCODER_PATH = 'facial_recognition/output/le.pickle'

def train_model(encodings_data):
    """
	Train the SVM model using face encodings got from
    MP

    :args: encoding_data : encodings.pickle got updated from MP

    :return: - username if sucessfully authenticated.
             - empty string otherwise.
    """
    # print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(encodings_data["names"])

    # print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(encodings_data["encodings"], labels)

    f = open(RECOGNIZER_PATH, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    f = open(LABEL_ENCODER_PATH, "wb")
    f.write(pickle.dumps(le))
    f.close()
