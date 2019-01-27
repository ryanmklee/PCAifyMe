import warnings

import cv2
warnings.filterwarnings("ignore")
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

face_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_eye.xml')

LEVEL_WEIGHTS = 5
REJECT_LEVELS = 1.3
sf = 0.20


def clean_individual(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, REJECT_LEVELS, LEVEL_WEIGHTS)
    if len(faces) != 0:
        x, y, w, h = faces[0]
        return img[y:y + h, x:x + w]


def read_image(path):
    img = cv2.imread(path)
    return cv2.resize(img, (0, 0), fx=sf, fy=sf)


def clean_input(json):
    paths = [('img')]
    X = []
    Y = ['labels']
    for path in paths:
        img = cv2.imread(path)
        X.append((clean_individual(img)))
    return X, Y


def train_mlp_model(X, y):
    # split into a training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    n_components = 100
    pca = PCA(n_components=n_components, whiten=True).fit(X_train)
    # apply PCA transformation
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    # Apply simple NN model
    clf = MLPClassifier(hidden_layer_sizes=(1024,), batch_size=256, verbose=True, early_stopping=True).fit(X_train_pca,
                                                                                                           y_train)
    return clf


def find_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, REJECT_LEVELS, LEVEL_WEIGHTS)
    print('Found {} faces!'.format(len(faces)))
    ret = []
    for (x, y, w, h) in faces:
        plt.figure()
        plt.imshow(cv2.cvtColor(img[y:y + h, x:x + w], cv2.COLOR_BGR2RGB))
        ret.append(gray[y:y + h, x:x + w])
    return ret


def verify_faces(img, labels):
    faces = find_faces(img)
    pass

