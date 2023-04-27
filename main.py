import random

from camera import Camera
from color import Color
from hittable import HittableList, Hittable
from ray import Ray
from sphere import Sphere
from vec3 import Point3, Vec3
from math import sqrt


def hit_sphere(center: Point3, radius: float, r: Ray) -> float:
    oc = r.origin - center
    a = r.direction.len_squared
    half_b = Vec3.dot(oc, r.direction)
    c = oc.len_squared - radius * radius
    discriminant = half_b * half_b - a * c
    if discriminant < 0:
        return -1
    else:
        return (-half_b - sqrt(discriminant)) / a


def ray_color(r: Ray, world: Hittable) -> Color:
    if hit_record := world.hit(r, 0, float('inf')):
        normal = hit_record.normal
        normal += Vec3(1, 1, 1)
        normal *= 0.5
        return Color.from_vec3(normal)

    unit_direction = r.direction.normalized()
    t = 0.5 * (unit_direction.y + 1)
    return (1 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1.0)


# image
aspect_ratio = 16 / 9
image_width = 200
image_height = int(image_width / aspect_ratio)
sample_per_pixel = 100

# world
world = HittableList()
world.add(Sphere(Point3(0, 0, -1), 0.5))
world.add(Sphere(Point3(0, -100.5, -1), 100))

# camera
camera = Camera()

# render
with open('image.ppm', 'w') as f:
    f.writelines(['P3\n',
                  '%d %d\n' % (image_width, image_height),
                  '255\n'])

    for j in range(image_height, 0, -1):
        print(f'scanlines remaining: {j}')
        for i in range(image_width):
            pixel_color = Color(0.0, 0.0, 0.0)
            for _ in range(sample_per_pixel):
                u = (i + random.random()) / (image_width - 1)
                v = (j + random.random()) / (image_height - 1)
                ray = camera.get_ray(u, v)
                pixel_color += ray_color(ray, world)
            pixel_color /= sample_per_pixel
            pixel_color.write_to(f)
