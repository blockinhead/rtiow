from hittable import Hittable, HitRecord
from vec3 import Vec3, Point3
from ray import Ray
from math import sqrt


class Sphere(Hittable):
    def __init__(self, center=Point3(0, 0, 0), radius=1.0):
        self.center = center
        self.radius = radius

    def hit(self, r: Ray, t_min: float, t_max: float) -> HitRecord | None:
        oc = r.origin - self.center
        a = r.direction.len_squared
        half_b = Vec3.dot(oc, r.direction)
        c = oc.len_squared - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return None

        sqrt_d = sqrt(discriminant)
        root = (-half_b - sqrt_d) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrt_d) / a
            if root < t_min or root > t_max:
                return None

        p = r.at(root)
        normal=(p - self.center) / self.radius
        front_face = Vec3.dot(r.direction, normal) < 0
        normal = normal if front_face else -normal

        return HitRecord(p=p,
                         t=root,
                         normal=normal,
                         front_face=front_face)


