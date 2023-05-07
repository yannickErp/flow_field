import math
import os
import sys
import time

from config import *
import pygame
import view
from flow_field import FlowField
from particle import Particle


def run():
    screen = view.View(SEED, WIDTH, HEIGHT, CAPTION, FPS)
    timestep = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if DRAW_BACKGROUND:
            screen.draw_image_background()
        if DRAW_FPS:
            screen.draw_fps_string()
        if DRAW_ANGLES:
            screen.draw_angles()
        if DRAW_FLOW:
            screen.draw_flow_field()
        if DRAW_PARTICLES:

            screen.draw_particles(DRAW_DOTS, DRAW_LINES, FIELD_SCALE)
        pygame.display.flip()
        #time.sleep(0.3)
        if timestep == 10000:
            sys.exit()
        if timestep % 100 == 0 and CAPTURE_SCREENSHOTS:
            screen.capture(int(timestep / 100))
        if timestep % 10 == 0 and PRINT_TIMESTEPS:
            print(timestep)
        timestep += 1


if __name__ == '__main__':
    if not os.path.exists("Screenshots"):
        os.makedirs("Screenshots")
    run()
