#Modified from http://www.pygame.org/project-Very+simple+Pong+game-816-.html
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
import numpy
import pygame
from pygame.locals import *
from sys import exit
import random
import pygame.surfarray as surfarray
import time
from collections import deque

pygame.init()

screen = pygame.display.set_mode((640,480),0,32)

#Creating 2 bars, a ball and background.
back = pygame.Surface((640,480))
background = back.convert()
background.fill((0,0,0))
bar = pygame.Surface((10,50))
bar1 = bar.convert()
bar1.fill((255,255,255))
bar2 = bar.convert()
bar2.fill((255,255,255))
circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(255,255,255),(int(15/2),int(15/2)),int(15/2))
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))




# some definitions
bar1_x, bar2_x = 10. , 620.
bar1_y, bar2_y = 215. , 215.
circle_x, circle_y = 307.5, 232.5
bar1_move, bar2_move = 0. , 0.
speed_x, speed_y, speed_circ = 250., 250., 250.
bar1_score, bar2_score = 0,0


last_n_losses_1 = 0
last_n_losses_2 = 0

HISTORY = 50

class PlayerStats(object):
    def __init__(self):
        self.start_time = 0
        self.losses = deque(HISTORY)
        self.wins = deque(HISTORY)

    def avg_survival(self):
        return mean(self.losses)

    def reset(self):
        self.losses = 0
        self.wins = 0

    def win(self, time_delta):
        self.wins.append(time_delta)

    def loss(self, time_delta):
        self.losses.append(time_delta)

class Reward(object):
    def __init__(self):
        self.reward = 0

    def update(self, increment):
        self.reward += increment

    def reset(self):
        self.reward = 0


class AxisComponents(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

class Speed(AxisComponents):
    def __init__(self, x, y):
        super(Speed, self).__init__(x=x, y=y)

class Bar(AxisComponents):
    def __init__(self, x, y, bar_len=10, thickness=5):
        super(Bar, self).__init__(x=x, y=y)
        self.bar_len = bar_len
        self.halfwidth = self.bar_len/2.
        self.thickness = thickness


class Player(Bar, PlayerStats):
    def __init__(self, x, y, bar_len):
        super(Player, self).__init__(x=x, y=y, bar_len=bar_len)
        self.score = 0
        self.start_time = 0


class Circle(AxisComponents):
    def __init__(self, x, y, diameter=0):
        super(Circle, self).__init__(x=x, y=y)
        self.diameter = diameter




def main():

    bar1 = Player(10., 215.)
    bar2 = Player(620., 215.)
    circle = Circle(307.5, 232.5)

    # # some definitions
    # bar1_x, bar2_x = 10. , 620.
    # bar1_y, bar2_y = 215. , 215.
    # circle_x, circle_y = 307.5, 232.5
    bar1_move, bar2_move = 0. , 0.
    speed_x, speed_y, speed_circ = 250., 250., 250.
    bar1_score, bar2_score = 0,0




#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",40)

start_time = time.time()

done = False
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == KEYDOWN:
            if event.key == K_UP:
                bar1_move = -ai_speed
            elif event.key == K_DOWN:
                bar1_move = ai_speed
        elif event.type == KEYUP:
            if event.key == K_UP:
                bar1_move = 0.
            elif event.key == K_DOWN:
                bar1_move = 0.

    score1 = font.render(str(bar1_score), True,(255,255,255))
    score2 = font.render(str(bar2_score), True,(255,255,255))

    screen.blit(background,(0,0))
    frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(630,470)),2)
    middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
    screen.blit(bar1,(bar1_x,bar1_y))
    screen.blit(bar2,(bar2_x,bar2_y))
    screen.blit(circle,(circle_x,circle_y))
    screen.blit(score1,(250.,210.))
    screen.blit(score2,(380.,210.))

    # screen.blit(last_n_losses_1,(250.,180.))
    # screen.blit(last_n_losses_2,(380.,180.))


    bar1_y += bar1_move

    # movement of circle
    time_passed = clock.tick(30)
    time_sec = time_passed / 1000.0

    circle_x += speed_x * time_sec
    circle_y += speed_y * time_sec
    ai_speed = speed_circ * time_sec

    #AI of the computer.
    if circle_x >= 305.:
        if not bar2_y == circle_y + 7.5:
            if bar2_y < circle_y + 7.5:
                bar2_y += ai_speed
            if  bar2_y > circle_y - 42.5:
                bar2_y -= ai_speed
        else:
            bar2_y == circle_y + 7.5

    # define bounds
    if bar1_y >= 420.: bar1_y = 420.
    elif bar1_y <= 10. : bar1_y = 10.
    if bar2_y >= 420.: bar2_y = 420.
    elif bar2_y <= 10.: bar2_y = 10.

    #since i don't know anything about collision, ball hitting bars goes like this.
    # bar1 collision
    if circle_x <= bar1_x + 10.:
        if circle_y >= bar1_y - 7.5 and circle_y <= bar1_y + 42.5:
            # circle hits bar, flip x direction
            circle_x = 20.
            speed_x = -speed_x
    # bar2 collision
    if circle_x >= bar2_x - 15.:
        if circle_y >= bar2_y - 7.5 and circle_y <= bar2_y + 42.5:
            # circle hits bar, flip x direction
            circle_x = 605.
            speed_x = -speed_x

    # border collision - bar1_x
    if circle_x < 5.:
        bar2_score += 1
        circle_x, circle_y = 320., random.randrange(5, 475, 1) #232.5
        # bar1_y, bar_2_y = 215., 215.
    elif circle_x > 620.:
        bar1_score += 1
        circle_x, circle_y = 307.5,  random.randrange(5, 475, 1) #232.5
        # bar1_y, bar2_y = 215., 215.
    if circle_y <= 10.:
        speed_y = -speed_y
        circle_y = 10.
    elif circle_y >= 457.5:
        speed_y = -speed_y
        circle_y = 457.5


    pygame.display.update()

pygame.quit()


def reset_circle_y(y_min, y_max):
    x = random.randrange(5, 5, 1)
