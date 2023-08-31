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
from log import log_true, log_false, log_warn
import json
from visualization import visualization as visual

from matplotlib.colors import ListedColormap
import matplotlib
matplotlib.use("TkAgg")

PATH = os.getcwd()

parser = argparse.ArgumentParser(
                    prog='main',
                    description='xd',
                    epilog='Text at the bottom of help')
parser.add_argument('--v', '--verbose', action='store_true', help='Enable verbose mode')

if "src" in PATH:
    PATH = PATH.replace("/src", "")

#loading json data
json_data = json.load(open(PATH + "/settings.json"))

log_true("loaded JSON file")
if json_data["verbose"]:
    logging = True
else:
    logging = False

if json_data["testing"]:
    send = True
else:
    send = False

def solve():
    #some logging stuff
    global logging
    args = parser.parse_args()
    
    if args.v:
        logging = True
        print("Logging set to true")

    if json_data["resource"] == "":
        img = load_frame.main(verbose=logging)
    else:
        img = load_frame.main(PATH + json_data["resource"], verbose=logging)
    empty_image = load_frame.main(PATH + "/assets/image_empty.png")

    playground, detect_playground_img = detect_playground.main(empty_image, logging)
    img_for_robot = img.copy()
    robot, robotImg = detect_robot.main(img_for_robot, logging)
    objects, objects_img = recognize_objects.main(img, logging)
    array = analyze_playground.main(playground, robot, objects, logging)
        
    path = generate_path.main(array, logging)
    if not send:
        send_solution.main(path)
    if True:
        visual(img,detect_playground_img,robotImg,objects_img,array,path)

if __name__ == "__main__":
    solve()