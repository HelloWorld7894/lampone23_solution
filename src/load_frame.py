#other imports
import cv2 as cv
import skimage
import numpy as np
import matplotlib.pyplot as plt
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

    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

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
