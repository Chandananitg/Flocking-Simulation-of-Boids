import time
from turtle import Screen
from boid import Boid

screen = Screen()
screen.tracer(0)
screen.title("Boids")
screen.setup(width=1.0, height=1.0, startx=0, starty=0)
screen.colormode(255)
colour = (225, 224, 255)
screen.bgcolor(colour)
on = True
boids = []
for _ in range(50):
    boid = Boid()
    boids.append(boid)
screen.update()

screen.listen()


def stop():
    global on
    on = False


screen.onkey(stop, "space")

while on:
    for boid in boids:
        boid.flock(boids)
        boid.update()
    time.sleep(0.01)
    screen.update()

screen.exitonclick()
