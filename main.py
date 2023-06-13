import random
from pathos.multiprocessing import Pool
from timeit import default_timer as timer

from camera import Camera
from color import Color
from hittable import HittableList, Hittable
from image import Image
from ray import Ray
from sphere import Sphere
from vec3 import Point3, Vec3
from math import sqrt
from material import Lambertian, Metal, Dielectric


def ray_color(r: Ray, world: Hittable, depth: int) -> Color:
    if depth <= 0:
        return Color.black()

    if hit_record := world.hit(r, 0.001, float('inf')):
        if scattered := hit_record.material.scatter(r, hit_record):
            return scattered.attenuation * ray_color(scattered.ray, world, depth - 1)
        return Color.black()

    unit_direction = r.direction.normalized()
    t = 0.5 * (unit_direction.y + 1)
    return (1 - t) * Color.white() + t * Color(0.5, 0.7, 1.0)


# image
aspect_ratio = 16.0 / 9.0
image_width =  800  # 200 # 1600
image_height = int(image_width / aspect_ratio)
sample_per_pixel = 50  # 50  # 250
max_depth = 20  # 20  # 50

# world
world = HittableList()
# world.add(Sphere(Point3(-0.7, 0, -1), -0.3, Dielectric(1.5)))
# world.add(Sphere(Point3(0.0, 0, -1), 0.3, Lambertian(Color(0.3, 0.3, 0.6))))
# world.add(Sphere(Point3(0.7, 0, -1), 0.3, Metal(Color(0.7, 0.3, 0.3), fuzz=0.3)))
world.add(Sphere(Point3(0, -1000, 0), 1000, Lambertian(Color(0.5, 0.5, 0.55))))
# '''
for a in range(-11, 11):
    for b in range(-11, 11):
        if random.random() > 0.45:
            continue
        r = random.random() * 0.2 + 0.2
        world.add(Sphere(center=Point3(a + 0.9 * random.random(), r, b + 0.9 * random.random()),
                         radius=r,
                         material=random.choices((Lambertian(Color.random() * Color.random()),
                                                  Metal(albedo=Color.random(), fuzz=random.uniform(0, 0.5)),
                                                  Dielectric(index_of_refraction=1.5)
                                                 ), (0.4, 0.4, 0.2))[0]
                         )
                  )
# '''

# camera
camera = Camera(look_from=Point3(13.0, 2.0, 3),
                look_at=Point3(0.0, 0.0, 0.0),
                up=Vec3(0.0, 1.0, 0.0),
                vertical_fov=20,
                aspect_ratio=aspect_ratio,
                aperture=0.1)

def calculate_pixel_color(world: HittableList, camera: Camera, i: int, j: int, image_width: int, image_height: int) -> Color:
    rays = [camera.get_ray((i + random.random()) / (image_width - 1), (j + random.random()) / (image_height - 1))
            for _ in range(sample_per_pixel)]
    samples = map(lambda ray: ray_color(ray, world=world, depth=max_depth), rays)
    pixel_color = sum(samples, Color(0.0, 0.0, 0.0))
    pixel_color /= sample_per_pixel
    pixel_color = Color(sqrt(pixel_color.x), sqrt(pixel_color.y), sqrt(pixel_color.z))
    return pixel_color

# render
t = timer()
image = Image(image_width, image_height)

buf_indices = [(j, i) for i in range(image_height) for j in range(image_width)]
with Pool(16) as p:
    buf_colors = p.map(lambda index: calculate_pixel_color(world, camera, index[0], index[1], image_width, image_height),
                       buf_indices)

# buf_colors = map(lambda index: calculate_pixel_color(world, camera, index[0], index[1], image_width, image_height),
#                  buf_indices)

for c, (i, j) in zip(buf_colors, buf_indices):
    image[j, i] = c

image.write_to('image.ppm')

print('done in %.2f seconds' % (timer() - t))
