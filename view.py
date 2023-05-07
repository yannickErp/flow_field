import random
import pygame

import utils
from flow_field import FlowField
from particle import Particle
from physics_classes import Vector
from config import *


class View:
    def __init__(self, seed, width, height, caption, fps):
        self.seed = seed
        self.width = width
        self.height = height
        self.flow_field = FlowField(int(self.width / FIELD_SCALE), int(self.height / FIELD_SCALE), FLOW_VARIETY,
                                    FLOW_CHANGE, self.seed, FIELD_SCALE)
        self.particles = [Particle(Vector(random.randint(0, width - 1),
                                          random.randint(0, height - 1)),
                                   PARTICLE_INITIAL_VELOCITY,
                                   PARTICLE_MASS,
                                   PARTICLE_RADIUS,
                                   PARTICLE_MAX_SPEED,
                                   PARTICLE_COLOR) for _ in range(PARTICLE_NUMBER)]
        pygame.init()
        pygame.display.set_caption(caption)
        self.font = pygame.font.Font(None, 25)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.changing_color = (255, 0, 255, ALPHA)
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

    def draw_image_background(self):
        background = pygame.image.load("Screenshots/background_1.jpeg")
        background.convert()
        self.screen.blit(background, (0, 0))

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_fps_string(self):
        self.clock.tick(self.fps)
        fps = self.clock.get_fps()
        fps_string = self.font.render(
            str(int(fps)), True, pygame.Color('black'))
        self.screen.blit(fps_string, (1, 1))

    def draw_line_from_position_to_position(self, position1, position2, color, size):
        pygame.draw.line(self.screen, color, (position1[0], position1[1]), (position2[0], position2[1]), size)

    def draw_particles(self, draw_dots: bool, draw_lines: bool, field_scale: int):
        if self.flow_field.flow_change != 0:
            self.flow_field.update_flow_field()
        particle_surface = self.screen.convert_alpha()
        particle_surface.fill([0, 0, 0, 0])
        for particle in self.particles:
            particle.check_edges(self.width, self.height)
            particle.update(self.flow_field, field_scale, self.width, self.height)
            if draw_dots:
                pygame.draw.circle(particle_surface, particle.color, (particle.pos.x, particle.pos.y), particle.radius)
            if draw_lines:
                pygame.draw.line(particle_surface, self.changing_color, (particle.pos.x, particle.pos.y),
                                 (particle.old_pos.x, particle.old_pos.y), particle.radius)
        self.screen.blit(particle_surface, (0, 0))
        self.change_color(COLOR_CHANGE_RATE)

    def draw_flow_field(self):
        for x in range(self.flow_field.width):
            for y in range(self.flow_field.height):
                origin_position = Vector(x * FIELD_SCALE, y * FIELD_SCALE)
                target_position = Vector(origin_position.x + self.flow_field.forces[x][y].x * FIELD_SCALE,
                                         origin_position.y + self.flow_field.forces[x][y].y * FIELD_SCALE)
                self.draw_line_from_position_to_position((x * FIELD_SCALE, y * FIELD_SCALE),
                                                         (target_position.x, target_position.y),
                                                         color=(40, 123, 222), size=1)
                pygame.draw.circle(self.screen, (40, 123, 222), (x * FIELD_SCALE, y * FIELD_SCALE), 2)

    def draw_angles(self):
        angles_surface = self.screen.convert_alpha()
        angles_surface.fill([0, 0, 0, 0])
        for x in range(self.flow_field.width):
            for y in range(self.flow_field.height):
                color = utils.translate(self.flow_field.angles[x][y], 0, 360, 0, 255)
                pygame.draw.circle(angles_surface, (color, color, color), (x * FIELD_SCALE, y * FIELD_SCALE), 10)
        self.screen.blit(angles_surface, (0, 0))

    # def create_flow(self):
    #     global z_off
    #     x_off = 0
    #     for x in range(self.cols_num):
    #         y_off = 0
    #         for y in range(self.rows_num):
    #             angle = noise.pnoise3(x_off / SCALE, y_off / SCALE, z_off / SCALE, self.seed) * 360
    #             y_off += FLOW_VARIETY
    #             index = x + y * self.cols_num
    #             origin_position = Vector(x * SCALE, y * SCALE)
    #             target_position = move_in_direction(x * SCALE, y * SCALE, angle, SCALE)
    #             flow_vector = Vector(target_position.x - origin_position.x, target_position.y - origin_position.y)
    #             self.flow_field[index] = flow_vector
    #             if DRAW_FLOW:
    #                 self.draw_line_from_position_to_position((x * SCALE, y * SCALE), (target_position.x, target_position.y), color=(40, 123, 222), size=2)
    #         x_off += FLOW_VARIETY
    #         z_off += FLOW_CHANGE

    def capture(self, count):
        pygame.image.save(self.screen, f"Screenshots/background_{count}.jpeg")

    def change_color(self, amount=10):
        # Choose a random color channel to modify
        channel = random.randint(0, 2)

        # Create a list from the current color tuple
        color_list = list(self.changing_color)

        # Increment or decrement the chosen color channel by a random amount
        delta = random.randint(-amount, amount)
        color_list[channel] += delta

        # Clamp the color channel value to the valid range of 0-255
        color_list[channel] = max(0, min(255, color_list[channel]))

        # Convert the modified color back to a tuple and store it in the class attribute
        self.changing_color = tuple(color_list)
