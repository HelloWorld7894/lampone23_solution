#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import math
from termcolor import colored

timeout = 0

def main(image, verbose = False):
    bot_not_found = True
    while bot_not_found:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)
        if len(corners) == 0:
            if timeout == 5:
                if verbose:
                    print(colored("timeout limit exceeded, aborting", "red"))
                exit(1)
            if verbose:
                print(colored("did not found the robot, repeating...", "yellow"))
            timeout += 1
        else:
            if verbose:
                print(colored("found the robot!", "green"))
            bot_not_found = False

    corners = corners[0][0].astype(np.int32)
    
    angle = ""

    x1 = corners[0][0]
    y1 = corners[0][1]

    x2 = corners[1][0]
    y2 = corners[1][1]

    d_x = x1 - x2
    d_y = y1 - y2

    if math.floor(d_x / image.shape[1]) == 0:
        #right or left
        if d_y > 0:
            angle = "L"
        else:
            angle = "R"
    if math.floor(d_y / image.shape[0]) == 0:
        #up or down
        if d_x > 0:
            angle = "U"
        else:
            angle = "D"

    if verbose:
        print("Robot parameters are:")
        print("Coordinations: ", corners)
        print("Heading: ", angle)

    return [corners, angle]


# just test to see
if __name__ == "__main__":
    image = cv2.imread('assets/image.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejected = detector.detectMarkers(gray)
    print(corners[0][0])


    image_with_markers = cv2.aruco.drawDetectedMarkers(image, corners, ids)
    cv2.imshow('Detected Markers', image_with_markers)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
