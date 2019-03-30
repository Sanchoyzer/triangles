from datetime import datetime
from random import uniform

from PIL import Image, ImageDraw


class BaseTriangleException(Exception):
    pass


class BadInput(BaseTriangleException):
    pass


class SavePicFail(BaseTriangleException):
    pass


class Point:
    __slots__ = 'x', 'y'

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def distance_by_x(self, p):
        return abs((self - p).x)

    def distance_by_y(self, p):
        return abs((self - p).y)

    def middle(self, p):
        return Point((self.x + p.x) / 2, (self.y + p.y) / 2)


class Triangle:
    __slots__ = 'a', 'b', 'c'

    def __init__(self, a: Point, b: Point, c: Point):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return '({}, {}, {})'.format(self.a, self.b, self.c)

    def get_new_triangles(self, k: float):
        middle_a = self.a.middle(self.b)
        middle_b = self.b.middle(self.c)
        middle_c = self.c.middle(self.a)

        new_a = Point(
            middle_a.x + uniform(-k, +k) * middle_a.distance_by_x(middle_b),
            middle_a.y + uniform(-k, +k) * middle_a.distance_by_y(middle_b),
        )
        new_b = Point(
            middle_b.x + uniform(-k, +k) * middle_b.distance_by_x(middle_c),
            middle_b.y + uniform(-k, +k) * middle_b.distance_by_y(middle_c),
        )
        new_c = Point(
            middle_c.x + uniform(-k, +k) * middle_c.distance_by_x(middle_a),
            middle_c.y + uniform(-k, +k) * middle_c.distance_by_y(middle_a),
        )

        return [
            Triangle(self.a, new_a, new_c),
            Triangle(self.b, new_b, new_a),
            Triangle(self.c, new_c, new_b),
        ]

    def get_sides_for_print(self):
        return [
            (self.a.x, self.a.y, self.b.x, self.b.y),
            (self.b.x, self.b.y, self.c.x, self.c.y),
            (self.c.x, self.c.y, self.a.x, self.a.y),
        ]

    def get_max_coord(self):
        return max(self.a.x, self.b.x, self.c.x), max(self.a.y, self.b.y, self.c.y)


class TriangleManager:
    __slots__ = 'n', 'k', 'w', 'h', 'pic_name', 'log_file', 'pic_type', 'triangle_list'

    def __init__(self, n, k, w, h, pic_name):
        self.log_file = 'log'
        self.pic_type = 'png'

        self.write_log('create: n = {}, k = {}, w = {}, h = {}, pic_name = {!r}'.
                       format(n, k, w, h, pic_name))
        self._check_input(n, k, w, h, pic_name)
        self.pic_name = f'{pic_name}.{self.pic_type}'
        self.n = n
        self.k = k
        self.w = w
        self.h = h
        self.triangle_list = [Triangle(Point(w / 2, 0), Point(0, h), Point(w, h))]

    def __str__(self):
        result = [str(t) for t in self.triangle_list]
        return '[{}]'.format(', '.join(result))

    def write_log(self, msg):
        with open(self.log_file, 'a') as f:
            f.write('[{}] {}\n'.
                    format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))

    def _check_input(self, n, k, w, h, pic_name):
        if not isinstance(n, int) or (n <= 0):
            self.write_log('"n" incorrect')
            raise BadInput('n')

        if not isinstance(k, float) or (k <= 0) or (k >= 1):
            self.write_log('"k" incorrect')
            raise BadInput('k')

        if not isinstance(w, int) or (w <= 0):
            self.write_log('"w" incorrect')
            raise BadInput('w')

        if not isinstance(h, int) or (h <= 0):
            self.write_log('"h" incorrect')
            raise BadInput('h')

        if pic_name is None or pic_name == '':
            self.write_log('"pic_name" incorrect')
            raise BadInput('pic_name')

    def _create_triangles(self):
        for i in range(self.n):
            self.write_log('step = {}, before {}'.format(i, self))
            new_list = []
            for t in self.triangle_list:
                new_list.extend(t.get_new_triangles(self.k))
            self.triangle_list = new_list
            self.write_log('step = {}, after {}'.format(i, self))

    def _get_max_coord(self):
        max_x, max_y = 0, 0
        for t in self.triangle_list:
            x, y = t.get_max_coord()
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return int(max_x) + 1, int(max_y) + 1

    def _save_pic(self):
        im = Image.new('RGB', self._get_max_coord(), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for t in self.triangle_list:
            for side in t.get_sides_for_print():
                draw.line(side, fill=0)
        del draw

        try:
            im.save(self.pic_name, self.pic_type)
        except (ValueError, IOError, KeyError) as exc:
            self.write_log('save pic fail: {}'.format(exc))
            raise SavePicFail(str(exc))
        else:
            self.write_log('save pic: {!r}'.format(self.pic_name))

    def get_picture(self):
        self._create_triangles()
        self._save_pic()
