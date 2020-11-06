# Test for character movement using various classes.

import turtle
import math

SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

wn = turtle.Screen()
wn.setup(SCREEN_WIDTH + 220, SCREEN_HEIGTH + 30)
wn.title("Character Movement Test")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

# Pause function.
is_paused = False
def pause_game():
    global is_paused
    if is_paused == True:
        is_paused = False
    else:
        is_paused = True

# Game class.
class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.level = 1

    def start_level(self):
        sprites.clear()
        
        sprites.append(player)

    def render_border(self, pen, x_offset, y_offset):
        pen.color("white")
        pen.width(3)
        pen.penup()

        left = self.width/-2.0 - x_offset
        right = self.width/2.0 - x_offset
        top = self.height/2.0 - y_offset
        bottom = -self.height/2.0 - y_offset

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()


# Sprite class.
class Sprite():
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0
        self.heading = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.2
        self.width = 20
        self.height = 20
        self.state = "active"
        self.max_dx = 5
        self.max_dy = 5

    def is_collision(self, other):
        if self.x < other.x + other.width and\
            self.x + self.width > other.x and\
            self.y < other.y + other.height and\
            self.y + self.height > other.y:
            return True
        else:
            return False

    def bounce(self, other):
        temp_dx = self.dx
        temp_dy = self.dy

        self.dx = other.dx
        self.dx = other.dx

        other.dx = temp_dx
        other.dx = temp_dy

    def update(self): 
        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust

        self.x += self.dx
        self.y += self.dy

        self.border_check()

    def border_check(self):
        if self.x > game.width/2.0 - 10:
            self.x = game.width/2.0 - 10
            self.dx *= -1

        elif self.x < -game.width/2.0 + 10:
            self.x = -game.width/2.0 + 10
            self.dx *= -1

        if self.y > game.height/2.0 - 10:
            self.y = game.height/2.0 - 10
            self.dy *= -1

        elif self.y < -game.height/2.0 + 10:
            self.y = -game.height/2.0 + 10
            self.dy *= -1

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

        pen.penup()

# Player class.
class Player(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, 0, 0, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da = 0

    def rotate_left(self):
        self.da = 5

    def rotate_right(self):
        self.da = -5

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        self.thrust += self.acceleration

    def decelerate(self):
        self.thrust = 0.0

    def update(self):
        if self.state == "active": 
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def reset(self):
        self.x = 0
        self.y = 0
        self.heading = 90
        self.dx = 0
        self.dy = 0
        self.lives -= 1

    def render(self, pen, x_offset, y_offset):
        pen.shapesize(0.5, 1.0, None)
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

        pen.shapesize(1.0, 1.0, None)

class Camera():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y

# Creates the player sprite.
game = Game(700, 500)
player = Player(0, 0, "triangle", "white")
camera = Camera(player.x, player.y)

# Sprites list.
sprites = []

# Sets up the level.
game.start_level()


# Keyboard bindings.
wn.listen()
wn.onkeypress(player.rotate_left, "Left")
wn.onkeypress(player.rotate_right, "Right")

wn.onkeyrelease(player.stop_rotation, "Left")
wn.onkeyrelease(player.stop_rotation, "Right")

wn.onkeypress(player.accelerate, "Up")
wn.onkeyrelease(player.decelerate, "Up")

wn.onkeypress(pause_game, "p")


# Main run loop.
while True:

    if not is_paused:
        pen.clear()

        # Updates all the sprites (There's only one here).
        for sprite in sprites:
            sprite.update()

        # Renders all the sprites (There's only one in this case).
        for sprite in sprites:
            sprite.render(pen, camera.x, camera.y)

        game.render_border(pen, camera.x, camera.y)

        # Updates the camera.
        camera.update(player.x, player.y)

            
        wn.update()
    else:
        wn.update()

# Help from tutorials and other places was used to make this.
