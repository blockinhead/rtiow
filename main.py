from color import Color

HEIGHT, WIDTH = 255, 255

with open('image.ppm', 'w') as f:
    f.writelines(['P3\n',
                  '%d %d\n' % (WIDTH, HEIGHT),
                  '255\n'])

    for j in range(HEIGHT, 0, -1):
        for i in range(WIDTH):
            Color(i / WIDTH, j / HEIGHT, 0.25).write_to(f)
