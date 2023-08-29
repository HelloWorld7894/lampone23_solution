#other imports
import cv2 as cv
import skimage
import numpy as np
import matplotlib.pyplot as plt

def main(path = ""):

    if len(path) == 0:
        URL = "http://192.168.100.22/image/image.png"
        image = skimage.io.imread(URL, as_gray=False)
    else:
        image = skimage.io.imread(path, as_gray=False)

    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)

    #geting contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        c = max(contours, key = cv.contourArea)
        x, y, w, h = cv.boundingRect(c)
        margin = 35

        X1 = x + margin
        Y1 = y + margin

        X2 = x + w - margin
        Y2 = y + h - margin

        return image[Y1:Y2, X1:X2]
    else:
        print("problem with finding contours, exiting program")
        exit(1)