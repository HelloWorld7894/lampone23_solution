#this is just a testing file for testing camera intrinsic matrix

import load_frame
import cv2
import numpy as np
import skimage

img = skimage.io.imread("./assets/image_all.png", as_gray=False)

# Example intrinsic matrix (K)
K = np.array([[800.0, 0.0, 960.0],
              [0.0, 600.0, 540.0],
              [0.0, 0.0, 1.0]])

# Example distortion coefficients (D)
D = np.array([0.03, -0.05, 0.002, 0.002])

map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, (img.shape[1], img.shape[0]), cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

cv2.imshow("img", img)
cv2.imshow("img2", undistorted_img)
cv2.waitKey(0)