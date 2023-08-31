import load_frame
import cv2
import numpy as np

img = load_frame.main("./assets/image_all.png")

print(img.shape)

# Example intrinsic matrix (K)
K = np.array([[650.0, 0.0, 235.0],
              [0.0, 550.0, 330.0],
              [0.0, 0.0, 1.0]])

# Example distortion coefficients (D)
D = np.array([0.01, -0.03, 0.001, 0.002])

map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, (648, 477), cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

cv2.imshow("img", img)
cv2.imshow("img2", undistorted_img)
cv2.waitKey(0)