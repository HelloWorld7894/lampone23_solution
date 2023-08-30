#!/usr/bin/python3

#own imports
import analyze_playground, detect_playground, detect_robot, generate_path, load_frame, recognize_objects, send_solution

#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
import os

PATH = os.getcwd()

parser = argparse.ArgumentParser(
                    prog='main',
                    description='xd',
                    epilog='Text at the bottom of help')
parser.add_argument('--v', '--verbose', action='store_true', help='Enable verbose mode')
logging = False

if "src" in PATH:
    PATH = PATH.replace("/src", "")


def solve():
    #some logging stuff
    global logging
    args = parser.parse_args()
    print(args.v)

    if args.v:
        logging = True

    img = load_frame.main(PATH + "/assets/image_all.png")
    img_log = img.copy()

    playground = detect_playground.main(img, logging)
    robot = detect_robot.main(img, logging)
    objects = recognize_objects.main(img, logging)
    array = analyze_playground.main(playground, robot, objects, logging)
    path = generate_path.main(array, logging)
    
    cv2.imshow("logging", img)
    cv2.waitKey(0)
    #send_solution.main(path)



if __name__ == "__main__":
    print(sys.argv)
    solve()