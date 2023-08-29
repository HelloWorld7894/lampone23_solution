
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg") #for linux users
import numpy as np

def main(empty_image):

    # images
    #main image


    # resize img
    #cropped_empty_img = empty_image[275:740, 675:1300]


    imgray = cv.cvtColor(empty_image, cv.COLOR_BGR2GRAY)
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

        # draw the biggest contour (c) in green
        cv.rectangle(empty_image,(X1, Y1), (X2, Y2), (0, 255, 0), 2)

    cv.imshow("img", empty_image)
    cv.waitKey(0)


if __name__ == "__main__":
    empty_image = cv.imread('assets/image_empty.png')
    
    SortedDots = main(empty_image)
    
    #cropped_empty_img = cv.rectangle(cropped_empty_img, SortedDots[7][0][0], SortedDots[7][0][1], (0,0,255), 3)
    
    #plt.imshow(cropped_empty_img)
    #plt.show()