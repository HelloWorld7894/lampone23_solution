#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import time
from skimage.filters import threshold_otsu
import scipy.signal


def main(URL):

    fig = plt.figure(figsize=(10, 7))
    rows = 3
    columns = 2

    img_color = [0,0,0]
    

    for i in range(3):
        img = skimage.io.imread(URL, as_gray=False)
        img_crop = img[250:760,650:1333,i]

        print(i)
        
        thresh = threshold_otsu(img_crop)
        img_color[i] = img_crop < thresh

        fig.add_subplot(rows, columns, i+1)

        # plt.imshow(img_crop, cmap="gray")
        # plt.colorbar()
        plt.imshow(img_color[i], cmap="gray")
        #plt.colorbar()
        plt.axis('off')
        plt.title(f"{i} chanel")
    

    fig.add_subplot(rows, columns, 4)

    img_xor = (np.logical_xor(img_color[0], img_color[2]))

    plt.imshow(img_xor, cmap="gray")
    plt.axis('off')
    plt.title("xor")


    fig.add_subplot(rows, columns, 5)

    img_and = (np.logical_and(img_color[0], img_color[2]))

    plt.imshow(img_and, cmap="gray")
    plt.axis('off')
    plt.title("and")


    fig.add_subplot(rows, columns, 6)

    img = (np.logical_xor(img_color[0], img_and))
    kernel = np.ones((10,10))
    img = scipy.signal.convolve2d(img,kernel,boundary='symm')
    img = img > 15
    plt.imshow(img,cmap = "gray")

    plt.imshow(img, cmap="gray")
    plt.axis('off')
    plt.title("final")
    print(img)
    plt.show()


    # Find connected components in the binary image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)

    # Create a random color map for visualization
    color_map = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)

    # Set background label to black (optional)
    color_map[0] = [0, 0, 0]

    # Create a colored label image
    colored_labels = color_map[labels]

    # Display the original image and the labeled image
    cv2.imshow('Original Image', img)
    cv2.imshow('Labeled Image', colored_labels)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    pass

if __name__ == "__main__":
    main("assets/image.png")

