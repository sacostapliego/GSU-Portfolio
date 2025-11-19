#File: PanamanianFlag.py
#Student: Steven Acosta-Pliego
#Course Name: CSC1301
#Data: 4/10/2023
#Drawing of the Panamanian Flag using turtle.

def draw_rectangle(height,length,color):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.down()
    count = 0
    while count < 2:
        turtle.right(90)
        turtle.forward(height)   
        turtle.right(90)
        turtle.forward(length)
        count += 1
    turtle.end_fill()
    turtle.up()
    return

def draw_star(x,y,color):
    turtle.setpos(x,y)
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.down()
    for i in range(5):
        turtle.forward(20)
        turtle.left(144)
        turtle.forward(20)
        turtle.right(72)
    turtle.end_fill()
    turtle.up()
    return
import turtle

turtle.up()
turtle.setpos(200,150)
draw_rectangle(300,400,"white")
turtle.setpos(0,0)
draw_rectangle(150,200,"blue")
turtle.left(180)
draw_rectangle(150,200,"red")
draw_star(-110,80,'blue')
turtle.setpos(0,0)
draw_star(100,-80,'red')
turtle.mainloop()