import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other_vector: 'Vector'):
        self.x += other_vector.x
        self.y += other_vector.y

    def sub(self, other_vector: 'Vector'):
        self.x -= other_vector.x
        self.y -= other_vector.y

    def mult(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def div(self, scalar):
        self.x /= scalar
        self.y /= scalar

    def negate(self):
        self.x = -self.x
        self.y = -self.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def set_mag(self, mag):
        self.normalize()
        self.mult(mag)

    def normalize(self):
        m = self.mag()
        if m != 0:
            self.div(m)

    def to_string(self):
        return f'x: {self.x}, y: {self.y}'

    def copy(self):
        return Vector(self.x, self.y)

    def limit(self, speed_max):
        if self.mag() > speed_max:
            self.normalize()
            self.mult(speed_max)
