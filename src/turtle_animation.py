import turtle
import time

def animate_path(img): 
    tr = turtle.Turtle()
    wn = turtle.Screen()
    wn.setup(width=500,height=500)
    wn.bgpic(img)
    wn.mainloop()