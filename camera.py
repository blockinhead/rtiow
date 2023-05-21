import math

from ray import Ray
from vec3 import Vec3, Point3


class Camera:
    def __init__(self,
                 look_from: Point3,
                 look_at: Point3,
                 up: Vec3 = Vec3(0.0, 1.0, 0.0),
                 vertical_fov = 90.0,
                 aspect_ratio = 16.0 / 9.0,
                 focal_length = 1.0,
                 ):
        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * math.tan(math.radians(vertical_fov) / 2)
        self.viewport_width = aspect_ratio * self.viewport_height
        self.focal_length = focal_length  # currently not used anymore

        self.w = (look_from - look_at).normalized()
        self.u = Vec3.cross(up, self.w).normalized()
        self.v = Vec3.cross(self.w, self.u)

        self.origin = look_from
        self.horizontal = self.viewport_width * self.u
        self.vertical = self.viewport_height * self.v

        self.lower_left_corner = self.origin \
                                 - self.horizontal / 2 \
                                 - self.vertical / 2 \
                                 - self.w

    def get_ray(self, u: float, v: float) -> Ray:
        return Ray(origin=self.origin,
                   direction=self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
    