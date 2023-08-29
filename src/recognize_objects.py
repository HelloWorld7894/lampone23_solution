#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import time
from skimage.filters import threshold_otsu

def main(URL):

    

    # print(img_crop.shape)

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

    #img = img_color[0]  ^ img_color[2]
    img_xor = (np.logical_xor(img_color[0], img_color[2]))

    plt.imshow(img_xor, cmap="gray")
    plt.axis('off')
    plt.title("xor")


    fig.add_subplot(rows, columns, 5)

    #img = img_color[0]  ^ img_color[2]
    img_and = (np.logical_and(img_color[0], img_color[2]))

    plt.imshow(img_and, cmap="gray")
    plt.axis('off')
    plt.title("and")


    fig.add_subplot(rows, columns, 6)

    #img = img_color[0]  ^ img_color[2]
    img = (np.logical_xor(img_color[0], img_and))

    plt.imshow(img, cmap="gray")
    plt.axis('off')
    plt.title("final")

    plt.show()

    pass

main("assets/image.png")

#x630 y250
#x1333 y760
