#other imports
import cv2 as cv
import skimage
import numpy as np
import matplotlib.pyplot as plt
from log import log_true, log_false, log_warn
from colorama import Fore

def main(path = "", verbose = False):
    URL = "http://192.168.100.22/image/image.png"

    if verbose:
        if len(path) == 0:
            print(f"Fetching from {URL}")
        else:
            print(f"Reading from local resources: {path}")

    global errored, timeout
    errored = True
    timeout = 0

    if len(path) == 0:
        while errored:
            try:
                image = skimage.io.imread(URL, as_gray=False)
                errored = False
                log_true("fetch succeeded")
            except:
                if timeout == 5:
                    log_false("timeout limit exceeded, aborting")
                    exit(1)

                log_warn("fetch failed, repeating")
                errored = True
                timeout += 1
            
    else:
        image = skimage.io.imread(path, as_gray=False)
        if verbose:
            log_true("Image loaded succesfuly")

    if image.shape[2] == 4:
        image = image[:, :, :3]

    # Example intrinsic matrix (K)
    K = np.array([[800.0, 0.0, 960.0],
                [0.0, 600.0, 540.0],
                [0.0, 0.0, 1.0]])

    # Example distortion coefficients (D)
    D = np.array([0.03, -0.05, 0.002, 0.002])

    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, (image.shape[1], image.shape[0]), cv.CV_16SC2)
    image = cv.remap(image, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)

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

        X2 = x + w - margin - 20
        Y2 = y + h - margin

        return image[Y1:Y2, X1:X2]
    else:
        print("problem with finding contours, exiting program")
        exit(1)