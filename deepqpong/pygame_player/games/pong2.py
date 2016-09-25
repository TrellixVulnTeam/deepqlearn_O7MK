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
        self.reward = 1
        self.tick = 0
        self.reward_loss = 0

    def update(self):
        self._update_tick()
        self._update_reward()
        self.reward_loss = self.reward/2

    def _update_tick(self):
        self.tick += 1
    def _update_reward(self):
        self.reward = max(1, self.tick + self.reward)

    def reset(self):
        self.reward = 1
        self.tick = 0


class AxisComponents(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

    def reset(self, x=0, y=0):
        self.x = x
        self.y = y

class Speed(AxisComponents):
    def __init__(self, x=0, y=0):
        super(Speed, self).__init__(x=x, y=y)
    def reverse_x(self):
        self.x = self.x * (-1.)
    def reverse_y(self):
        self.y = self.y * (-1.)
    def random_direction(self):
        self.y *= random.choice([1, -1])
        self.x *= random.choice([1, -1])


class Bar(AxisComponents):
    def __init__(self, x, y, xl=10, yl=5):
        super(Bar, self).__init__(x=x, y=y)
        self.xl = xl
        self.yl = yl
        self.ylmid = self.yl/2.
        self.bar = None

class Player(Bar, PlayerStats):
    def __init__(self, x, y, xl, yl):
        super(Player, self).__init__(x=x, y=y, xl=xl, yl=yl)
        self.score = 0
        self.start_time = 0

class Circle(AxisComponents):
    def __init__(self, x, y, diameter=0):
        super(Circle, self).__init__(x=x, y=y)
        self.diameter = diameter
        self.speed = Speed(0, 0)

class GameSurface(object):
    def __init__(self):
        self.min = AxisComponents()
        self.max = AxisComponents()

# SURFACE = GameSurface()
# SURFACE.min.x

SURFACE_X = 640
SURFACE_Y = 480
BAR_X = 10
BAR_Y = 50
HALFBARLEN = 25
BORDER_WIDTH_X = 10
BORDER_WIDTH_Y = 10


class GameSurface(object):
    SURFACE_X = SURFACE_X
    SURFACE_Y = SURFACE_Y
    X_MIN = BORDER_WIDTH_X
    Y_MIN = BORDER_WIDTH_Y
    X_MAX = SURFACE_X - BORDER_WIDTH_X
    Y_MAX = SURFACE_Y - BORDER_WIDTH_Y
    DIM = (SURFACE_X, SURFACE_Y)
    BAR_DIM = (10,50)


SURFACE = GameSurface()

surface = AxisComponents(SURFACE_X,SURFACE_Y)

pygame.init()

screen = pygame.display.set_mode(SURFACE.DIM, 0, 32)

#Creating 2 bars, a ball and background.
back = pygame.Surface(SURFACE.DIM)
background = back.convert()
background.fill((0,0,0))
bar = pygame.Surface(SURFACE.BAR_DIM)
bar1 = bar.convert()
bar1.fill((255,255,255))
bar2 = bar.convert()
bar2.fill((255,255,255))
circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(255,255,255),(int(15/2),int(15/2)),int(15/2))
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))




# some definitions
# bar1_x, bar2_x = 10. , 620.
# bar1_y, bar2_y = 215. , 215.
# circle_x, circle_y = 307.5, 232.5
bar1_move, bar2_move = 0. , 0.
# speed_x, speed_y, speed_circ = 250., 250., 250.
# bar1_score, bar2_score = 0,0



HISTORY = 50


player1 = Player(10., 215., xl=10, yl=50)
player2 = Player(620., 215., xl=10, yl=50)
ball = Circle(307.5, 232.5)
scorer = Reward()

player1.bar = bar1
player2.bar = bar2
ball.circle = circle
ball.speed = Speed(250., 250.)

speed_circ = 250.

# bar1_move, bar2_move = 0. , 0.
# speed_x, speed_y, speed_circ = 250., 250., 250.



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

    # score1 = font.render(str(bar1_score), True,(255,255,255))
    # score2 = font.render(str(bar2_score), True,(255,255,255))
    score1 = font.render(str(player1.score), True,(255,255,255))
    score2 = font.render(str(player2.score), True,(255,255,255))

    screen.blit(background,(0,0))
    frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(630,470)),2)
    middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
    screen.blit(bar1,(player1.x, player1.y))
    screen.blit(bar2,(player2.x,player2.y))
    screen.blit(ball.circle,(ball.x, ball.y))
    screen.blit(score1, (150.,210.))
    screen.blit(score2, (380.,210.))

    current_reward = font.render(str(scorer.reward), True,(255,255,255))
    screen.blit(current_reward, (200.,310.))


    player1.move(x=0, y=bar1_move)

    # movement of circle
    time_passed = clock.tick(30)
    time_sec = time_passed / 1000.0

    ai_speed = speed_circ * time_sec
    ball.move(ball.speed.x * time_sec, ball.speed.y * time_sec)

    # scorer.update()

    #AI of the computer.
    # if circle_x >= 305.:
    #     if not bar2_y == circle_y + 7.5:
    #         if bar2_y < circle_y + 7.5:
    #             bar2_y += ai_speed
    #         if  bar2_y > circle_y - 42.5:
    #             bar2_y -= ai_speed
    #     else:
    #         bar2_y == circle_y + 7.5

    if ball.x >= SURFACE_X/2:
        #if not player2.y == ball.y + HALFBARLEN:
        if player2.y < ball.y + HALFBARLEN:
            player2.move(0, y=ai_speed)
        if  player2.y > ball.y - HALFBARLEN:
            player2.move(0, y=-ai_speed)
        # else:
            # bar2_y == circle_y + 7.5
            # player2.y == ball.y + 7.5#+ HALFBARLEN
            # player2.move(0, y=ai_speed)

    # define bounds
    # if bar1_y >= 420.: bar1_y = 420.
    # elif bar1_y <= 10. : bar1_y = 10.
    # if bar2_y >= 420.: bar2_y = 420.
    # elif bar2_y <= 10.: bar2_y = 10.

    # upper bound
    if player1.y >= 420:#SURFACE_Y - HALFBARLEN - BORDER_WIDTH_Y:
        player1.y = 420#SURFACE_Y - HALFBARLEN - BORDER_WIDTH_Y
    # lower bound
    elif player1.y <= 10.:#SURFACE_Y - HALFBARLEN - BORDER_WIDTH_Y:
        player1.y = 10.
    if player2.y >= 420.: player2.y = 420.
    elif player2.y <= 10.: player2.y = 10.



    #since i don't know anything about collision, ball hitting bars goes like this.
    # bar1 collision
    # if circle_x <= bar1_x + 10.:
    #     if circle_y >= bar1_y - 7.5 and circle_y <= bar1_y + 42.5:
    #         # circle hits bar, flip x direction
    #         circle_x = 20.
    #         speed_x = -speed_x
    if ball.x <= player1.x + 10.:
        if ball.y >= player1.y - 7.5 and ball.y <= player1.y + 42.5:
            # circle hits bar, flip x direction
            ball.x = 20.
            ball.speed.reverse_x()
            # modified score
            scorer.update()
            player1.score += scorer.reward



    # bar2 collision
    # if circle_x >= bar2_x - 15.:
    #     if circle_y >= bar2_y - 7.5 and circle_y <= bar2_y + 42.5:
    #         # circle hits bar, flip x direction
    #         circle_x = 605.
    #         speed_x = -speed_x
    if ball.x >= player2.x - 15.:
        if ball.y >= player2.y - 7.5 and ball.y <= player2.y + 42.5:
            # circle hits bar, flip x direction
            ball.x = 605.
            ball.speed.reverse_x()
            # modified score
            scorer.update()
            player2.score += scorer.reward


    # border collision - bar1_x
    # if circle_x < 5.:
    #     bar2_score += 1
    #     circle_x, circle_y = 320., random.randrange(5, 475, 1) #232.5
        # bar1_y, bar_2_y = 215., 215.
    if ball.x < 5.:
        # player2.score += 1
        ball.reset(320., random.randrange(5, 475, 1)) #232.5
        # modified score
        player1.score -= scorer.reward_loss
        scorer.reset()
        ball.speed.random_direction()
        



    # elif circle_x > 620.:
    #     bar1_score += 1
    #     circle_x, circle_y = 307.5,  random.randrange(5, 475, 1) #232.5
    #     # bar1_y, bar2_y = 215., 215.
    elif ball.x > 620.:
        # player1.score += 1
        player2.score -= scorer.reward_loss
        ball.reset(307.5, random.randrange(5, 475, 1))
        ball.speed.random_direction()
        scorer.reset()


    # if circle_y <= 10.:
    #     speed_y = -speed_y
    #     circle_y = 10.
    if ball.y <= 10.:
        ball.speed.reverse_y()
        ball.y = 10.

    # elif circle_y >= 457.5:
    #     speed_y = -speed_y
    #     circle_y = 457.5
    elif ball.y >= 457.5:
        ball.speed.reverse_y()
        ball.y = 457.5


    pygame.display.update()

pygame.quit()
