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

#init backwork
pygame.init()

class Simulation:
    #AI stuff
    #body_transform, pendulum_top_transform, body_velocity, pendulum_top_velocity
    def get_screen_center(self):
        return self.screenCenter

    def get_screen_width(self):
        return self.screenWidth

    def body_transform(self):
        return self.play_body.local_to_world((0, 0))

    def pendulum_top_transform(self):
        return self.pendulum_body.local_to_world((0, 0))

    def body_velocity(self):
        return self.play_body.velocity_at_local_point((0, 0))

    def pendulum_top_velocity(self):
        return self.pendulum_body.velocity_at_local_point((0, 0))

    #the game itself
    def __init__(self):
        self.screenWidth = round(pygame.display.get_desktop_sizes()[0][0] / 1.5)
        self.screenHeight = round(pygame.display.get_desktop_sizes()[0][1] / 1.5)
        self.screenCenter = Vec2d(round(self.screenWidth / 2), round(self.screenHeight / 2))

        # init display
        self.screen = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight)
        )
        self.reset()

        #print(pygame.display.get_window_size())
        self.clock = pygame.time.Clock()
        self.running = True

    def reset(self):
        #Physics & Backworks
        self.space = pymunk.Space()
        self.space.gravity = 0.0, 98.1

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.frame_iteration = 0
        self.score = 0

        #pendulum
        self.pendulum_body = pymunk.Body(10, 10)
        self.pendulum_body.mass = 1

        self.pendulum_body.position = self.screenCenter + (0, -75)
        self.pendulum_shape = pymunk.Circle(self.pendulum_body, 5, (0, 0))
        self.pendulum_shape.friction = 1.0

        self.play_body = pymunk.Body(10, float("inf"))
        self.play_body.position = self.screenCenter
        self.move_joint = pymunk.GrooveJoint(
            self.space.static_body, self.play_body, (0, self.screenHeight / 2), (self.screenWidth, self.screenHeight / 2), (0, 0)
        )

        self.rotation_center_joint = pymunk.PinJoint(self.pendulum_body, self.play_body, (0, 0), (0, 0))
        self.rotation_center_joint.distance = 75

        self.space.add(self.pendulum_body, self.pendulum_shape, self.rotation_center_joint, self.play_body, self.move_joint)

    def play_step(self, action):
        self.frame_iteration += 1

        #running
        if self.running:
            #check for quiters
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.image.save(screen, "AI_balance.png")
            
            #agent action
            self.play_body.velocity -= (action[0] - action[1], 0) * 200

            #Clear screen
            self.screen.fill(pygame.Color("white"))

            #check if lose or score
            reward = 0
            game_over = False

            #self.body_transform()[1] < self.pendulum_top_transform()[1] or 
            if self.frame_iteration > 1000:
                game_over = True
                reward = -10
                return reward, game_over, self.score

            if self.body_transform()[1] > self.pendulum_top_transform()[1]:
                self.score += 1
                reward = 10

            #Draw physics
            self.space.debug_draw(self.draw_options)
            dt = 1.0 / 60.0
            for x in range(1):
                self.space.step(dt)

            #Flip screen
            pygame.display.flip()
            self.clock.tick(50)
            pygame.display.set_caption("PyMunk Test | fps: " + str(round(self.clock.get_fps())))

            #return score to agent
            return reward, game_over, self.score
