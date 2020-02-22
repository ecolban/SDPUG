from itertools import chain
from math import gcd

from src.utils import log


class SvgTemplate(object):

    def __init__(self, p, margin, unit):
        self._margin, self._unit, self._p = margin, unit, p
        self.width, self.height = 2 * self._margin + p * self._unit, 2 * self._margin + p * self._unit
        self._preamble = f'<?xml version="1.0" encoding="UTF-8"?> <svg xmlns="http://www.w3.org/2000/svg" ' \
                         f'width="{self.width}" height="{self.height}">\n' \
                         f'<polygon stroke="none" fill="#000000" points="0 0 {self.width} 0 ' \
                         f'{self.width} {self.height} 0 {self.height}"/>\n' \
                         f'<polygon stroke="#ffffff" fill="none" points="{self._margin} {self._margin} ' \
                         f'{self.width - self._margin} {self._margin} ' \
                         f'{self.width - self._margin} {self.height - self._margin} ' \
                         f'{self._margin} {self.height - self._margin}"/>'

    def add_segments(self, segments, stroke):
        for x1, y1, x2, y2 in segments:
            yield f'<line x1="{round(self._margin + x1 * self._unit, 2)}"' \
                  f' y1="{round(self._margin + (self._p - y1) * self._unit, 2)}"' \
                  f' x2="{round(self._margin + x2 * self._unit, 2)}"' \
                  f' y2="{round(self._margin + (self._p - y2) * self._unit, 2)}"' \
                  f' stroke="{stroke}"/>'

    def make_svg(self, out_file, contents):
        with open(out_file, 'w') as f:
            print(self._preamble, file=f)
            for line in contents:
                print(line, file=f)
            print('</svg>', file=f)


def make_finite_geom_svg():
    p = 7
    margin, unit = 10, 40

    def translate(a, b, c):
        """return a * (x - 0.5) + b * (y - 0.5) + c = 0"""
        return a, b, c - 0.5 * (a + b)

    def add_points():
        for x in range(p):
            for y in range(p):
                if (3 * x + 6 * y + 5) % p == 0:
                    yield f'<circle cx="{margin + (2 * x + 1) * unit // 2}" ' \
                          f'cy="{margin + (2 * (p - y) - 1) * unit // 2}" ' \
                          f'r="4" stroke="#ffffff" fill="#ff0000"/>'
                else:
                    yield f'<circle cx="{margin + (2 * x + 1) * unit // 2}" ' \
                          f'cy="{margin + (2 * (p - y) - 1) * unit // 2}" ' \
                          f'r="2" stroke="#ffffff" fill="#ffffff"/>'

    template = SvgTemplate(p, margin=margin, unit=unit)
    contents = chain(
        template.add_segments(log('yellow')(get_segments)(*translate(3, -1, -2), p), stroke='#ffff00'),
        template.add_segments(log('cyan')(get_segments)(*translate(2, -3, -6), p), stroke='#00ffff'),
        template.add_segments(log('magenta')(get_segments)(*translate(1, 2, -3), p), stroke='#ff00ff'),
        add_points())
    template.make_svg('../assets/finite_geometry.svg', contents)


def make_test_svg():
    p = 12
    margin, unit = 10, 30
    template = SvgTemplate(p, margin=margin, unit=unit)
    contents = chain(
        template.add_segments(log('yellow')(get_segments)(2, -1, 0, p=p), stroke='#ffff00'),
        template.add_segments(log('cyan')(get_segments)(3, 4, 0, p=p), stroke='#00ffff'))
    template.make_svg('../assets/fg.svg', contents)


def get_segments(a, b, c, m):
    """a and be are non-zero ints, c is a float, m is a positive float"""
    if a < 0:
        a, b, c = -a, -b, -c
    d = gcd(a, b)
    if d > 1:
        a, b, c = a // d, b // d, c / d

    # If b < 0 (i.e., the slope is positive), flip line across x-axis, and then flip
    # the results back. This reduces the number of cases to consider.
    b, flipped = abs(b), b < 0
    c = c % -m  # -m < c <= 0

    pts = [(x * m, (-a * x * m - c) / b) for x in range(b + 1)]
    pts += [((b * -y * m + c) / -a, -y * m) for y in range(a)]
    pts.sort()
    res = []
    epsilon = 1e-3
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 0.09:
            # if the length of a segment is less than 0.3, skip it.
            continue
        x1 = 0 if abs(x1 % m - m) < epsilon else x1 % m
        y1 = m if abs(y1 % m) < epsilon else y1 % m
        x2 = m if abs(x2 % m) < epsilon else x2 % m
        y2 = 0 if abs(y2 % m - m) < epsilon else y2 % m
        seg = (x1, m - y1, x2, m - y2) if flipped else (x1, y1, x2, y2)
        res.append(tuple(round(coord, 2) for coord in seg))
    return res


if __name__ == "__main__":
    # make_test_svg()
    make_finite_geom_svg()
