import unittest
from vec3 import Vec3


class TestVec3(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(Vec3(0, 0, 0), Vec3())

    def test_neg(self):
        self.assertEqual(-Vec3(1, 2, 3), Vec3(-1, -2, -3))

    def test_normalize(self):
        self.assertEqual(Vec3(2, 0, 0).normalize(), Vec3(1, 0, 0))


if __name__ == '__main__':
    unittest.main()
