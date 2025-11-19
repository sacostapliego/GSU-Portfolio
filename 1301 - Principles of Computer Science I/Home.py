#The view of a regular rural area home on a hot summer day. 
#File: HomeScape.py
#Student: Steven Acosta-Pliego
#Course Name: CSC1301
#Data: 4/10/2023
#Description of program: Created a program to create a house with many flowers

import turtle
import math

#Function to draw windows, parameters are where to put the windows
def draw_window(x,y):
    turtle.up()
    turtle.setpos(x,y)
    turtle.down()
    #Window Box
    count = 0
    turtle.fillcolor("azure3")
    turtle.begin_fill()
    while count < 4:
        turtle.right(90)
        turtle.forward(60)
        count = count + 1
    turtle.end_fill()
    #Window Panels Horizontal
    turtle.up()
    turtle.backward(30)
    turtle.right(90)
    turtle.down()
    turtle.forward(60)
    turtle.up()
    #Window Panels Vertical
    turtle.backward(30)
    turtle.right(90)
    turtle.backward(30)
    turtle.down()
    turtle.forward(60)
    turtle.up()
    #Set positon at 0,0 and facing right
    turtle.right(180)
    turtle.setpos(0,0)
    return

#Function to draw rectangles for the landscape and base of the house
def draw_rectangle(height,length):
    turtle.down()
    count = 0
    while count < 2:
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)
        turtle.forward(length)
        count += 1
    return

#Function to draw flowers
def draw_flower(x,y,deg,color):
    turtle.setpos(x,y)
    turtle.fillcolor(color) 
    turtle.begin_fill() 
    turtle.down()
    turtle.right(deg)
    for i in range(4):
        turtle.circle(10,270)
        turtle.left(180)
    turtle.end_fill()
    #Draw dor in middle of flower
    turtle.up()
    turtle.backward(10)
    turtle.down()
    turtle.fillcolor("yellow") 
    turtle.begin_fill() 
    turtle.circle(2)
    turtle.end_fill()
    #Draw stem for flower
    turtle.up()
    turtle.forward(10)
    turtle.down()
    turtle.forward(20)
    turtle.right(360 - deg)
    return

#Function to draw clouds
def draw_clouds(x,y):
    turtle.setpos(x,y)
    turtle.down()
    turtle.fillcolor("whitesmoke")
    turtle.begin_fill()
    for i in range(4):
        turtle.circle(30,225)
        turtle.left(180)
    turtle.right(180)
    turtle.forward(150)
    turtle.end_fill()
    turtle.up()
    return

#Triangles to add texture to grass
def draw_triangles(x,y):
    turtle.setpos(x,y)
    turtle.down()
    for i in range(4):
        turtle.left(60)
        turtle.forward(15)
        turtle.right(120)
        turtle.forward(15)
        turtle.left(60)
    turtle.up()

    return

#Sets the position to (0,0) and arrow pointing to the right
def set_positon(degrees):
    turtle.up()
    turtle.setpos(0,0)
    turtle.right(degrees)
    return

#Speed to draw
turtle.speed(10)
set_positon(0)

#Landscape
turtle.up()
turtle.fillcolor("DarkOliveGreen3")
turtle.begin_fill()
turtle.setpos(400,-180)
draw_rectangle(200,800)
turtle.end_fill()

#Sky
turtle.up()
turtle.fillcolor("CadetBlue1")
turtle.begin_fill()
turtle.setpos(400,500)
draw_rectangle(680,800)
turtle.end_fill()

#Sun
turtle.up()
turtle.setpos(220,170)
turtle.fillcolor("Yellow")
turtle.begin_fill()
turtle.circle(90)
turtle.end_fill()

#Base of House
turtle.up()
turtle.setpos(200,0)
turtle.fillcolor("burlywood")
turtle.begin_fill()
draw_rectangle(200,400)
turtle.end_fill()

#Roof of House
turtle.forward(25)
turtle.left(150)
turtle.fillcolor("burlywood4")
turtle.begin_fill()
turtle.forward(450/math.sqrt(3))
turtle.left(60)
turtle.forward(450/math.sqrt(3))
turtle.left(150)
turtle.end_fill()
set_positon(0)

#Draw 5 windows for house
draw_window(175,-30)
draw_window(-115,-30)
draw_window(175,-120)
draw_window(-115,-120)
draw_window(25,-30)

#Door for house
turtle.setpos(-35,-200)
turtle.right(180)
turtle.fillcolor("burlywood3")
turtle.begin_fill()
draw_rectangle(70,60)
turtle.end_fill()
set_positon(180)

#Doorknob
turtle.setpos(15,-170)
turtle.down()
turtle.fillcolor("Yellow")
turtle.begin_fill()
turtle.circle(2)
turtle.end_fill()
set_positon(0)

#Grass
draw_triangles(-200,-300)
draw_triangles(-150,-350)
draw_triangles(-50,-260)
draw_triangles(-300,-250)
draw_triangles(-325,-350)
draw_triangles(-350,-310)
draw_triangles(200,-300)
draw_triangles(150,-350)
draw_triangles(50,-290)
draw_triangles(300,-250)
draw_triangles(275,-350)
draw_triangles(300,-310)
draw_triangles(0,-330)

#Flowers
draw_flower(-150,-300,80,"cyan")
set_positon(0)
draw_flower(-250,-250,90,"yellow")
set_positon(0)
draw_flower(200,-270,90,"green3")
set_positon(0)
draw_flower(100,-240,100,"gold1")
set_positon(0)
draw_flower(-300,-300,80,"green3")
set_positon(0)
draw_flower(-50,-250,90,"yellow")
set_positon(0)
draw_flower(100,-300,90,"red")
set_positon(0)
draw_flower(300,-230,100,"cyan")
set_positon(0)

#Clouds
draw_clouds(300,160)
draw_clouds(30,160)
draw_clouds(-180,250)
set_positon(0)

turtle.mainloop()
