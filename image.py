from color import Color


class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        l = width * height
        self._image_r = [0] * l
        self._image_g = [0] * l
        self._image_b = [0] * l

    def __setitem__(self, index: tuple, color: Color):
        row, column = index
        self._image_r[column + row * self.width] = int(color.x * 255.999)
        self._image_g[column + row * self.width] = int(color.y * 255.999)
        self._image_b[column + row * self.width] = int(color.z * 255.999)

    def write_to(self, file_name: str):
        with open(file_name, 'w') as f:
            f.writelines(['P3\n',
                          '%d %d\n' % (self.width, self.height),
                          '255\n'])

            for row in range(self.height - 1, -1, -1):
                for col in range(self.width):
                    f.write('%d %d %d ' % (self._image_r[col + row * self.width],
                                           self._image_g[col + row * self.width],
                                           self._image_b[col + row * self.width]))
