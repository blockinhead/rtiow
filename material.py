from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from vec3 import Vec3
from ray import Ray

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from color import Color
    from hittable import HitRecord


@dataclass
class Scattered:
    attenuation: Color
    ray: Ray


class Material(ABC):
    @abstractmethod
    def scatter(self, ray: Ray, hit_record: HitRecord) -> Scattered:
        pass


class Lambertian(Material):
    def __init__(self, color: Color):
        self.albedo = color

    def scatter(self, ray: Ray, hit_record: HitRecord) -> Scattered:
        scatter_direction = hit_record.normal + Vec3.random_in_unit_sphere().normalized()
        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        return Scattered(attenuation=self.albedo,
                         ray=Ray(hit_record.p, scatter_direction))
