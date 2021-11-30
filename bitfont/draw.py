# file of drawing functions that can be used on CellSurface

from .functions import *

# directions for flood_fill
ORTHOGONAL = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIAGONAL = ((1, 1), (-1, 1), (-1, -1), (1, -1))
CHEBYSHEV = (*ORTHOGONAL, *DIAGONAL)


def horizontal_line(p, length):
    """Returns a set of points that make a horizontal line with given length."""
    points = set()
    for i in range(length):
        points.add((p[0] + i, p[1]))
    return points


def vertical_line(p, length):
    """Returns a set of points that make a vertical line with given length."""
    points = set()
    for i in range(length):
        points.add((p[0], p[1] + i))
    return points


def dda_line(p1, p2):
    """Returns a set of points between p1 and p2 to draw a dda line."""
    # Return if same point.
    if p1 == p2:
        return [p1]
    # Initialize the points list.
    points = []
    # Find number of points to linear interpolate to.
    n = diagonal_distance(p1, p2)
    # Do n+1 linear interpolations.
    for i in range(n + 1):
        # Linear interpolate the point, round to nearest integer point, add to list.
        points.append(round_point(lerp_point(p1, p2, i / n)))
    # Return the points list.
    return points


def orthogonal_line(p1, p2):
    """Returns a set of points between p1 and p2 to draw an orthogonal line.
    When the line passes through a diagonal, vertical steps are chosen."""
    # cannot handle vertical or horizontal lines
    if p1[0] == p2[0] or p1[1] == p2[1]:
        # delegate to dda_line
        return dda_line(p1, p2)
    # get distances, abs distances, and signs
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    nx, ny = math.fabs(dx), math.fabs(dy)
    sign_x, sign_y = math.copysign(1, dx), math.copysign(1, dy)
    # make point list and variables
    p = [p1[0], p1[1]]
    points = set()
    points.add((p[0], p[1]))
    ix = iy = 0
    # loop through line
    while ix < nx or iy < ny:
        if (0.5 + ix) / nx < (0.5 + iy) / ny:
            # horizontal step
            p[0] += sign_x
            ix += 1
        else:
            # vertical step
            p[1] += sign_y
            iy += 1
        # add new point, making sure to cast coordinates to integers
        points.add((int(p[0]), int(p[1])))
    return points


def supercover_line(p1, p2):
    """Returns a set of points between p1 and p2 to draw a supercover line.
    Supercover is like orthogonal, except it supports diagonal steps."""
    # cannot handle vertical or horizontal lines
    if p1[0] == p2[0] or p1[1] == p2[1]:
        # delegate to dda_line
        return dda_line(p1, p2)
    # get distances, abs distances, and signs
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    nx, ny = math.fabs(dx), math.fabs(dy)
    sign_x, sign_y = math.copysign(1, dx), math.copysign(1, dy)
    # make point list and variables
    p = [p1[0], p1[1]]
    points = [(p[0], p[1])]
    ix = iy = 0
    # loop through line
    while ix < nx or iy < ny:
        if (0.5 + ix) / nx == (0.5 + iy) / ny:
            # diagonal step
            p[0] += sign_x
            p[1] += sign_y
            ix += 1
            iy += 1
        elif (0.5 + ix) / nx < (0.5 + iy) / ny:
            # horizontal step
            p[0] += sign_x
            ix += 1
        else:
            # vertical step
            p[1] += sign_y
            iy += 1
        # add new point, making sure to cast coordinates to integers
        points.append((int(p[0]), int(p[1])))
    return points


def filled_circle(center, radius):
    """Returns a set of points that make a filled circle.
    Center and radius don't have to be integers, but look best as N.0 or N.5.
    STYLE GUIDE:
    If center is N.0, radius should be N.5.
    If center is N.5, radius should be N.0."""
    points = set()
    # create dimensions for bounding rectangle
    top = center[1] - radius
    bottom = center[1] + radius
    left = center[0] - radius
    right = center[0] + radius
    # begin looping through bounding rectangle
    y = top
    while y <= bottom:
        x = left
        while x <= right:
            p = floor_point((x, y))
            # if it is inside the radius, add it to the set
            if point_in_circle(p, center, radius):
                points.add(p)
            x += 1
        y += 1
    return points


def outline_circle(center, radius):
    """Returns a set of points that make an outline of a circle.
    Uses filled_circle as a base for drawing the outline.
    Center and radius are not tested as anything but N.0 or N.5.
    Use other decimals at your own risk, anything could happen.
    STYLE GUIDE:
    If center is N.0, radius should be N.5.
    If center is N.5, radius should be N.0."""
    points = set()
    # get normal filled circle to hollow out
    filled_points = filled_circle(center, radius)
    # create dimensions for bounding rectangle
    top = center[1] - radius
    bottom = center[1] + radius
    left = center[0] - radius
    right = center[0] + radius
    # flags for keeping track of progress
    upper = True  # we start in the top half of the circle
    in_circle = False  # we don't start in the circle
    # begin looping through bounding rectangle
    y = top
    while y <= bottom:
        x = left
        while x <= right:
            p = floor_point((x, y))
            if point_in_circle(p, center, radius):
                if upper:
                    # upper half of circle
                    if not in_circle:
                        # because we are in the circle but the flag hasn't
                        # been set, this is the first point in the row
                        in_circle = True
                        # add point and opposite x value point
                        points.add(p)
                        # double center x & subtract col for opposite col number
                        # cast to int because it can't be a float
                        points.add((int(center[0] * 2 - p[0]), p[1]))
                    elif (p[0], p[1] - 1) not in filled_points:
                        # otherwise, we are in the middle of the circle
                        # add only if top is free, which it is on the edges
                        points.add(p)
                else:
                    # for the lower half of the circle, copy upper half
                    # double center y & subtract row for opposite row number
                    # y value cast to int for safety
                    if (p[0], int(center[1] * 2 - p[1])) in points:
                        points.add(p)
            x += 1
        y += 1
        # when starting a new row, reset in_circle to properly find first point
        in_circle = False
        # know when we switch to lower half
        if int(y) > center[1]:
            upper = False
    return points


def draw_circle(center, radius, width=0):
    """Returns a set of points that make a circle on a grid.
    If width is less than zero, ValueError is raised.
    If width is zero, the default, a filled circle is drawn.
    If width is one, an outline of a filled circle is drawn.
    If width is larger, then two circles are made, one bigger and one smaller.
    The circles are subtracted to get a circle with a thicker outline.
    The center and radius do not have to be integers, but nicer circles are
    drawn when center and radius are either N.0 or N.5.
    WEIRD CIRCLES OCCUR WHEN WIDTH IS NOT AN INTEGER. SEE STYLE GUIDE BELOW.
    If width is one, only do center and radius of N.0 and N.5.
    The outline circle function is untested on anything else.
    STYLE GUIDE:
    If width is 0 or 1 then:
        If center is N.0, radius should be N.5.
        If center is N.5, radius should be N.0.
    Otherwise, it's a bit more complicated:
        If center is N.0 then:
            If width is even, radius should be N.0.
            If width is odd, radius should be N.5.
        If center is N.5 then:
            Everything looks nice."""
    if width < 0:
        # cannot have negative width
        raise ValueError("Width must be 0 or higher.")
    elif width == 0:
        # width of 0 is a filled circle, and the default
        points = filled_circle(center, radius)
    elif width == 1:
        # width of 1 is the outline of a filled circle
        points = outline_circle(center, radius)
    else:
        points = set()
        # calculate extra radius
        r = (width - 1) / 2
        # get bigger and smaller circles
        full_points = filled_circle(center, radius + r)
        empty_points = filled_circle(center, radius - r - 1)
        # subtract smaller circle from bigger circle
        for p in full_points:
            if p not in empty_points:
                points.add(p)
    return points


def circle_pie(center, radius, start_angle, stop_angle, width=0):
    """Returns a set of points that make a filled circle pie.
    Center and radius don't have to be integers, but look best as N.0 or N.5.
    start_angle and stop_angle should be given in degrees, from 0 to 360.
    If start_angle is bigger than stop_angle, nothing will be drawn.
    STYLE GUIDE:
    If center is N.0, radius should be N.5.
    If center is N.5, radius should be N.0."""
    points = set()
    # get standard filled circle
    circle_points = draw_circle(center, radius, width)
    # loop through points
    for p in circle_points:
        # get angle
        angle = math.degrees(angle_between_points(center, p, True))
        # if angle is within limits, add point
        if angle_in_arc(angle, start_angle, stop_angle):
            points.add(p)
        # special case when angle equals zero
        elif angle == 0:
            # always add center point
            if p == floor_point(center):
                points.add(p)
    return points


def filled_ellipse(center, rx, ry):
    """Returns a set of points that make a filled ellipse.
    Center and radii don't have to be integers, but look best as N.0 or N.5.
    STYLE GUIDE:
    If center is N.0, radii should be N.5.
    If center is N.5, radii should be N.0."""
    points = set()
    # create dimensions for bounding rectangle
    top = center[1] - ry
    bottom = center[1] + ry
    left = center[0] - rx
    right = center[0] + rx
    # begin looping through bounding rectangle
    y = top
    while y <= bottom:
        x = left
        while x <= right:
            p = floor_point((x, y))
            # if it is inside the radii, add it to the set
            if point_in_ellipse(p, center, rx, ry):
                points.add(p)
            x += 1
        y += 1
    return points


def outline_ellipse(center, rx, ry):
    """Returns a set of points that make an outline of an ellipse.
    Uses filled_ellipse as a base for drawing the outline.
    Center and radii are not tested as anything but N.0 or N.5.
    Use other decimals at your own risk, anything could happen.
    STYLE GUIDE:
    If center is N.0, radii should be N.5.
    If center is N.5, radii should be N.0."""
    points = set()
    # get normal filled ellipse to hollow out
    filled_points = filled_ellipse(center, rx, ry)
    # create dimensions for bounding rectangle
    top = center[1] - ry
    bottom = center[1] + ry
    left = center[0] - rx
    right = center[0] + rx
    # flags for keeping track of progress
    upper = True  # we start in the top half of the ellipse
    in_ellipse = False  # we don't start in the ellipse
    # begin looping through bounding rectangle
    y = top
    while y <= bottom:
        x = left
        while x <= right:
            p = floor_point((x, y))
            if point_in_ellipse(p, center, rx, ry):
                if upper:
                    # upper half of ellipse
                    if not in_ellipse:
                        # because we are in the ellipse but the flag hasn't
                        # been set, this is the first point in the row
                        in_ellipse = True
                        # add point and opposite x value point
                        points.add(p)
                        # double center x & subtract col for opposite col number
                        # cast to int because it can't be a float
                        points.add((int(center[0] * 2 - p[0]), p[1]))
                    elif (p[0], p[1] - 1) not in filled_points:
                        # otherwise, we are in the middle of the ellipse
                        # add only if top is free, which it is on the edges
                        points.add(p)
                else:
                    # for the lower half of the ellipse, copy upper half
                    # double center y & subtract row for opposite row number
                    # y value cast to int for safety
                    if (p[0], int(center[1] * 2 - p[1])) in points:
                        points.add(p)
            x += 1
        y += 1
        # when starting a new row, reset in_ellipse to properly find first point
        in_ellipse = False
        # know when we switch to lower half
        if int(y) > center[1]:
            upper = False
    return points


def draw_ellipse(center, rx, ry, width=0):
    """Returns a set of points that make an ellipse on a grid.
    If width is less than zero, ValueError is raised.
    If width is zero, the default, a filled ellipse is drawn.
    If width is one, an outline of a filled ellipse is drawn.
    If width is larger, then two ellipses are made, one bigger and one smaller.
    The ellipses are subtracted to get an ellipse with a thicker outline.
    The center and radii do not have to be integers, but nicer ellipses are
    drawn when center and radii are either N.0 or N.5.
    WEIRD ELLIPSES OCCUR WHEN WIDTH IS NOT AN INTEGER. SEE STYLE GUIDE BELOW.
    If width is one, only do center and radii of N.0 and N.5.
    The outline ellipse function is untested on anything else.
    STYLE GUIDE:
    If width is 0 or 1 then:
        If center is N.0, radii should be N.5.
        If center is N.5, radii should be N.0.
    Otherwise, it's a bit more complicated:
        If center is N.0 then:
            If width is even, radii should be N.0.
            If width is odd, radii should be N.5.
        If center is N.5 then:
            Everything looks nice."""
    if width < 0:
        # cannot have negative width
        raise ValueError("Width must be 0 or higher.")
    elif width == 0:
        # width of 0 is a filled ellipse, and the default
        points = filled_ellipse(center, rx, ry)
    elif width == 1:
        # width of 1 is the outline of a filled ellipse
        points = outline_ellipse(center, rx, ry)
    else:
        points = set()
        # calculate extra radii
        r = (width - 1) / 2
        # get bigger and smaller ellipses
        full_points = filled_ellipse(center, rx + r, ry + r)
        empty_points = filled_ellipse(center, rx - r - 1, ry - r - 1)
        # subtract smaller ellipse from bigger ellipse
        for p in full_points:
            if p not in empty_points:
                points.add(p)
    return points


def ellipse_pie(center, rx, ry, start_angle, stop_angle, width=0):
    """Returns a set of points that make a filled ellipse pie.
    Center and radii don't have to be integers, but look best as N.0 or N.5.
    start_angle and stop_angle should be given in degrees, from 0 to 360.
    If start_angle is bigger than stop_angle, nothing will be drawn.
    STYLE GUIDE:
    If center is N.0, radii should be N.5.
    If center is N.5, radii should be N.0."""
    points = set()
    # get standard filled ellipse
    ellipse_points = draw_ellipse(center, rx, ry, width)
    # loop through points
    for p in ellipse_points:
        # get angle
        angle = math.degrees(angle_between_points(center, p, True))
        # if angle is within limits, add point
        if angle_in_arc(angle, start_angle, stop_angle):
            points.add(p)
        # special case when angle equals zero
        elif angle == 0:
            # always add center point
            if p == floor_point(center):
                points.add(p)
    return points


def draw_rect(rect, filled=True):
    """Returns a set of points for a filled or unfilled rectangle.
    The rect argument must be (x, y, w, h)."""
    points = set()
    x, y, w, h = rect
    # loop through each row
    for row in range(h):
        # first and last rows always are fully filled
        if not filled and not (row == 0 or row == h - 1):
            # only add first and last point for unfilled rectangles
            points.add((x, y + row))
            points.add((x + (w - 1), y + row))
        else:
            # add the entire row
            for col in range(w):
                points.add((x + col, y + row))
    return points


def flood_fill(array2d, start_pos, blocked=None, directions=ORTHOGONAL):
    """Flood fills non recursively on given 2D array starting with start_pos.
    Blocked defaults to None, where all cells not equal to start_pos are walls.
    If blocked is specified, only those cells will block the flood.
    Blocked can be an empty list, which will flood the whole array.
    New cells are found by looking in the given directions.
    Directions defaults to orthogonal, but custom movements are possible."""
    points = set()
    # set to hold all locations still needed to check
    stack = {start_pos}
    # set for locations already visited
    visited = set()
    # just syntactic sugar
    old = array2d[start_pos[0]][start_pos[1]]
    # main algorithm loop
    while len(stack) > 0:
        x, y = stack.pop()
        # do not process already visited cells
        if (x, y) in visited:
            continue
        # mark cell as visited
        visited.add((x, y))
        # if the point is out of bounds
        if x < 0 or y < 0 or x > len(array2d) - 1 or y > len(array2d[0]) - 1:
            continue
        # process blocked cells
        if blocked is None:
            # all cells except those equal to the original
            if array2d[x][y] != old:
                continue
        else:
            # all cells specifically blocked
            if array2d[x][y] in blocked:
                continue
        # add flooded point
        points.add((x, y))
        # stack new points according to directions
        for direction in directions:
            stack.add((x + direction[0], y + direction[1]))
    return points
