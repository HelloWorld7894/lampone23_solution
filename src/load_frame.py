#other imports
import cv2 as cv
import skimage
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
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
                print(colored("fetch succeeded", "green"))
            except:
                if timeout == 5:
                    print(colored("timeout limit exceeded, aborting", "red"))
                    exit(1)

                print(colored("fetch failed, repeating", "yellow"))
                errored = True
                timeout += 1
            
    else:
        image = skimage.io.imread(path, as_gray=False)
        if verbose:
            print(colored("Image loaded succesfuly", "green"))

    if image.shape[2] == 4:
        image = image[:, :, :3]

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