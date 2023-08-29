#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import time
from skimage.filters import threshold_otsu
import scipy.signal

import test

def main(img):
    fig = plt.figure(figsize=(10, 7))
    rows = 3
    columns = 3

    fig.add_subplot(rows, columns, 4)

    plt.imshow(img, cmap="gray")
    plt.axis('off')
    plt.title("orichinal")

    img_color = [0,0,0]
    
    for i in range(3):
        img_chanel = img[:,:,i]

        print(i)

        thresh = threshold_otsu(img_chanel)
        img_color[i] = img_chanel < thresh

        fig.add_subplot(rows, columns, i+1)

        plt.imshow(img_color[i], cmap="gray")
        plt.axis('off')
        plt.title(f"{i} chanel")
    

    fig.add_subplot(rows, columns, 5)

    img_xor = (np.logical_xor(img_color[1], img_color[2]))

    img_xor = (np.logical_xor(img_xor, img_color[0]))

    plt.imshow(img_xor, cmap="gray")
    plt.axis('off')
    plt.title("and 1 2")


    fig.add_subplot(rows, columns, 6)

    img_and = (np.logical_and(img_color[0], img_color[2]))

    

    plt.imshow(img_and, cmap="gray")
    plt.axis('off')
    plt.title("and")


    fig.add_subplot(rows, columns, 7)

    img = (np.logical_xor(img_color[0], img_and))
    kernel = np.ones((10,10))
    img_clear = scipy.signal.convolve2d(img,kernel,boundary='symm')
    img_clear = img_clear > 40
    plt.imshow(img_clear,cmap = "gray")

    plt.imshow(img_clear, cmap="gray")
    plt.axis('off')
    plt.title("final")
    

    """labeling"""

    binary_array = img_clear

    # Perform connected component labeling
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_array.astype(np.uint8))

    # Print the number of labels found
    print("Number of labels:", num_labels)

    # Print statistics for each component
    for label in range(1, num_labels):
        leftmost = stats[label, cv2.CC_STAT_LEFT]
        topmost = stats[label, cv2.CC_STAT_TOP]
        width = stats[label, cv2.CC_STAT_WIDTH]
        height = stats[label, cv2.CC_STAT_HEIGHT]
        area = stats[label, cv2.CC_STAT_AREA]
        centroid_x, centroid_y = centroids[label]
        print(f"Label {label}: Area={area}, Bounding Box=({leftmost}, {topmost}, {width}, {height}), Centroid=({centroid_x}, {centroid_y})")


    plt.show()

    test.main(binary_array)

    pass

if __name__ == "__main__":
    main(skimage.io.imread("assets/image.png", as_gray=False)[250:760,650:1333,:])

