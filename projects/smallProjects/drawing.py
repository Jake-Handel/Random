""" Turtle drawing animation of a love heart """
import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Love Heart")
screen.bgcolor("black")

# Create a turtle
pen = turtle.Turtle()
pen.color("red")
pen.speed(1)

# Draw the heart
pen.begin_fill()
pen.left(45)
pen.forward(100)
pen.circle(50, 180)
pen.right(90)
pen.circle(50, 180)
pen.forward(100)
pen.end_fill()

# Hide the turtle
pen.hideturtle()

# Keep the window open
screen.mainloop()
