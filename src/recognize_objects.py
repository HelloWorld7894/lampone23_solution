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
    rows = 5
    columns = 3
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
    
    #adding img and label to list so when debug is True they can be shown
    imgs.append(img)
    imgs_titles.append(f"orichinal {img.shape}")

    """thresholding"""
    #separeting the robot and playground lines using binary AND function
    #is used to separet other elements
    img_and = (np.logical_and(imgs[0], imgs[2]))
    imgs.append(img_and)
    imgs_titles.append(f"and {img_and.shape}")
    
    #using xOR to separate blue squares
    img = (np.logical_xor(imgs[0], img_and))
    #removing artefacts using blur and hard coded thershold
    kernel = np.ones((10,10))
    img_clear = scipy.signal.convolve2d(img,kernel,boundary='symm')
    img_clear = img_clear > 40
    imgs.append(img_clear)
    imgs_titles.append(f"final {img_clear.shape}")

    #other weird way of geting red never used
    img_and12 = (np.logical_xor(imgs[1], imgs[2]))
    img_and12 = (np.logical_xor(img_and12, img_and))
    img_and12 = (np.logical_xor(img_and12, imgs[1]))
    kernel = np.ones((10,10))
    img_and12 = scipy.signal.convolve2d(img_and12,kernel,boundary='symm')
    imgs.append(img_and12)
    imgs_titles.append(f"and 1 2 {img_and12.shape}")

    #geting red and blue ones in two steps
    img_xor = (np.logical_xor(imgs[0], imgs[2]))
    kernel = np.ones((10,10))
    img_xor = scipy.signal.convolve2d(img_xor,kernel,boundary='symm')
    imgs.append(img_xor)
    imgs_titles.append(f"mazaní {img_xor.shape}")

    #the second step
    img_xor = img_xor > 40
    imgs.append(img_xor)
    imgs_titles.append(f"kulatý obdelníky {img_xor.shape}")

    #retarded way of geting red from red and blue dots and xORing blue dots
    img_red = (np.logical_xor(img_xor, img_clear))
    kernel = np.ones((20,20))
    img_red = scipy.signal.convolve2d(img_red,kernel,boundary='symm')
    img_red = img_red > 40
    imgs.append(img_red)
    imgs_titles.append(f"kulatý {img_red.shape}")

    #somehow working green detection but it is using too much blur and thresholding to get clear green
    # img_green = (np.logical_and(imgs[0], imgs[1]))
    # img_green = (np.logical_xor(img_green, imgs[2]))
    # img_green = (np.logical_xor(img_green, img_and12))
    img_green = (np.logical_xor(imgs[1], imgs[2]))
    kernel = np.ones((40,40))
    img_green = scipy.signal.convolve2d(img_green,kernel,boundary='symm')
    img_green = img_green > 400
    imgs.append(img_green)
    imgs_titles.append(f"green {img_green.shape}")

    #better recognition of red dots
    #geting playground without green using AND from channel 0 and 1
    #and xORing it with channel 1
    #img_red2 = np.logical_and(np.logical_and(imgs_inverted[[0], imgs[1]),imgs[2])
    img_red2 = (np.logical_and(imgs[0], imgs[1]))
    img_red2 = (np.logical_xor(img_red2, imgs[1]))
    kernel = np.ones((10,10))
    img_red2 = scipy.signal.convolve2d(img_red2,kernel,boundary='symm')
    img_red2 = img_red2 > 40
    imgs.append(img_red2)
    imgs_titles.append(f"red2 {img_red2.shape}")

    #better green using iverted green channel
    img_green2 = np.logical_and(np.logical_and(imgs[0], imgs_inverted[1]),imgs[2])
    kernel = np.ones((5,5))
    img_green2 = scipy.signal.convolve2d(img_green2,kernel,boundary='symm')
    img_green2 = img_green2 > 10
    imgs.append(img_green2)
    imgs_titles.append(f"green2 {img_green2.shape}")

    #better blue 
    img_blue2 = (np.logical_and(imgs[0], imgs_inverted[2]))
    kernel = np.ones((5,5))
    img_blue2 = scipy.signal.convolve2d(img_blue2,kernel,boundary='symm')
    img_blue2 = img_blue2 > 15
    imgs.append(img_blue2)
    imgs_titles.append(f"blue2 {img_blue2.shape}")
    
    """labeling"""
    insert = [img_blue2,img_red2,img_green2]
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
        fig = plt.figure(figsize=(10, 7))
        for i in range(1,len(imgs)+1):
            fig.add_subplot(rows, columns, i)
            plt.imshow(imgs[i-1], cmap="gray")
            plt.axis('off')
            plt.title(f"{imgs_titles[i-1]}")
        plt.show()

    #print(output)
    return output

if __name__ == "__main__":
    main(skimage.io.imread("assets/imagewgreen.png", as_gray=False)[270:760,650:1333,:],True)

