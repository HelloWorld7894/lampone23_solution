#own imports
import analyze_playground, detect_playground, detect_robot, generate_path, load_frame, recognize_objects, send_solution

#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt

def solve():
    load_frame.main()
    detect_playground.main()
    detect_robot.main()
    recognize_objects.main()
    analyze_playground.main()
    generate_path.main()
    send_solution.main()


if __name__ == "__main__":
    solve()
