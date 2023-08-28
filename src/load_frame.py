#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt

def main():
    URL = "http://192.168.100.22/image/image.png"
    return skimage.io.imread(URL, as_gray=False)