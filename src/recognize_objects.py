#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import load_frame
from skimage.filters import threshold_otsu
import scipy.signal
import termcolor

import recognize_same_color as dan

def main(img, verbose = False):
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
    # img_red = (np.logical_and(imgs[0], imgs[1]))
    # img_red = (np.logical_xor(img_red, imgs[1]))
    img_red = np.logical_and(np.logical_and(imgs_inverted[0], imgs[1]),imgs[2])
    kernel = np.ones((5,5))
    img_red = scipy.signal.convolve2d(img_red,kernel,boundary='symm')
    img_red = img_red > 20
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
    insert = [img_blue,img_green,img_red]
    output = []

    stars = dan.main(img_red)
    print(stars)

    for i, binary_array in enumerate(insert):
        num_labels, label, stats, centroids = cv2.connectedComponentsWithStats(binary_array.astype(np.uint8))
        labels = []
        star_label = []
        for label in range(1, num_labels):
            leftmost = stats[label, cv2.CC_STAT_LEFT]
            topmost = stats[label, cv2.CC_STAT_TOP]
            width = stats[label, cv2.CC_STAT_WIDTH]
            height = stats[label, cv2.CC_STAT_HEIGHT]
            area = stats[label, cv2.CC_STAT_AREA]
            centroid_x, centroid_y = centroids[label]

            isntstar = True
            for star in stars:
                if star[0] > leftmost and star[0] < leftmost + width and star[1] > topmost and star[1] < topmost + height and i == 2 and area > 200:
                    star_label.append([round(centroid_x),round(centroid_y),leftmost,topmost,width,height])
                    isntstar = False
            if area > 200 and isntstar:
                labels.append([round(centroid_x),round(centroid_y),leftmost,topmost,width,height])
                if verbose:
                    print(f"Label {label}: Area={area}, Bounding Box=({leftmost}, {topmost}, {width}, {height}), Centroid=({centroid_x}, {centroid_y})")
        print()
        output.append(labels)
    output.append(star_label)


    """showing subplots for debug and development"""
    if verbose:
        for i in output:
            print("[", end="")
            for j in i:
                print(j)
            print(len(i))
            print("]")
            print()

        fig = plt.figure(figsize=(13, 6))
        for i in range(1,len(imgs)+1):
            fig.add_subplot(rows, columns, i)
            plt.imshow(imgs[i-1], cmap="gray")
            plt.axis('off')
            plt.title(f"{imgs_titles[i-1]}")
        plt.show()

    return output, visualisation(img,output)

def visualisation(img, x, bgr = False):
    bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    objects = ["ctverecek","ctverecek","ctverecek","hvezdicka"]
    barvicky = [(255,0,0),(0,255,0),(0,0,255),(0,0,255)]
    thickness = 2

    for i in range(len(x)):
        for j in x[i]:
            cv2.rectangle(bgr_img, (j[2], j[3]),(j[2]+j[4], j[3]+j[5]), barvicky[i], thickness)
            text_position = (j[2], j[3]+j[5]+10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1/2
            cv2.putText(bgr_img, objects[i], text_position, font, font_scale, barvicky[i], 1)
    if bgr:
        return bgr_img
    else:
        return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

if __name__ == "__main__":
    # urls = [
    #     "assets/image_all.png"
    #     "assets/imagewgreen.png",
    #     "assets/image.png",
    #     "assets/image_empty.png"
    # ]
    # for i in urls:
    #     main(skimage.io.imread(i, as_gray=False)[270:760,650:1333,:],True)
    
    img = load_frame.main()
    x, y = main(img,False)

    img_out = visualisation(img,x,True)

    cv2.imshow('bleueh',img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

