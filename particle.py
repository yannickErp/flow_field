import pygame
from line_profiler_pycharm import profile
from physics_classes import Vector
from flow_field import FlowField


class Particle:
    def __init__(self, pos: Vector, vel: Vector, mass: float, radius: float, max_speed: float, color: tuple):
        self.pos = pos
        self.old_pos = self.pos.copy()
        self.vel = vel
        self.acc = Vector(0, 0)
        self.mass = mass
        self.color = color
        self.radius = radius
        self.max_speed = max_speed

    def update(self, flow_field: FlowField, field_scale: int, width: int, height: int):
        self.update_previous_position()
        self.check_edges(width, height)
        self.follow_flow_field(flow_field, field_scale)
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        if self.vel.mag() > self.max_speed:
            self.vel.set_mag(self.max_speed)
        self.vel.limit(self.max_speed)
        self.acc.mult(0)

    def apply_force(self, force: Vector):
        force.div(self.mass)
        self.acc.add(force)

    def update_previous_position(self):
        self.old_pos = self.pos.copy()

    def check_edges(self, screen_width: int, screen_height: int):
        if self.pos.x >= screen_width:
            self.pos.x -= screen_width
            self.update_previous_position()
        elif self.pos.x <= 0:
            self.pos.x += screen_width
            self.update_previous_position()
        if self.pos.y >= screen_height:
            self.pos.y -= screen_height
            self.update_previous_position()
        elif self.pos.y <= 0:
            self.pos.y += screen_height

    def follow_flow_field(self, flow_field: FlowField, field_scale: int):
        flow_field_x = int(self.pos.x / field_scale)
        flow_field_y = int(self.pos.y / field_scale)
        field_vector = flow_field.forces[flow_field_x][flow_field_y]
        force = field_vector.copy()
        self.apply_force(force)
