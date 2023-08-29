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

def main(img, debug = False):
    rows = 4
    columns = 3
    imgs = []
    imgs_titles = []

    for i in range(3):
        img_chanel = img[:,:,i]

        #print(i)

        thresh = threshold_otsu(img_chanel)
        imgs.append(img_chanel < thresh)
        imgs_titles.append((f"{i} chanel {imgs[i].shape}"))
    

    imgs.append(img)
    imgs_titles.append(f"orichinal {img.shape}")


    img_and = (np.logical_and(imgs[0], imgs[2]))
    imgs.append(img_and)
    imgs_titles.append(f"and {img_and.shape}")
    
    img = (np.logical_xor(imgs[0], img_and))
    kernel = np.ones((10,10))
    img_clear = scipy.signal.convolve2d(img,kernel,boundary='symm')
    img_clear = img_clear > 40
    imgs.append(img_clear)
    imgs_titles.append(f"final {img_clear.shape}")

    img_xor = (np.logical_xor(imgs[1], imgs[2]))
    img_xor = (np.logical_xor(img_xor, img_and))
    img_xor = (np.logical_xor(img_xor, imgs[1]))
    imgs.append(img_xor)
    imgs_titles.append(f"and 1 2 {img_xor.shape}")

    img_xor = (np.logical_xor(imgs[0], imgs[2]))
    kernel = np.ones((10,10))
    img_xor = scipy.signal.convolve2d(img_xor,kernel,boundary='symm')
    imgs.append(img_xor)
    imgs_titles.append(f"mazaní {img_xor.shape}")

    img_xor = img_xor > 40
    imgs.append(img_xor)
    imgs_titles.append(f"kulatý obdelníky {img_xor.shape}")

    img_red = (np.logical_xor(img_xor, img_clear))
    kernel = np.ones((20,20))
    img_red = scipy.signal.convolve2d(img_red,kernel,boundary='symm')
    img_red = img_red > 40
    imgs.append(img_red)
    imgs_titles.append(f"kulatý {img_red.shape}")

    if debug:
        fig = plt.figure(figsize=(10, 7))
        for i in range(1,11):
            print(i)
            fig.add_subplot(rows, columns, i)
            plt.imshow(imgs[i-1], cmap="gray")
            plt.axis('off')
            plt.title(f"{imgs_titles[i-1]}")
        plt.show()
    """labeling"""
    insert = [img_clear,img_red]
    output = []

    for binary_array in insert:

        # Perform connected component labeling
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_array.astype(np.uint8))

        # Print the number of labels found
        #print("Number of labels:", num_labels)

        labels = []
        # Print statistics for each component
        for label in range(1, num_labels):
            leftmost = stats[label, cv2.CC_STAT_LEFT]
            topmost = stats[label, cv2.CC_STAT_TOP]
            width = stats[label, cv2.CC_STAT_WIDTH]
            height = stats[label, cv2.CC_STAT_HEIGHT]
            area = stats[label, cv2.CC_STAT_AREA]
            centroid_x, centroid_y = centroids[label]
            labels.append([leftmost,topmost,width,height,centroid_x,centroid_y])
            #print(f"Label {label}: Area={area}, Bounding Box=({leftmost}, {topmost}, {width}, {height}), Centroid=({centroid_x}, {centroid_y})")

        output.append(labels)

    print(output)
    

    #print(output)
    plt.show()



    return output


if __name__ == "__main__":
    main(skimage.io.imread("assets/image.png", as_gray=False)[250:760,650:1333,:])

