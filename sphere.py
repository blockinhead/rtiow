from hittable import Hittable, HitRecord
from material import Material
from vec3 import Vec3, Point3
from ray import Ray
from math import sqrt


class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float, material: Material):
        self.center = center
        self.radius = radius
        self.material = material

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

        return HitRecord(p=p,
                         t=root,
                         normal=normal,
                         material=self.material)\
            .set_face_normal(r)
