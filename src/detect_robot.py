import cv2
import cv2.aruco as aruco

image = cv2.imread('image.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

image_with_markers = aruco.drawDetectedMarkers(image, corners, ids)

cv2.imshow('Detected Markers', image_with_markers)
cv2.waitKey(0)
cv2.destroyAllWindows()
