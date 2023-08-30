#other imports
import cv2
import skimage
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored

def rectangles_intersect(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if x1 > x2 + w2 or x2 > x1 + w1:
        return False

    if y1 > y2 + h2 or y2 > y1 + h1:
        return False

    return True

def main(playground,robot,objects, verbose = False):
    BestArray = [np.zeros((len(playground),len(playground[0])))]
    for Y in range(len(playground)):
        for X in range(len(playground[0])):
            #Get Ground
            groundX = playground[Y][X][0][0]
            groundY = playground[Y][X][0][1]
            groundW = playground[Y][X][1][0]-playground[Y][X][0][0]
            groundH = playground[Y][X][1][1]-playground[Y][X][0][1]
            #Get Robot
            robotX = robot[0][1][0]
            robotY = robot[0][1][1]
            robotW = robot[0][3][0]-robot[0][1][0]
            robotH = robot[0][3][1]-robot[0][1][1]
            if rectangles_intersect((groundX,groundY,groundW,groundH), (robotX,robotY,robotW,robotH)):
                BestArray[0][Y][X] = 1 #start
                print("robot cords: ", X,Y)
            #get Rentangle
            if not objects == None:
                for rect in objects[1]:
                    if rectangles_intersect((groundX,groundY,groundW,groundH),(rect[0],rect[1],10,10)):
                        BestArray[0][Y][X] = 2 #Blue rects
            if not objects == None:
                for rect in objects[0]:
                    if rectangles_intersect((groundX,groundY,groundW,groundH),(rect[0],rect[1],10,10)):
                        BestArray[0][Y][X] = 3 #Blue rects 
            if not objects == None:
                for rect in objects[2]:
                    if rectangles_intersect((groundX,groundY,groundW,groundH),(rect[0],rect[1],10,10)):
                        BestArray[0][Y][X] = 4 #Blue rects
            if not objects == None:
                for rect in objects[3]:
                    if rectangles_intersect((groundX,groundY,groundW,groundH),(rect[0],rect[1],10,10)):
                        BestArray[0][Y][X] = 5 #Blue rects   
    #print(rect[:4])
    
    print(BestArray)
    return BestArray[0]
            
            
       
