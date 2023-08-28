#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt

def main(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()

    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    return cv2.aruco.drawDetectedMarkers(image, corners, ids) # TODO:  return just angle and rentangle 2 points 


if __name__ == "__main__":
    image = cv2.imread('assets/image.png')
    image_with_markers = main(image)
    cv2.imshow('Detected Markers', image_with_markers)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
