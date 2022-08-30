from color import Color
from ray import Ray
from vec3 import Point3, Vec3


def ray_color(r: Ray) -> Color:
    unit_direction = r.direction.normalized()
    t = 0.5 * (unit_direction.y + 1)
    return (1 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1.0)


# image
aspect_ratio = 16 / 9
image_width = 50
image_height = int(image_width / aspect_ratio)


# camera
viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0

origin = Point3(0, 0, 0)
horizontal = Vec3(viewport_width, 0, 0)
vertical = Vec3(0, viewport_height, 0)
lower_left_corner = origin - horizontal / 2 - vertical / 2 - Vec3(0, 0, focal_length)


# render
with open('image.ppm', 'w') as f:
    f.writelines(['P3\n',
                  '%d %d\n' % (image_width, image_height),
                  '255\n'])

    for j in range(image_height, 0, -1):
        for i in range(image_width):
            u = i / (image_width - 1)
            v = j / (image_height - 1)
            direction = lower_left_corner + u * horizontal + v * vertical - origin
            ray = Ray(origin=origin,
                      direction=direction)
            ray_color(ray).write_to(f)
