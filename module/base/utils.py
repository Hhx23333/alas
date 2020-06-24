import numpy as np
from PIL import ImageStat


def random_normal_distribution_int(a, b, n=5):
    """Generate a normal distribution int within the interval. Use the average value of several random numbers to
    simulate normal distribution.

    Args:
        a (int): The minimum of the interval.
        b (int): The maximum of the interval.
        n (int): The amount of numbers in simulation. Default to 5.

    Returns:
        int
    """
    if a < b:
        output = np.mean(np.random.randint(a, b, size=n))
        return int(output.round())
    else:
        return b


def ensure_time(second, n=5, precision=3):
    """Ensure to be time.

    Args:
        second (int, float, tuple): time.
        n (int): The amount of numbers in simulation. Default to 5.
        precision (int): Decimals.

    Returns:

    """
    if isinstance(second, tuple):
        multiply = 10 ** precision
        return random_normal_distribution_int(second[0] * multiply, second[1] * multiply, n) / multiply
    else:
        return second


def random_rectangle_point(area):
    """Choose a random point in an area.

    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).

    Returns:
        int: x
        int: y
    """
    x = random_normal_distribution_int(area[0], area[2])
    y = random_normal_distribution_int(area[1], area[3])
    return x, y


def random_rectangle_vector(vector, box, random_range=(0, 0, 0, 0), padding=15):
    """Place a vector in a box randomly.

    Args:
        vector: (x, y)
        box: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        random_range (tuple): Add a random_range to vector. (x_min, y_min, x_max, y_max).
        padding (int):

    Returns:
        tuple(int), tuple(int): start_point, end_point.
    """
    vector = np.array(vector) + random_rectangle_point(random_range)
    vector = np.round(vector).astype(np.int)
    half_vector = np.round(vector / 2).astype(np.int)
    box = np.array(box) + np.append(np.abs(half_vector) + padding, -np.abs(half_vector) - padding)
    center = random_rectangle_point(box)
    start_point = center - half_vector
    end_point = start_point + vector
    return tuple(start_point), tuple(end_point)


def random_line_segments(p1, p2, n, random_range=(0, 0, 0, 0)):
    """Cut a line into multiple segments.

    Args:
        p1: (x, y).
        p2: (x, y).
        n: Number of slice.
        random_range: Add a random_range to points.

    Returns:
        list[tuple]: [(x0, y0), (x1, y1), (x2, y2)]
    """
    return [tuple((((n - index) * p1 + index * p2) / n).astype(int) + random_rectangle_point(random_range))
            for index in range(0, n + 1)]


def area_offset(area, offset):
    """

    Args:
        area(tuple): (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        offset(tuple): (x, y).

    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
    """
    return tuple(np.array(area) + np.append(offset, offset))


def area_pad(area, pad=10):
    """

    Args:
        area(tuple): (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        pad(int):

    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
    """
    return tuple(np.array(area) + np.array([pad, pad, -pad, -pad]))


def point_in_area(point, area, threshold=5):
    """

    Args:
        point: (x, y).
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        threshold: int

    Returns:
        bool
    """
    return area[0] - threshold < point[0] < area[2] + threshold and area[1] - threshold < point[1] < area[3] + threshold


def area_in_area(area1, area2, threshold=5):
    """

    Args:
        area1: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        area2: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        threshold: int

    Returns:
        bool
    """
    return area2[0] - threshold <= area1[0] \
           and area2[1] - threshold <= area1[1] \
           and area1[2] <= area2[2] + threshold \
           and area1[3] <= area2[3] + threshold


def area_cross_area(area1, area2, threshold=5):
    """

    Args:
        area1: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        area2: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        threshold: int

    Returns:
        bool
    """
    return point_in_area((area1[0], area1[1]), area2, threshold=threshold) \
           or point_in_area((area1[2], area1[1]), area2, threshold=threshold) \
           or point_in_area((area1[0], area1[3]), area2, threshold=threshold) \
           or point_in_area((area1[2], area1[3]), area2, threshold=threshold)


def node2location(node):
    """
    Args:
        node(str): Example: 'E3'

    Returns:
        tuple: Example: (6, 4)
    """
    return ord(node[0]) % 32 - 1, int(node[1:]) - 1


def location2node(location):
    """
    Args:
        location(tuple): Example: (6, 4)

    Returns:
        str: Example: 'E3'
    """
    return chr(location[0] + 64 + 1) + str(location[1] + 1)


def get_color(image, area):
    """Calculate the average color of a particular area of the image.

    Args:
        image (PIL.Image.Image): Screenshot.
        area (tuple): (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)

    Returns:
        tuple: (r, g, b)
    """
    temp = image.crop(area)
    stat = ImageStat.Stat(temp)
    return np.array(stat.mean)


def color_similarity(color1, color2):
    """
    Args:
        color1 (tuple): (r, g, b)
        color2 (tuple): (r, g, b)

    Returns:
        int:
    """
    diff = np.array(color1) - np.array(color2)
    positive, negative = diff, np.abs(diff)
    positive[diff < 0] = 0
    negative[diff > 0] = 0
    diff = np.max(positive) + np.max(negative)
    return diff


def color_similar(color1, color2, threshold=10):
    """Consider two colors are similar, if tolerance lesser or equal threshold.
    Tolerance = Max(Positive(difference_rgb)) + Max(- Negative(difference_rgb))
    The same as the tolerance in Photoshop.

    Args:
        color1 (tuple): (r, g, b)
        color2 (tuple): (r, g, b)
        threshold (int): Default to 10.

    Returns:
        bool: True if two colors are similar.
    """
    # print(color1, color2)
    diff = np.array(color1) - np.array(color2)
    positive, negative = diff, np.abs(diff)
    positive[diff < 0] = 0
    negative[diff > 0] = 0
    diff = np.max(positive) + np.max(negative)
    return diff <= threshold


def color_similar_1d(bar, color, threshold=10):
    """
    Args:
        bar: 1D array.
        color: (r, g, b)
        threshold(int): Default to 10.

    Returns:
        np.ndarray: bool
    """
    diff = np.array(bar) - np.array(color)
    positive, negative = diff, np.abs(diff)
    positive[diff < 0] = 0
    negative[diff > 0] = 0
    diff = np.max(positive, axis=1) + np.max(negative, axis=1)
    return diff <= threshold


def color_similarity_2d(image, color):
    """
    Args:
        image: 2D array.
        color: (r, g, b)

    Returns:
        np.ndarray: uint8
    """
    diff = np.array(image) - color
    positive, negative = diff, np.abs(diff)
    positive[diff < 0] = 0
    negative[diff > 0] = 0
    diff = 255.0 - np.max(positive, axis=2) - np.max(negative, axis=2)
    diff[diff < 0] = 0
    image = diff.astype(np.uint8)
    return image


def extract_letters(image, letter=(255, 255, 255), back=(0, 0, 0)):
    """Set letter color to black, set background color to white.

    Args:
        image: Shape (height, width, channel)
        letter (tuple): Letter RGB.
        back (tuple): Background RGB.

    Returns:
        np.ndarray: Shape (height, width)
    """
    image = color_similarity_2d(np.array(image), color=letter)
    back = color_similarity(back, letter)
    image = (255.0 - image) * (1 + back / 255)
    image[image > 255] = 255
    return image


def red_overlay_transparency(color1, color2, red=247):
    """Calculate the transparency of red overlay.

    Args:
        color1: origin color.
        color2: changed color.
        red(int): red color 0-255. Default to 247.

    Returns:
        float: 0-1
    """
    return (color2[0] - color1[0]) / (red - color1[0])


def color_bar_percentage(image, area, prev_color, reverse=False, starter=0, threshold=30):
    """
    Args:
        image:
        area:
        prev_color:
        reverse: True if bar goes from right to left.
        starter:
        threshold:

    Returns:
        float: 0 to 1.
    """
    image = np.array(image.crop(area))
    image = image[:, ::-1, :] if reverse else image
    length = image.shape[1]
    prev_index = starter

    for _ in range(1280):
        bar = color_similarity_2d(image, color=prev_color)
        index = np.where(np.any(bar > 255 - threshold, axis=0))[0]
        if not index.size:
            return prev_index / length
        else:
            index = index[-1]
        if index <= prev_index:
            return index / length
        prev_index = index

        prev_row = bar[:, prev_index] > 255 - threshold
        if not prev_row.size:
            return prev_index / length
        prev_color = np.mean(image[:, prev_index], axis=0)

    return 0.
