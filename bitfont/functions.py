# file of various grid related functions

import math


def points_to_rect(p1, p2):
    """Given two points, returns rect bound by p1 and p2."""
    x1, y1 = p1
    x2, y2 = p2

    if (x1 == x2) and (y1 == y2):
        # same point
        return x1, y1, 1, 1
    elif x1 == x2:
        # vertical line
        y = y1 if y1 < y2 else y2
        h = int(math.fabs(y1 - y2) + 1)
        return x1, y, 1, h
    elif y1 == y2:
        # horizontal line
        x = x1 if x1 < x2 else x2
        w = int(math.fabs(x1 - x2) + 1)
        return x, y1, w, 1
    else:
        clause1 = x1 < x2
        clause2 = y1 < y2
        if clause1 and clause2:
            # p1 is top left, p2 is bottom right
            w = int(math.fabs(x1 - x2) + 1)
            h = int(math.fabs(y1 - y2) + 1)
            return x1, y1, w, h
        elif clause1 and not clause2:
            # p1 is bottom left, p2 is top right
            w = int(math.fabs(x1 - x2) + 1)
            h = int(math.fabs(y1 - y2) + 1)
            return x1, y2, w, h
        elif clause2 and not clause1:
            # p1 is top right, p2 is bottom left
            w = int(math.fabs(x1 - x2) + 1)
            h = int(math.fabs(y1 - y2) + 1)
            return x2, y1, w, h
        elif not clause1 and not clause2:
            # p1 is bottom right, p2 is top left
            w = int(math.fabs(x1 - x2) + 1)
            h = int(math.fabs(y1 - y2) + 1)
            return x2, y2, w, h
        else:
            raise RuntimeError("If you get this error, you are beyond help.")


def point_distances(p1, p2):
    """Returns the x and y difference between two points."""
    return p2[0] - p1[0], p2[1] - p1[1]


def angle_between_points(p1, p2, full_circle=False, negate_y=True):
    """Returns angle from p1 to p2 utilizing math.atan2().
    Returns angle in radians between -pi and pi.
    If full_circle is True, then returns angle between 0 and tau (2 * pi).
    Defaults to negating y due to y axis in video graphics going down.
    Pass False to the negate_y argument for normal Cartesian grid behavior."""
    dx, dy = point_distances(p1, p2)
    # negate for video graphics negative y axis
    if negate_y:
        dy = -dy
    angle = math.atan2(dy, dx)
    # if full_circle, then change negative angles into angles between 0 and math.tau
    if full_circle and angle < 0:
        angle += math.tau
    return angle


def dist_between_points(p1, p2):
    """Returns actual distance between two points with math.sqrt() function."""
    dx, dy = point_distances(p1, p2)
    return math.sqrt(dx ** 2 + dy ** 2)


def dist_sqrd_between_points(p1, p2):
    """Returns squared distance of two points.
    Lack of math.sqrt() call makes this faster, so use when you can."""
    dx, dy = point_distances(p1, p2)
    return dx ** 2 + dy ** 2


def angle_in_arc(angle, start_angle, stop_angle):
    """Returns true if angle lies within arc described by start_angle and end_angle.
    All angles should be given in degrees.
    Arc starts at start_angle and goes counter-clockwise until stop_angle is reached."""
    # normalize all angles with modulo, this works with negative numbers too
    angle %= 360
    start_angle %= 360
    stop_angle %= 360
    # if the arc is just a line
    if start_angle == stop_angle:
        # angle must be equal to the line
        return angle == start_angle
    # if start_angle < stop_angle, use a chained comparison
    if start_angle < stop_angle:
        return start_angle <= angle <= stop_angle
    # otherwise, the zero line has been crossed and we must adjust the angles
    else:
        # adjust stop_angle so chained comparison is valid
        stop_angle += 360
        # if angle is over (or on) the zero line, then adjust it as well
        # angle must be over (or on) zero, but also less than start_angle
        if 0 <= angle < start_angle:
            angle += 360
        return start_angle <= angle <= stop_angle


def point_in_rect(pos, rect):
    """Returns true if given point is inside the given rect."""
    return rect[0] <= pos[0] < (rect[2] + rect[0]) and rect[1] <= pos[1] < (rect[3] + rect[1])


def point_in_circle(pos, center, radius):
    """Returns true if given point is inside the given circle."""
    # print(dist_sqrd_between_points(pos, center), radius**2)
    return dist_sqrd_between_points(pos, center) <= radius ** 2


def point_in_ellipse(pos, center, rx, ry):
    """Returns true if given point lies inside given ellipse with given axes"""
    dx, dy = point_distances(pos, center)
    return (dx ** 2 / rx ** 2) + (dy ** 2 / ry ** 2) <= 1


def lerp(start, end, t):
    """Linear interpolation, returns float except when t is 0 or 1."""
    return start + t * (end - start)


def lerp_point(p1, p2, t):
    """Lerps between two points, point returned has float coors."""
    return lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t)


def round_point(p):
    """Rounds point's coors to nearest integer, according to python rounding."""
    return round(p[0]), round(p[1])


def floor_point(p):
    """Truncates x and y of point to integers."""
    return int(p[0]), int(p[1])


def slope_of_points(p1, p2):
    """Returns slope between points according to rise/run formula.
    REMEMBER: Points that have the y axis reversed will be negative."""
    dx, dy = point_distances(p1, p2)
    return dy / dx


def diagonal_distance(p1, p2):
    """Returns the diagonal distance between two points.
    Diagonal distance is abs of the largest distance, x or y."""
    dx, dy = point_distances(p1, p2)
    return int(max(math.fabs(dx), math.fabs(dy)))


def manhattan_distance(p1, p2):
    """Returns the manhattan distance between two points.
    Manhattan distance is delta x + delta y."""
    dx, dy = point_distances(p1, p2)
    return int(math.fabs(dx) + math.fabs(dy))


def simple_direction(p1, p2):
    """Takes two points and gives one of the nine directions from p1 to p2.
    The nine directions are arranged on a grid:
    X|X|X
    X|X|X
    X|X|X
    REMEMBER: Y axis is reversed, just like computer graphics.
    If points fall perfectly on the line, corner directions will be chosen."""
    # p1 is to the right of p2
    clause1 = p1[0] > p2[0]
    # p1 is lower than p2
    clause2 = p1[1] > p2[1]

    # picks between directions based on clause
    def clause_axis(clause, yes, no):
        """This section of code is used a lot in the main code.
        If the clause is true, returns yes, otherwise returns no.
        Slopes repeat twice over the whole circle of angles, so clauses are
        used to determine which slope to actually return."""
        if clause:
            return yes
        return no

    # vertical line
    if p1[0] == p2[0]:
        # if y coors are equal too
        if p1[1] == p2[1]:
            # same point
            return 0, 0
        # otherwise, pick up or down direction
        return clause_axis(clause2, (0, 1), (0, -1))
    # begin main formula by getting slope of the points
    slope = slope_of_points(p1, p2)
    # horizontal lines
    if slope == 0:
        return clause_axis(clause1, (-1, 0), (1, 0))
    if 0 < slope < 0.5:
        return clause_axis(clause1, (-1, 0), (1, 0))
    if 0 > slope > -0.5:
        return clause_axis(clause1, (-1, 0), (1, 0))
    # vertical lines
    if slope > 2 or slope < -2:
        return clause_axis(clause2, (0, 1), (0, -1))
    # top right and bottom left
    if -0.5 >= slope >= -2:
        return clause_axis(clause1, (-1, -1), (1, 1))
    # top left and bottom right
    if 0.5 <= slope <= 2:
        return clause_axis(clause1, (-1, 1), (1, -1))
