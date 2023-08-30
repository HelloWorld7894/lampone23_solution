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
    if args.v:
        logging = True
        
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    
    img = load_frame.main()
    empty_image = load_frame.main("assets/image_empty.png")
    axs[0][0].imshow(img)
    axs[0][0].set_title('orichinal')
    playground, detect_playground_img = detect_playground.main(empty_image, logging)
    axs[0][1].imshow(detect_playground_img)
    axs[0][1].set_title('playground_detection')
    robot, robot_img = detect_robot.main(img, logging)
    axs[0][2].imshow(robot_img)
    axs[0][2].set_title('robot_detection')
    objects, objects_img = recognize_objects.main(img, logging)
    axs[1][0].imshow(objects_img)
    axs[1][0].set_title('Recognize_objects')
    array = analyze_playground.main(playground, robot, objects, logging)
    #path = generate_path.main(array, logging)
    #send_solution.main(path)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print(sys.argv)
    solve()