import cv2
import numpy as np
import os
import sys
from keras.layers import *
import tensorflow as tf

IMG_WIDTH = 30
IMG_HEIGHT = 30

IMG_KEYS = {
    0 : "speed limit (20km/h)", 1 : "speed limit (30km/h)", 2 : "speed limit (50km/h)",
    3 : "speed limit (60km/h)", 4 : "speed limit (70km/h)", 5 : "speed limit (80km/h)",
    6 : "end of speed limit", 7 : "speed limit (100km/h)", 8 : "speed limit (120km/h)",
    9 : "no passing", 10 : "no passing for vehicle", 11 : "right of way",
    12 : "priority road", 13 : "yield", 14 : "stop",
    15 : "no vehicles", 16 : "vehicles over 3.5m", 17 : "no entry",
    18 : "general caution", 19 : "dangerous curve to the left", 20 : "dangerous curve to the right",
    21 : "double curve", 22 : "bumpy road", 23 : "slippery road",
    24 : "road narrows", 25 : "road work", 26 : "traffic signals",
    27 : "pedestrians", 28 : "children crossing", 29 : "bicycles crossing",
    30 : "beware of ice/snow", 31 : "wild animals crossing", 32 : "end of all restrictions",
    33 : "turn right ahead", 34 : "turn left ahead", 35 : "ahead only",
    36 : "go straight or right", 37 : "go straight or left", 38 : "keep right",
    39 : "keep left", 40 : "roundabout mandatory", 41 : "end of no passing",
    42 : "end of no passing by"
}

def main():
    curr_path = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(curr_path, "model.h5")
    model = tf.keras.models.load_model(model_path)
    img = cv2.imread("00000_00000.ppm")
    resized = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    a = np.reshape(resized, (1,30,30,3))
    
    classification = model.predict(a).argmax()
    print(classification)
    print(IMG_KEYS[classification])

if __name__ == "__main__":
    main()