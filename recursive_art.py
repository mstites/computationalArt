"""
2/13/2019

@author: Griffith Stites
"""

import random
from PIL import Image

def get_function(start = 1, end = 6):
    """Get a random function.

    Uses a dictionary as a switch to chose a random function to return.

    >>> get_function(1, 1)
    'prod'
    >>> get_function(2, 2)
    'avg'
    >>> get_function(3, 3)
    'cos_pi'
    >>> get_function(4, 4)
    'sin_pi'
    >>> get_function(5, 5)
    'x'
    >>> get_function(6, 6)
    'y'
    """
    # NEED TO ADD TWO MORE BUILDING BLOCKS THAT ARE BETWEEN [-1, 1] OUTPUT WITH [-1, 1] INPUT
    return {
        1:'prod',
        2:'avg',
        3:'cos_pi',
        4:'sin_pi',
        5:'x',
        6:'y',
    }[random.randint(start, end)] # choses a random case from start to end

def build_random_function(min_depth, max_depth):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of
        these functions)

    >>> build_random_function(1, 3)
    #>>> build_random_function(3, 3)
    >>> build_random_function(7, 9)
    """
    list = []
    depth = random.randint(min_depth, max_depth) # randomize the length between the beginning and end
    print(depth)
    if(depth == 1): # have reached the end and must stop
        list.append(get_function(5, 6)) # get either x or y
        return list
    elif(depth == 2):
        list.append(get_function(3, 4)) # get either sin or cos
        list.append(build_random_function(depth - 1, depth - 1))
    elif(depth >= 3): # must add three depth or larger
        list.append(get_function(1, 4)) # get prod, avg, cos, or sin
        if(list[0] == "prod"):
            list.append(build_random_function(2, depth))
            list.append(build_random_function(2, depth))
        elif(list[0] == "avg"):
            list.append(build_random_function(2, depth))
            list.append(build_random_function(2, depth))
        else: # if sin or cos
            list.append(build_random_function(1, depth - 1))
    # else:
    #     list.append(build_random_function(depth - 1, depth - 1))
    # list.append(build_random_function(depth - 1, depth - 1))
    return list

def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.

    The representation of the function f is defined in the assignment write-up.

    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function

    Returns:
        The function value

    Examples:
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    >>> evaluate_random_function()
    """
    if (f[0] == "x"):
        return x
    else:
        return y

    # prod(a, b) = ab
    # avg(a, b) = 0.5*(a + b)
    # cos_pi(a) = cos(pi * a)
    # sin_pi(a) = sin(pi * a)
    # x(a, b) = a
    # y(a, b) = b


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10) # 0.5 is half way between 0 and 1, 5 is half way between 0 and 10
        5.0
        >>> remap_interval(5, 4, 6, 0, 2) # 5 is half way in between 4 and 6, 1.0 is between 0 and 2
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # step_ratio = step from the start of the input interval to val divided by the size of the interval
    step_ratio = (val-input_interval_start)/float(input_interval_end - input_interval_start)

    # the step ratio multiplied by the output interval, then added to the start value for output
    return (step_ratio * (output_interval_end-output_interval_start)) + output_interval_start


def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """Generate a test image with random pixels and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size): # loops over all the x dimensions (rows)
        for j in range(y_size): # loops over all the y pixels (columns) in that row
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(get_function, globals())
    doctest.run_docstring_examples(build_random_function, globals(), verbose = True)
    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    # generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
