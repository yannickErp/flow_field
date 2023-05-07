import math

import noise
import numpy as np
from line_profiler_pycharm import profile
from opensimplex import OpenSimplex

import utils
from config import FLOW_CHANGE
from physics_classes import Vector
from noise import pnoise2


class FlowField:
    def __init__(self, width: int, height: int, flow_variety: float, flow_change: float, seed: int, field_scale: int):
        self.seed = seed
        self.width = width
        self.height = height
        self.flow_variety = flow_variety
        self.flow_change_state = 0
        self.flow_change = flow_change
        self.field_scale = field_scale
        self.angles = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.forces = [[Vector(0, 0) for _ in range(self.width)] for _ in range(self.height)]
        self.calculate_field()

    def calculate_field(self):
        x_off = 0
        simplex_noise = OpenSimplex(seed=self.seed)
        for x in range(self.width):
            y_off = 0
            for y in range(self.height):
                angle = simplex_noise.noise3(x_off / self.field_scale, y_off / self.field_scale, self.flow_change_state / self.field_scale) * 360
                y_off += self.flow_variety
                directional_vector = utils.get_vector_from_angle(angle)
                self.forces[x][y] = directional_vector
                self.angles[x][y] = angle

            x_off += self.flow_variety

    def update_flow_field(self):
        self.flow_change_state += self.flow_change
        self.calculate_field()
