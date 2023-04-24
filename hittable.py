from abc import ABC, abstractmethod
from dataclasses import dataclass
from ray import Ray
from vec3 import Vec3, Point3


@dataclass
class HitRecord:
    p: Point3
    normal: Vec3
    t: float
    front_face: bool


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
