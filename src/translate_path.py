import cv2
import skimage
import numpy as np
import sys
import argparse
import os
from termcolor import colored

def main(heading, path_array, verbose = False):
    curr_heading = heading
    out_string = ""
    for i, curr_coord in enumerate(path_array):
        if i + 1 == len(path_array):
            break

        d_y = curr_coord[0] - path_array[i+1][0] 
        d_x = curr_coord[1] - path_array[i+1][1]

        if d_y == 1: #up
            if curr_heading == "N":
                out_string += "F"
            elif curr_heading == "W":
                out_string += "R"
            elif curr_heading == "E":
                out_string += "L"

            curr_heading = "N"

        elif d_y == -1: #down
            if curr_heading == "S":
                out_string += "F"
            elif curr_heading == "W":
                out_string += "L"
            elif curr_heading == "E":
                out_string += "R"

            curr_heading = "S"

        if d_x == 1: #left
            if curr_heading == "N":
                out_string += "L"
            elif curr_heading == "W":
                out_string += "F"
            elif curr_heading == "S":
                out_string += "R"

            curr_heading = "W"

        elif d_x == -1: #right
            if curr_heading == "N":
                out_string += "R"
            elif curr_heading == "E":
                out_string += "F"
            elif curr_heading == "S":
                out_string += "L"

            curr_heading = "E"

    if verbose:
        print(colored("generated robot commands!", "green"))
        print("commands: " + out_string)
    return out_string

if __name__ == "__main__":
    path_array = [(7, 1), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (2, 5), (1, 5), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3)]
    heading = "W"
    main(heading, path_array, verbose=False)