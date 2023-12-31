from __future__ import annotations

import math
import typing
import random
import unittest


class CannotRefract(Exception):
    pass


class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __repr__(self):
        return f'Vec3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})'

    def __eq__(self, other: Vec3):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __iadd__(self, other: Vec3):
        self._x += other._x
        self._y += other._y
        self._z += other._z
        return self

    def __imul__(self, other: float):
        self._x *= other
        self._y *= other
        self._z *= other
        return self

    def __idiv__(self, other: float):
        self._x /= other
        self._y /= other
        self._z /= other
        return self

    @property
    def len_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    @property
    def length(self) -> float:
        return pow(self.len_squared, 0.5)

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z)

    def write_to(self, fp: typing.TextIO):
        fp.write('%f %f %f ' % (self.x, self.y, self.z))

    def __add__(self, other: Vec3) -> Vec3:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: [Vec3, float]) -> Vec3:
        if isinstance(other, Vec3):
            return self.__class__(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, float):
            return self.__class__(self.x * other, self.y * other, self.z * other)
        else:
            raise Exception(f'unsupported arg type {type(other)} for Vec3 multiplication')

    def __rmul__(self, other: [Vec3, float]) -> Vec3:
        return self.__mul__(other)

    def __truediv__(self, other: float):
        return self * (1 / other)

    def normalized(self) -> Vec3:
        return self * (1 / self.length)

    def near_zero(self) -> bool:
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s

    def reflect_by(self, normal: Vec3) -> Vec3:
        return self - 2 * Vec3.dot(self, normal) * normal

    def refract(self, normal: Vec3, etai_over_etat: float) -> Vec3:
        cos_theta = min(Vec3.dot(-self, normal), 1.0)
        sin_theta = math.sqrt(1 - cos_theta * cos_theta)
        if etai_over_etat * sin_theta > 1.0 or self._reflectance(cos_theta, etai_over_etat) > random.random():
            raise CannotRefract()

        r_out_perpendicular = etai_over_etat * (self + cos_theta * normal)
        r_out_parallel = -math.sqrt(abs(1 - r_out_perpendicular.len_squared)) * normal
        return r_out_perpendicular + r_out_parallel

    @staticmethod
    def _reflectance(cos_theta: float, refraction_ratio: float):
        r0 = (1 - refraction_ratio) / (1 + refraction_ratio)
        r0 = r0 * r0
        return r0 + (1 - r0) * math.pow((1 - cos_theta), 5)


    @staticmethod
    def dot(a: Vec3, b: Vec3) -> float:
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross(a: Vec3, b: Vec3) -> Vec3:
        return Vec3(a.y * b.z - a.z * b.y,
                    a.z * b.x - a.x * b.z,
                    a.x * b.y - a.y * b.x)

    @staticmethod
    def random_in_unit_square() -> Vec3:
        return Vec3(random.random(), random.random(), random.random())

    @staticmethod
    def random_in_unit_sphere() -> Vec3:
        while True:
            if (res := Vec3.random_in_unit_square() * 2.0 - Vec3(1.0, 1.0, 1.0)).len_squared < 1:
                return res

    @staticmethod
    def random_in_unit_disk() -> Vec3:
        while True:
            if (res := Vec3(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0)).len_squared < 1:
                return res


class Point3(Vec3):
    pass


class TestVec3(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(Vec3(0, 0, 0), Vec3())

    def test_neg(self):
        self.assertEqual(-Vec3(1, 2, 3), Vec3(-1, -2, -3))

    def test_normalize(self):
        self.assertEqual(Vec3(2, 0, 0).normalized(), Vec3(1, 0, 0))

    def test_random(self):
        self.assertLess(Vec3.random_in_unit_sphere().len_squared, 1)

    def test_refract(self):
        v = Vec3.random_in_unit_square()
        v._y = -(v.y * v.y + 0.1)  # to make it always fall
        v = v.normalized()
        up = Vec3(0.0, 1.0, 0.0)  # to refract on horizontal surface
        self.assertTrue((v - v.refract(up, 1.0)).near_zero())
