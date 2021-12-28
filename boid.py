import random
from turtle import Turtle
from vector import Vector, angle_between, length, dist, scalar_div, normalize, scalar_mul, setMag

# # Only Alignment
# ALIGN_MULTIPLIER = 1
# COHESION_MULTIPLIER = 0
# SEPARATION_MULTIPLIER = 0

# # Only Cohesion
# ALIGN_MULTIPLIER = 0
# COHESION_MULTIPLIER = 1
# SEPARATION_MULTIPLIER = 0

# # Only Separation
# ALIGN_MULTIPLIER = 0
# COHESION_MULTIPLIER = 0
# SEPARATION_MULTIPLIER = 1

# Flocking
ALIGN_MULTIPLIER = 1.3
COHESION_MULTIPLIER = 0.175
SEPARATION_MULTIPLIER = 0.175

PERCEPTION_RADIUS = 180
COLOUR_LIST = [(187, 96, 255), (153, 51, 255), (128, 0, 255), (153, 82, 224), (140, 26, 255), (166, 77, 255),
               (153, 56, 250), (140, 31, 249)]
xaxis = Vector(1, 0)


class Boid(Turtle, Vector):
    def __init__(self):
        super().__init__()
        boid_color = random.choice(COLOUR_LIST)
        self.color(boid_color)
        self.penup()
        self.shapesize(2)
        x_cor = random.randint(-650, 650)
        y_cor = random.randint(-300, 300)
        x_vel = random.randint(-5, 5)
        y_vel = random.randint(-5, 5)

        self.position = Vector(x_cor, y_cor)
        self.velocity = Vector(x_vel, y_vel)
        if length(self.velocity) == 0:
            self.velocity = Vector(1, 1)
        self.acceleration = Vector(0, 0)
        self.angle_bw_xaxis_and_velocity = angle_between(xaxis, self.velocity)
        self.max_speed = 5
        self.max_force = 2

    def angle(self):
        if length(self.velocity) != 0:
            return angle_between(xaxis, self.velocity)
        else:
            return 0

    def update(self):
        self.edge_shift()
        self.velocity = self.velocity + self.acceleration
        self.velocity = setMag(self.velocity, self.max_speed)
        self.position = self.position + self.velocity
        self.goto(self.position.x, self.position.y)
        self.move_align()
        self.acceleration = scalar_mul(self.acceleration, 0)

    def edge_shift(self):
        if self.position.x >= 750:
            self.position.x = -750
        elif self.position.x <= -750:
            self.position.x = 750
        if self.position.y >= 400:
            self.position.y = -400
        elif self.position.y <= -400:
            self.position.y = 400

    def move_align(self):
        if self.heading() != self.angle:
            self.left(self.angle() - self.heading())

    def align(self, boids):
        perception_radius = PERCEPTION_RADIUS
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            d = dist(self.position, boid.position)
            if d <= perception_radius and boid is not self:
                steering += normalize(boid.velocity)
                total += 1
        if total > 1:
            steering = scalar_div(steering, total)
            steering = steering - self.velocity
            if length(steering) > self.max_force:
                steering = setMag(steering, self.max_force)
        return steering

    def cohesion(self, boids):
        perception_radius = PERCEPTION_RADIUS
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            d = dist(self.position, boid.position)
            if d <= perception_radius and boid is not self:
                steering += boid.position
                total += 1
        if total > 1:
            steering = scalar_div(steering, total)
            steering = steering - self.position
            steering = setMag(steering, self.max_speed)
            steering = steering - self.velocity
            if length(steering) > self.max_force:
                steering = setMag(steering, self.max_force)
        return steering

    def separation(self, boids):
        perception_radius = PERCEPTION_RADIUS
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            d = dist(self.position, boid.position)
            if perception_radius >= d >= -perception_radius and boid is not self:
                diff = self.position - boid.position
                diff = scalar_div(diff, d)
                steering += diff
                total += 1
        if total > 0:
            steering = scalar_div(steering, total)
            steering = setMag(steering, self.max_speed)
            steering = steering - self.velocity
            if length(steering) > self.max_force:
                steering = setMag(steering, self.max_force)
        return steering

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        alignment = scalar_mul(alignment, ALIGN_MULTIPLIER)
        cohesion = scalar_mul(cohesion, COHESION_MULTIPLIER)
        separation = scalar_mul(separation, SEPARATION_MULTIPLIER)
        # self.acceleration = alignment
        # self.acceleration = cohesion
        # self.acceleration = separation
        # self.acceleration = alignment + cohesion
        # self.acceleration = alignment + separation
        # self.acceleration = cohesion + separation
        self.acceleration = alignment + cohesion + separation


