
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
    cropped_empty_img = empty_image[275:740, 675:1300]


    #simpling img

    imgray = cv.cvtColor(cropped_empty_img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)

    #geting contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Sorting

    Ysort = []
    Xsort = []
    SortedDots = []
    # Y sort
    for countor in contours[2:]:
        cordX = []
        cordY = []
        for dot in countor:
            cordX.append(dot[0][0])
            cordY.append(dot[0][1])
            
        Ysort.append([[min(cordX),min(cordY)],[max(cordX),max(cordY)]])
    Ysort.sort(key=lambda x: (x[0][1])) 
    # X sort and creating 8x8x2x2 4D aray lol this code is fucked shit but it sorting
    for i in range(8):
        if i == 0:
            Xsort = Ysort[:8]
        else:
            Xsort = Ysort[i*8:i*8+8]
        Xsort.sort(key=lambda x: (x[0][0]))
        SortedDots.append(Xsort)
    return SortedDots



if __name__ == "__main__":
    empty_image = cv.imread('assets/image_empty.png')
    
    SortedDots = main(empty_image)
    
    #cropped_empty_img = cv.rectangle(cropped_empty_img, SortedDots[7][0][0], SortedDots[7][0][1], (0,0,255), 3)
    
    #plt.imshow(cropped_empty_img)
    #plt.show()