from __future__ import annotations
import typing
import unittest


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

    @staticmethod
    def dot(a: Vec3, b: Vec3) -> float:
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross(a: Vec3, b: Vec3) -> Vec3:
        return Vec3(a.y * b.z - a.z * b.y,
                    a.z * b.x - a.x * b.z,
                    a.x * b.y - a.y * b.x)


class Point3(Vec3):
    pass


class TestVec3(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(Vec3(0, 0, 0), Vec3())

    def test_neg(self):
        self.assertEqual(-Vec3(1, 2, 3), Vec3(-1, -2, -3))

    def test_normalize(self):
        self.assertEqual(Vec3(2, 0, 0).normalized(), Vec3(1, 0, 0))
