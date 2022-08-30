import unittest
from vec3 import Vec3, Point3


class Ray(object):
    def __init__(self, origin=Point3(), direction=Vec3()):
        self._origin = origin
        self._direction = direction

    @property
    def origin(self) -> Point3:
        return self._origin

    @property
    def direction(self) -> Vec3:
        return self._direction

    def at(self, t: float) -> Point3:
        return self._origin + self._direction * t

    def __repr__(self):
        return f'Ray({self.origin} {self.direction})'


class TestRay(unittest.TestCase):
    def test_at(self):
        self.assertEqual(Ray(Point3(), Vec3(1.0, 0.0, 0.0)).at(2.0), Point3(2.0, 0.0, 0.0))
