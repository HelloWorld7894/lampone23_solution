import cv2
import skimage
import numpy as np
import sys
import argparse
import os
from log import log_true, log_false, log_warn

def main(heading, path_array, verbose = False):
    print(path_array)

    curr_heading = heading
    curr_pos = path_array[0]
    out_string = ""
    append = ""
    for i, curr_coord in enumerate(path_array):
        if i + 1 == len(path_array):
            break

        d_y = curr_coord[0] - path_array[i+1][0] 
        d_x = curr_coord[1] - path_array[i+1][1]

        if (curr_pos[0] == curr_coord[0] and curr_pos[1] == curr_coord[1]):
            #robot just needs to rotate
            append = ""
        else:
            append = "F"

        if d_y == 1: #up
            if curr_heading == "N":
                out_string += "F"
            elif curr_heading == "W":
                out_string += append + "R"
            elif curr_heading == "E":
                out_string += append + "L"
            elif curr_heading == "S":
                out_string += append + "LL"

            curr_heading = "N"

        elif d_y == -1: #down
            if curr_heading == "S":
                out_string += "F"
            elif curr_heading == "W":
                out_string += append + "L"
            elif curr_heading == "E":
                out_string += append + "R"
            elif curr_heading == "N":
                out_string += append + "LL"

            curr_heading = "S"

        if d_x == 1: #left
            if curr_heading == "N":
                out_string += append + "L"
            elif curr_heading == "W":
                out_string += "F"
            elif curr_heading == "S":
                out_string += append + "R"
            elif curr_heading == "E":
                out_string += append + "LL"

            curr_heading = "W"

        elif d_x == -1: #right
            if curr_heading == "N":
                out_string += append + "R"
            elif curr_heading == "E":
                out_string += "F"
            elif curr_heading == "S":
                out_string += append + "L"
            elif curr_heading == "W":
                out_string += append + "LL"

            curr_heading = "E"
        
        curr_pos = curr_coord

        if i == 0:
            #we need to delete the first command because of the shift
            out_string = out_string[1:]

    if verbose:
        log_true("generated robot commands")
        print("commands: " + out_string)

    out_string += "F"

    return out_string

if __name__ == "__main__":
    path_array = [(7, 1), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (2, 5), (1, 5), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3)]
    heading = "W"
    main(heading, path_array, verbose=False)