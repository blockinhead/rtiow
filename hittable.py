from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from material import Material
from ray import Ray
from vec3 import Vec3, Point3


@dataclass
class HitRecord:
    p: Point3
    normal: Vec3
    material: Material
    t: float
    front_face: bool = True

    def set_face_normal(self, ray: Ray) -> HitRecord:
        self.front_face = Vec3.dot(ray.direction, self.normal) < 0
        self.normal = self.normal if self.front_face else -self.normal

        return self


class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float) -> HitRecord | None:
        pass


class HittableList(Hittable):
    def __init__(self):
        self.objects: list[Hittable] = []

    def add(self, obj: Hittable):
        self.objects.append(obj)

    def hit(self, r: Ray, t_min: float, t_max: float) -> HitRecord | None:
        closest = t_max
        res = None

        for obj in self.objects:
            if hr := obj.hit(r, t_min, closest):
                res = hr
                closest = hr.t

        return res
