import argparse
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from matplotlib import pyplot as plt










# images
#main image
image = cv.imread('image_empty.png')


imagerobot = cv.imread('image.png')


# resize img
cropped_imagerobot = imagerobot[275:740, 675:1300]
cropped_img = image[275:740, 675:1300]


#simpling img

imgray = cv.cvtColor(cropped_img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, t)


#geting contours

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)





# visualization
cv.drawContours(cropped_imagerobot, contours, -1, (0,255,0), 1)
print(contours[5])
plt.imshow(cropped_imagerobot)
plt.show()