"""This example showcase an arrow pointing or aiming towards the cursor.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys

import pygame

import math

import pymunk
import pymunk.constraints
import pymunk.pygame_util
from pymunk import Vec2d

def zero_gravity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, (0,0), damping, dt)

def solid(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, (0,0), 0, 0)

def pointsInCircum(r, n, center):
    return [(math.cos(2*math.pi/n*x)*r + center[0], math.sin(2*math.pi/n*x)*r + center[1]) for x in range(0,n)]

def main():
    pygame.init()
    screenWidth = round(pygame.display.get_desktop_sizes()[0][0] / 1.5)
    screenHeight = round(pygame.display.get_desktop_sizes()[0][1] / 1.5)
    screenCenter = Vec2d(round(screenWidth / 2), round(screenHeight / 2))
    screen = pygame.display.set_mode(
        (screenWidth, screenHeight)
    )

    #print(pygame.display.get_window_size())
    clock = pygame.time.Clock()
    running = True

    #Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, 9.81
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    #Variables
    stiffness = 10000.0
    damping = 1000.0 / 6
    pointMass = 1.0
    pointCount = 150

    objects = []

    #body
    ps = [(0, 0), (10, -75), (-10, -75)]
    moment = pymunk.moment_for_poly(1, ps)
    play_body = pymunk.Body(500, float("inf"))
    play_body.angle = 0 * math.pi
    play_body.mass = 10
    play_body.center_of_gravity = (30, -74)

    play_body.position = screenCenter
    play_Shape = pymunk.Poly(play_body, ps)
    play_Shape.friction = 1.0
    play_Shape.elasticity = 0

    move_joint = pymunk.GrooveJoint(
        space.static_body, play_body, (0, screenHeight / 2), (screenWidth, screenHeight / 2), (0, 0)
    )
    space.add(play_body, play_Shape, move_joint)

    #running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.image.save(screen, "AI_balance.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                play_body.velocity = (-50, 0)
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                play_body.velocity = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                play_body.velocity = (50, 0)
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                play_body.velocity = 0, 0

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        space.debug_draw(draw_options)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("PyMunk Test | fps: " + str(round(clock.get_fps())))


if __name__ == "__main__":
    main()
