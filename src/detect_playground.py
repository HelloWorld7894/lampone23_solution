
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg") #for linux users
import numpy as np
import load_frame
from log import log_true, log_false, log_warn

import math
from collections import defaultdict


def segment_by_angle_kmeans(lines, k=2, **kwargs):
    """Groups lines based on angle with k-means.

    Uses k-means on the coordinates of the angle on the unit circle 
    to segment `k` angles inside `lines`.
    """

    # Define criteria = (type, max_iter, epsilon)
    default_criteria_type = cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER
    criteria = kwargs.get('criteria', (default_criteria_type, 10, 1.0))
    flags = kwargs.get('flags', cv.KMEANS_RANDOM_CENTERS)
    attempts = kwargs.get('attempts', 10)

    # returns angles in [0, pi] in radians
    angles = np.array([line[0][1] for line in lines])
    # multiply the angles by two and find coordinates of that angle
    pts = np.array([[np.cos(2*angle), np.sin(2*angle)]
                    for angle in angles], dtype=np.float32)

    # run kmeans on the coords
    labels, centers = cv.kmeans(pts, k, None, criteria, attempts, flags)[1:]
    labels = labels.reshape(-1)  # transpose to row vec

    # segment lines based on their kmeans label
    segmented = defaultdict(list)
    for i, line in enumerate(lines):
        segmented[labels[i]].append(line)
    segmented = list(segmented.values())
    return segmented

def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]


def segmented_intersections(lines):
    """Finds the intersections between groups of lines."""

    intersections = []
    for i, group in enumerate(lines[:-1]):
        for next_group in lines[i+1:]:
            for line1 in group:
                for line2 in next_group:
                    intersections.append(intersection(line1, line2)) 

    return intersections


def main(empty_image, verbose = False):
    
    #simpling img

    imgray = cv.cvtColor(empty_image, cv.COLOR_BGR2GRAY)
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
    # X sort and creating 8x8x2x2 4D aray but it sorting
    for i in range(8):
        if i == 0:
            Xsort = Ysort[:8]
        else:
            Xsort = Ysort[i*8:i*8+8]
        Xsort.sort(key=lambda x: (x[0][0]))
        SortedDots.append(Xsort)

    for x in range(8):
        for y in range(8):
            return_img = cv.rectangle(empty_image, SortedDots[y][x][0], SortedDots[y][x][1], (0,0,255), 3)

    if verbose:
        log_true("background detected")
    return SortedDots, return_img 

#much better version using intersections and HoughLines, TODO: output type still not same as main()
def main2(image, verbose = False):
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(7,7),0)
    
    thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
    kernel = np.ones((5,5),np.float32)/25
    thresh_blur = cv.filter2D(thresh,-1,kernel)
    canny = cv.Canny(thresh_blur, 50, 150)

    test_image = np.zeros(image.shape)
    out_image = np.zeros(image.shape[:2])

    lines = cv.HoughLines(canny, 1, np.pi / 180, 150, None, 0, 0)

    segmented = segment_by_angle_kmeans(lines)
    intersections = segmented_intersections(segmented)
 
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(test_image, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    
    for intersec in intersections:
        #cv.drawMarker(test_image, intersec[0], (0, 255, 0), cv.MARKER_CROSS, 15, 5)
        cv.circle(out_image, intersec[0], 7, (255, 255, 255), -1)

    out_image = out_image.astype('uint8')
    contours, hierarchy = cv.findContours(out_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(test_image, contours, -1, (0,255,0), 3)

    centers = []

    for c in contours:
        # compute the center of the contour
        M = cv.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # draw the contour and center of the shape on the image
        cv.circle(test_image, (cX, cY), 7, (255, 255, 255), -1)
        cv.putText(test_image, "center", (cX - 20, cY - 20),
            cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        centers.append([cX, cY])

    cv.imshow("img", thresh)
    cv.imshow("lines", test_image)
    cv.imshow("out", out_image)
    cv.waitKey(0)

    return centers, test_image

if __name__ == "__main__":
    image = load_frame.main("./assets/image_all.png")
