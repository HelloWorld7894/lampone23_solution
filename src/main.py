#!/usr/bin/python3

#own imports
import analyze_playground, detect_playground, detect_robot, generate_path, load_frame, recognize_objects, send_solution

#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
import sys

def solve():
    img = load_frame.main()
    playground = detect_playground.main(img)
    robot = detect_robot.main(img)
    objects = recognize_objects.main(img,True)
    array = analyze_playground.main(playground, robot, objects)
    path = generate_path.main(array)
    #send_solution.main(path)



if __name__ == "__main__":
    print(sys.argv)
    solve()