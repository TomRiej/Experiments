from math import sqrt

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @ staticmethod
    def sub(vec1, vec2):
        return Vector(vec2.x - vec1.x, vec2.y-vec1.y)

    def getMagnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.getMagnitude()
        self.x = self.x/mag
        self.y = self.y/mag

    def mult(self, s):
        self.x *= s
        self.y *= s

    def add(self, vect):
        self.x += vect.x
        self.y += vect.y