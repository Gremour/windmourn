# -*- coding: utf-8 -*-


def bresenham(start, end):
    """Returns list of tuples of coords, forming a Bresenham line
    from start to end."""

    assert len(start) == 2 and len(end) == 2, "function requires tuples of 2d coords, i.e.: (1, 4), (7, 2)"

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    ydir = 1 if dy >= 0 else -1
    xdir = 1 if dx >= 0 else -1
    if ydir < 0:
        dy = -dy
    if xdir < 0:
        dx = -dx
    dx, dy = dx + 1, dy + 1
    hor = dx > dy
    if not hor:
        dx, dy = dy, dx
    res = []
    e = 0
    y = 0
    for x in range(dx):
        if hor:
            res.append((start[0] + x * xdir, start[1] + y * ydir))
        else:
            res.append((start[0] + y * xdir, start[1] + x * ydir))
        e += dy
        if e >= dx:
            e -= dx
            y += ydir

    return res


def count_steps(crd_list):
    return [[y for (x, y) in crd_list].count(z) for z in set([y for (x, y) in crd_list])]

