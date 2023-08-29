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
    rows = 2
    columns = 4
    imgs = []
    imgs_inverted = []
    imgs_titles = []


    """channeling"""
    for i in range(3):
        #create binary arrays of each channel using otsu threshold
        img_chanel = img[:,:,i]
        thresh = threshold_otsu(img_chanel)
        #add each channel to list so they can be shown later
        imgs.append(img_chanel < thresh)
        imgs_inverted.append(img_chanel > thresh)
        imgs_titles.append((f"{i} chanel {imgs[i].shape}"))
    
    #adding img and label to lists so when debug is True they can be displayed
    imgs.append(img)
    imgs_titles.append(f"orichinal {img.shape}")

    """thresholding"""
    #better recognition of red dots
    #geting playground without green using AND from channel 0 and 1
    #and xORing it with channel 1
    img_red = (np.logical_and(imgs[0], imgs[1]))
    img_red = (np.logical_xor(img_red, imgs[1]))
    kernel = np.ones((10,10))
    img_red = scipy.signal.convolve2d(img_red,kernel,boundary='symm')
    img_red = img_red > 40
    imgs.append(img_red)
    imgs_titles.append(f"red {img_red.shape}")

    #better green using iverted green channel
    img_green = np.logical_and(np.logical_and(imgs[0], imgs_inverted[1]),imgs[2])
    kernel = np.ones((5,5))
    img_green = scipy.signal.convolve2d(img_green,kernel,boundary='symm')
    img_green = img_green > 10
    imgs.append(img_green)
    imgs_titles.append(f"green {img_green.shape}")

    #better blue 
    img_blue = (np.logical_and(imgs[0], imgs_inverted[2]))
    kernel = np.ones((5,5))
    img_blue = scipy.signal.convolve2d(img_blue,kernel,boundary='symm')
    img_blue = img_blue > 15
    imgs.append(img_blue)
    imgs_titles.append(f"blue {img_blue.shape}")
    
    """labeling"""
    insert = [img_blue,img_red,img_green]
    output = []

    for binary_array in insert:
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_array.astype(np.uint8))
        labels = []
        for label in range(1, num_labels):
            leftmost = stats[label, cv2.CC_STAT_LEFT]
            topmost = stats[label, cv2.CC_STAT_TOP]
            width = stats[label, cv2.CC_STAT_WIDTH]
            height = stats[label, cv2.CC_STAT_HEIGHT]
            area = stats[label, cv2.CC_STAT_AREA]
            centroid_x, centroid_y = centroids[label]
            labels.append([leftmost,topmost,width,height,centroid_x,centroid_y])
            print(f"Label {label}: Area={area}, Bounding Box=({leftmost}, {topmost}, {width}, {height}), Centroid=({centroid_x}, {centroid_y})")
        print()
        output.append(labels)


    """showing subplots for debug and development"""
    if debug:
        fig = plt.figure(figsize=(13, 6))
        for i in range(1,len(imgs)+1):
            fig.add_subplot(rows, columns, i)
            plt.imshow(imgs[i-1], cmap="gray")
            plt.axis('off')
            plt.title(f"{imgs_titles[i-1]}")
        plt.show()

    #print(output)
    return output

if __name__ == "__main__":
    urls = [
        "assets/imagewgreen.png",
        "assets/image.png",
        "assets/image_empty.png"
    ]
    for i in urls:
        main(skimage.io.imread(i, as_gray=False)[270:760,650:1333,:],True)

