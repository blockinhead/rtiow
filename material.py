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
    def scatter(self, ray: Ray, hit_record: HitRecord) -> Scattered | None:
        pass


class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, ray: Ray, hit_record: HitRecord) -> Scattered | None:
        scatter_direction = hit_record.normal + Vec3.random_in_unit_sphere().normalized()
        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        return Scattered(attenuation=self.albedo,
                         ray=Ray(hit_record.p, scatter_direction))


class Metal(Material):
    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = min(float(fuzz), 1.0)

    def scatter(self, ray: Ray, hit_record: HitRecord) -> Scattered | None:
        reflected = ray.direction.normalized().reflect_by(hit_record.normal)
        scattered_ray = Ray(hit_record.p, reflected + self.fuzz * Vec3.random_in_unit_sphere())
        if Vec3.dot(scattered_ray.direction, hit_record.normal) > 0:
            return Scattered(attenuation=self.albedo,
                             ray=scattered_ray)
