import typing
from vec3 import Vec3


class Color(Vec3):
    def write_to(self, fp: typing.TextIO):
        fp.write('%d %d %d ' % (int(self.x * 255.999), int(self.y * 255.999), int(self.z * 255.999)))

    @classmethod
    def from_vec3(cls, vec3: Vec3):
        return cls(vec3.x, vec3.y, vec3.z)
