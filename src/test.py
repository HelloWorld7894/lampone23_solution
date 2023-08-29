import cv2
import numpy as np

out_list = []

def main(image):
    image = (image * 255).astype(np.uint8)
    test_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
                        
    kernel3 = np.array([[0, -1,  0],
                        [-1,  5, -1],
                        [0, -1,  0]])
    image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel3)

    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
    i = 0
    
    # list for storing names of shapes
    for contour in contours:
    
        # here we are ignoring first counter because 
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue
    
        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.05 * cv2.arcLength(contour, True), True)
        
        # using drawContours() function
        cv2.drawContours(test_img, [approx], 0, (0, 0, 255), 5)
    
        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
    
        # putting shape name at center of each shape
        if len(approx) == 3: #cls 1
            cv2.putText(test_img, 'trojuhelnik', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
        elif len(approx) == 4:
            cv2.putText(test_img, 'ctverec', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        elif len(approx) == 5:
            cv2.putText(test_img, 'hvezda', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(test_img, 'kruh', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
    cv2.imshow("test", test_img)
    cv2.imshow("test2", image)
    cv2.waitKey(0)