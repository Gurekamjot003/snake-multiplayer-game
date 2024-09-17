import turtle
import random
import time
import pygame
import os
import sys

# Initialize pygame for sound effects
pygame.mixer.init()

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def restart_game():
    global score1, score2
    global segments1, segments2
    global head1, head2
    global food

    score1 = 0
    score2 = 0

    for segment in segments1:
        segment.goto(1000, 1000)
    for segment in segments2:
        segment.goto(1000, 1000)
    segments1.clear()
    segments2.clear()

    head1.goto(0, 0)
    head1.direction = "stop"
    head2.goto(0, 20)
    head2.direction = "stop"

    food.goto(100, 100)

    text.clear()
    text.write("Blue: {} Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))

# Game variables
delay = 0.1
score1 = 0
score2 = 0
target_score = 30

# Screen setup
scrn = turtle.Screen()
scrn.title("SNAKE GAME")
scrn.bgcolor("black")
scrn.setup(600, 600)
scrn.tracer(0)

# Border
border = turtle.Turtle()
border.penup()
border.speed(0)
border.pencolor("white")
border.pensize(5)
border.goto(-270, 270)
border.pendown()
for i in range(4):
    border.forward(540)
    border.right(90)
border.hideturtle()

# Text for score display
text = turtle.Turtle()
text.speed(0)
text.penup()
text.color("white")
text.goto(0, 270)
text.hideturtle()
text.write("Blue: {} \t Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))

textt = turtle.Turtle()
textt.speed(0)
textt.penup()
textt.color("white")
textt.goto(200, 270)
textt.hideturtle()
textt.write("Target:{}".format(target_score), align="center", font=("arial", 16, "normal"))

# Snake 1
head1 = turtle.Turtle()
head1.speed(0)
head1.penup()
head1.color("pink")
head1.shape("square")
head1.goto(0, 0)
head1.direction = "stop"
segments1 = []

# Snake 2
head2 = turtle.Turtle()
head2.speed(0)
head2.penup()
head2.color("light blue")
head2.shape("square")
head2.goto(0, 0)
head2.direction = "stop"
segments2 = []

# Food
food = turtle.Turtle()
food.speed(0)
food.penup()
food.color("yellow")
food.shape("circle")
food.goto(100, 100)

# Movement functions
def go_up1():
    if head1.direction != "down":
        head1.direction = "up"

def go_down1():
    if head1.direction != "up":
        head1.direction = "down"

def go_right1():
    if head1.direction != "left":
        head1.direction = "right"

def go_left1():
    if head1.direction != "right":
        head1.direction = "left"

def go_up2():
    if head2.direction != "down":
        head2.direction = "up"

def go_down2():
    if head2.direction != "up":
        head2.direction = "down"

def go_right2():
    if head2.direction != "left":
        head2.direction = "right"

def go_left2():
    if head2.direction != "right":
        head2.direction = "left"

def move(snake_head):
    if snake_head.direction == "up":
        snake_head.sety(snake_head.ycor() + 20)
    if snake_head.direction == "down":
        snake_head.sety(snake_head.ycor() - 20)
    if snake_head.direction == "right":
        snake_head.setx(snake_head.xcor() + 20)
    if snake_head.direction == "left":
        snake_head.setx(snake_head.xcor() - 20)

# Keyboard bindings
scrn.listen()
scrn.onkey(go_up1, "Up")
scrn.onkey(go_down1, "Down")
scrn.onkey(go_right1, "Right")
scrn.onkey(go_left1, "Left")
scrn.onkey(go_up2, "w")
scrn.onkey(go_down2, "s")
scrn.onkey(go_right2, "d")
scrn.onkey(go_left2, "a")

# Load sounds
eat_sound = pygame.mixer.Sound(resource_path("eating.mp3"))
win_sound = pygame.mixer.Sound(resource_path("game-win.mp3"))
alert_sound = pygame.mixer.Sound(resource_path("alert.mp3"))
alert_sound.set_volume(0.1)
killed_sound = pygame.mixer.Sound(resource_path("killed.mp3"))
killed_sound.set_volume(0.3)
pygame.mixer.music.load(resource_path("background.mp3"))
pygame.mixer.music.play(-1)

def update_background_color():
    global scrn
    try:
        current_bgcolor = scrn.bgcolor()
        if score1 < score2:
            if current_bgcolor != 'dark blue':
                alert_sound.play()
            scrn.bgcolor("dark blue")
        elif score2 < score1:
            if current_bgcolor != 'dark red':
                alert_sound.play()
            scrn.bgcolor("dark red")
        elif score1 == score2:
            scrn.bgcolor("black")
    except turtle.Terminator:
        # Screen may have been closed; ignore this error
        pass
    except Exception as e:
        # Print any other exception that may occur
        print(f"Error updating background color: {e}")

try:
    while True:
        scrn.update()
        update_background_color()

        for head in [head1, head2]:
            if head.xcor() > 270 or head.xcor() < -270 or head.ycor() < -270 or head.ycor() > 270:
                head.goto(0, 0)
                killed_sound.play()
                head.direction = "stop"
                segments = segments1 if head == head1 else segments2
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                if head == head1:
                    score1 = 0
                else:
                    score2 = 0
                update_background_color()
                text.clear()
                text.write("Blue: {} \t Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))

        if head1.distance(food) < 20:
            food.goto(random.randint(-260, 260), random.randint(-260, 260))
            ns = turtle.Turtle()
            ns.speed(0)
            ns.color("red")
            ns.shape("square")
            ns.penup()
            segments1.append(ns)
            score1 += 1
            text.clear()
            eat_sound.play()
            update_background_color()
            text.write("Blue: {} \t Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))
            if score1 >= target_score:
                text.clear()
                pygame.mixer.music.stop()
                win_sound.play()
                text.write("Red WINS!", align="center", font=("arial", 24, "normal"))
                time.sleep(2)
                restart_game()

        if head2.distance(food) < 20:
            food.goto(random.randint(-260, 260), random.randint(-260, 260))
            ns = turtle.Turtle()
            ns.speed(0)
            ns.color("blue")
            ns.shape("square")
            ns.penup()
            segments2.append(ns)
            score2 += 1
            text.clear()
            eat_sound.play()
            update_background_color()
            text.write("Blue: {} \t Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))
            if score2 >= target_score:
                text.clear()
                pygame.mixer.music.stop()
                win_sound.play()
                text.write("Blue WINS!", align="center", font=("arial", 24, "normal"))
                time.sleep(2)
                restart_game()

        for i in range(len(segments1) - 1, 0, -1):
            segments1[i].goto(segments1[i - 1].xcor(), segments1[i - 1].ycor())
        if len(segments1) > 0:
            segments1[0].goto(head1.xcor(), head1.ycor())

        for i in range(len(segments2) - 1, 0, -1):
            segments2[i].goto(segments2[i - 1].xcor(), segments2[i - 1].ycor())
        if len(segments2) > 0:
            segments2[0].goto(head2.xcor(), head2.ycor())

        move(head1)
        move(head2)

        # Check for collisions with itself
        for segment in segments1:
            if segment.distance(head1) < 20:
                head1.goto(0, 0)
                killed_sound.play()
                head1.direction = "stop"
                for seg in segments1:
                    seg.goto(1000, 1000)
                segments1.clear()
                score1 = 0
                update_background_color()
                text.clear()
                text.write("Blue: {} \t Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))

        for segment in segments2:
            if segment.distance(head2) < 20:
                head2.goto(0, 0)
                killed_sound.play()
                head2.direction = "stop"
                for seg in segments2:
                    seg.goto(1000, 1000)
                segments2.clear()
                score2 = 0
                update_background_color()
                text.clear()
                text.write("Blue: {} \t Red: {}".format(score2, score1), align="center", font=("arial", 24, "normal"))

        time.sleep(delay)

except turtle.Terminator:
    pygame.mixer.music.stop()
    pygame.quit()
    print("Game closed gracefully")

except Exception as e:
    print(f"Error updating background color: {e}")