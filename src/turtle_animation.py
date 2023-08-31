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
    for i in path
    wn.mainloop()
    


animate_path()