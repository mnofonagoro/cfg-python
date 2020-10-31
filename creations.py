import turtle

def triangle(side_length, colour):
    angle = 120
    turtle.color(colour, colour)
    turtle.begin_fill()

    for eren in range(3):
        turtle.forward(side_length)
        turtle.right(angle)
    turtle.end_fill()
    turtle.done()
triangle(100, "pink")

triangle(1000, "yellow")
