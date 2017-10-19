# -*- coding: utf-8 -*-
# Some algorithms to use


def bresenham(start_point, end_point, start=0, end=-1, step=1):
    """This is generator for Bresenham line.

    Generates tuples of coordinates, forming a Bresenham line from start_point to end_point.
    start and end should contain tuples of 2d coordinates, i. e.: (1, 4), (7, 2)"""

    assert len(start_point) == 2 and len(end_point) == 2, "function requires tuples of 2d coords, i. e.: (1, 4), (7, 2)"

    if start_point == end_point:
        yield start_point
        return

    # Calculate deltas (size of strip in pixels for x and y).
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]

    # Calculate directions of strip for x and y and make dx and dy positive integers.
    ydir = 1 if dy >= 0 else -1
    xdir = 1 if dx >= 0 else -1
    if ydir < 0:
        dy = -dy
    if xdir < 0:
        dx = -dx

    # We're including last point, so increment dx and dy.
    dx, dy = dx + 1, dy + 1

    # If dx is larger, than dy, the strip is horizontally oriented.
    hor = dx > dy

    # Otherwise, swap dx and dy, and keep that in mind.
    if not hor:
        dx, dy = dy, dx

    # At this point, both dx and dy are positive, dx is larger than dy,
    # and Bresenhem line is calculated in first octant.
    # Just don't forget to do reverse calculations before we return value.

    # We're going to create a list of straight horizontal parts of the line.
    # Example:   dx = 10, dy = 3
    #       ***
    #          ****
    #              ***
    # The l array must hold [3, 4, 3]

    # Fill l with integer division result, i. e. [3, 3, 3].
    l = [dx // dy] * dy
    # Calculate number of pixels that must be added yet to l.
    o = dx % dy
    if o > 0:
        # Calculate step (in logical pixels) between additions to l.
        ri = dy / o
        # Do o additions distributed evenly over the l.
        for c in range(o):
            i = int(c * ri + ri / 2)
            l[i] += 1

    # At this point, l holds list of straight horizontal parts of the line.

    start_ind = start
    if start < 0:
        start_ind = dx + 1 + start
    end_ind = end
    if end_ind < 0:
        end_ind = dx + 1 + end_ind
    if start_ind > end_ind:
        start_ind, end_ind = end_ind, start_ind
    step_cnt = step
    cur_ind = 0

    x, y = 0, 0
    # Iterate over l.
    for j in l:
        # Each element of l is the number of pixels that must be generated for same y
        for k in range(j):

            # Check for iteration parameters (start, end, step)
            if cur_ind >= end_ind:
                return
            hide = cur_ind < start_ind
            cur_ind += 1
            if hide:
                continue
            else:
                step_cnt += 1
                if step_cnt < step:
                    continue
                else:
                    step_cnt = 0

            # We can yield value now
            if hor:
                # Return current position, plus start position
                yield ((x + k) * xdir + start_point[0], y * ydir + start_point[1])
            else:
                # Remember: we have swapped dx and dy!
                yield (y * xdir + start_point[0], (x + k) * ydir + start_point[1])

        # One line is over. Move x by j, move y by one. Repeat.
        x += j
        y += 1


