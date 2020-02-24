from fractions import Fraction
from itertools import chain
from math import gcd


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
        def to_float(x):
            return float(Fraction(x))

        for x1, y1, x2, y2 in segments:
            yield f'<line x1="{round(self._margin + to_float(x1) * self._unit, 2)}"' \
                  f' y1="{round(self._margin + (self._p - to_float(y1)) * self._unit, 2)}"' \
                  f' x2="{round(self._margin + to_float(x2) * self._unit, 2)}"' \
                  f' y2="{round(self._margin + (self._p - to_float(y2)) * self._unit, 2)}"' \
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
        template.add_segments(segments(*translate(3, -1, -2), p), stroke='#ffff00'),
        template.add_segments(segments(*translate(2, -3, -6), p), stroke='#00ffff'),
        template.add_segments(segments(*translate(1, 2, -3), p), stroke='#ff00ff'),
        add_points())
    template.make_svg('../assets/finite_geometry.svg', contents)


def make_test_svg():
    p = 12
    margin, unit = 10, 30
    template = SvgTemplate(p, margin=margin, unit=unit)
    contents = chain(
        template.add_segments(segments(2, -1, 0, p), stroke='#ffff00'),
        template.add_segments(segments(3, 4, 0, p), stroke='#00ffff'))
    template.make_svg('../assets/fg.svg', contents)


def segments(a, b, c, m):
    """a and be are non-zero ints, c is a Fraction, m is a positive Fraction"""
    c, m = Fraction(c), Fraction(m)
    if a < 0:
        a, b, c = -a, -b, -c
    d = gcd(a, b)
    if d > 1:
        a, b, c = a // d, b // d, c / d

    # If b < 0 (i.e., the slope is positive), flip line across x-axis, and then flip
    # the results back. This reduces the number of cases to consider.
    b, flipped = abs(b), b < 0
    c = c % -m  # -m < c <= 0

    pts = sorted({(x * m, (-a * x * m - c) / b) for x in range(b + 1)} \
                 | {((b * -y * m + c) / -a, -y * m) for y in range(a)})
    res = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        x1, y1, x2, y2 = x1 % m, y1 % -m + m, x2 % -m + m, y2 % m
        seg = (x1, m - y1, x2, m - y2) if flipped else (x1, y1, x2, y2)
        res.append(tuple(str(coord) for coord in seg))
    return res


if __name__ == "__main__":
    make_test_svg()
    # make_finite_geom_svg()
