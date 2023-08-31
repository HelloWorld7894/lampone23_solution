import turtle
import time
import urllib.request



def animate_path(path): 
    image_url = "http://192.168.100.22/image/image.png"
    local_filename, headers = urllib.request.urlretrieve(image_url, "assets/image_last.png")
    t = turtle.Turtle()
    wn = turtle.Screen()
    wn.setup(width=700,height=550)
    wn.bgpic("assets/image_last.png")
    t.penup()
    t.forward(-10)
    t.left(90)
    t.forward(70)
    t.right(90)
    for i in path:
        time.sleep(1)
        if i == "F":
            if t.heading() % 360 == 180:
                t.forward(75)
            if t.heading() % 360 == 90:
                t.forward(60)
            if t.heading() % 360 == 0:
                t.forward(75)
            if t.heading() % 360 == 270:
                t.forward(60)
        if i == "B":
            t.forward(-60)
        if i == "L":
            t.left(90)
        if i == "R":
            t.right(90)
    wn.mainloop()