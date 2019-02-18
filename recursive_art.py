"""
2/13/2019

@author: Griffith Stites
"""

import random
import math
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
    >>> get_function(7, 7)
    'x2'
    >>> get_function(8, 8)
    'y2'
    """
    return {
        1:'prod',
        2:'avg',
        3:'cos_pi',
        4:'sin_pi',
        5:'x',
        6:'y',
        7:'x2',
        8:'y2',
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
    >>> build_random_function(3, 3)
    >>> build_random_function(7, 9)
    """
    list = []

    # Implemented this if statement to try to speed up run times instead of randomizing each time
    if(min_depth != max_depth): # if min_depth and max_depth are not the same
        depth = random.randint(min_depth, max_depth) # randomize the length between the beginning and end
    else: # otherwise, depth is the min_depth (which is the same as the max_depth)
        depth = min_depth

    if(depth == 1): # have reached the end and must stop
        list.append(get_function(5, 8)) # get either x, x2, y, or y2
        return list
    elif(depth == 2):
        list.append(get_function(3, 4)) # get either sin or cos
        list.append(build_random_function(depth - 1, depth - 1)) # go get x or y
    elif(depth >= 3): # must add three depth or larger
        list.append(get_function(1, 4)) # get prod, avg, cos, or sin
        if(list[0] == "prod"):
            depth_n = random.randint(1, depth - 1) # create a new depth to represent the amount after the function that we have to create
            # either val1 or val2 must be depth-1, such that prod[val1],[val2] is depth long. The other can be any length
            list.append(build_random_function(1, depth - 1)) # the first value is a random length
            list.append(build_random_function(depth - 1, depth - 1)) # the second half is the remaining interval needed
        elif(list[0] == "avg"):
            # either val1 or val2 must be depth-1, such that avg[val1],[val2] is depth long. The other can be any length
            list.append(build_random_function(1, depth - 1)) # the first value is a random length up to the interval length
            list.append(build_random_function(depth - 1, depth - 1)) # the second half is the remaining interval needed
        else: # if sin or cos
            # must be depth-1 long
            list.append(build_random_function(depth - 1, depth - 1))
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
        >>> evaluate_random_function(['sin_pi', ['y']], 0.5, 0.75)
        0.7071067811865476
        >>> evaluate_random_function(['cos_pi', ['cos_pi', ['y']]], 0.75, 0.6)
        0.5646348864175506
        >>> evaluate_random_function(['sin_pi', ['cos_pi', ['y']]], 0.75, 0.6)
        -0.8253408053890464
        >>> evaluate_random_function(["prod", ["x"], ["y"]], 0.1, 0.2)
        0.020000000000000004
        >>> evaluate_random_function(["avg", ["x"], ["y"]], 1, -.5)
        0.25
        >>> evaluate_random_function(["prod", ["sin_pi", ["x"]], ["cos_pi", ["y"]]], 0.4, 0.8)
        -0.7694208842938133
        >>> evaluate_random_function(['prod', ['sin_pi', ['y2']], ['sin_pi', ['y']]], -1, -0.9942857142857143)
        >>> evaluate_random_function(['sin_pi', ['y']], -1, -0.9942857142857143)

        CREATE sOME MORE COMPLEX DOCTESTS WITH NESTED AVG AND PROD

    """
    print(f)
    test = f[0] # testing the first value in the function
    if (test == "x"): # if the value is x, etc etc
        return x
    elif (test == "y"):
        return y
    elif (test == "x2"):
        return x**2
    elif (test == "y2"):
        return y**2
    elif (test == "sin_pi"): # if the value is sin_pi
        return math.sin(math.pi*evaluate_random_function(f.pop(1), x, y)) # find sin(pi*the value within the function). f.pop(1) gives the function the part within sin
    elif (test == "cos_pi"):
        return math.cos(math.pi*evaluate_random_function(f.pop(1), x, y)) # same as sin but for cos
    elif (test == "prod"):
        return evaluate_random_function(f.pop(1), x, y) * evaluate_random_function(f.pop(1), x, y) # the second one is f.pop(1) as well because now the second value is the first value as the first value was kicked out
    elif (test == "avg"):
        return (evaluate_random_function(f.pop(1), x, y) + evaluate_random_function(f.pop(1), x, y))/2
    else: # ????
        return evaluate_random_function(f.pop(1), x, y)

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].
)
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
        127)
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
    # red_function = build_random_function(7, 9)
    # green_function = build_random_function(7, 9)
    # blue_function = build_random_function(7, 9)
    red_function = ['sin_pi', ['avg', ['avg', ['sin_pi', ['x2']], ['sin_pi', ['x2']]], ['avg', ['y2'], ['sin_pi', ['sin_pi', ['sin_pi', ['y2']]]]]]]
    green_function = ['prod', ['y'], ['prod', ['x2'], ['sin_pi', ['sin_pi', ['avg', ['prod', ['x'], ['sin_pi', ['y2']]], ['prod', ['y'], ['sin_pi', ['y2']]]]]]]]
    blue_function = ['prod', ['sin_pi', ['sin_pi', ['avg', ['sin_pi', ['x2']], ['sin_pi', ['sin_pi', ['y2']]]]]], ['sin_pi', ['prod', ['sin_pi', ['avg', ['prod', ['sin_pi', ['x2']], ['sin_pi', ['y']]], ['avg', ['x'], ['sin_pi', ['x']]]]], ['prod', ['sin_pi', ['sin_pi', ['y']]], ['sin_pi', ['sin_pi', ['sin_pi', ['y']]]]]]]]
    print("red_function = ", red_function)
    print("green_function = ", green_function)
    print("blue_function = ", blue_function)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size): # loops over all the x dimensions (rows)
        for j in range(y_size): # loops over all the y pixels (columns) in that row
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            print("x = ", x, "y = ", y)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
                # color_map(evaluate_random_function(['cos_pi', ['avg', ['avg', ['sin_pi', ['x2']], ['sin_pi', ['x2']]], ['avg', ['y2'], ['cos_pi', ['sin_pi', ['cos_pi', ['y2']]]]]]], x, y)),
                # color_map(evaluate_random_function(['prod', ['y'], ['prod', ['x2'], ['cos_pi', ['cos_pi', ['avg', ['prod', ['x'], ['sin_pi', ['y2']]], ['prod', ['y'], ['cos_pi', ['y2']]]]]]]], x, y)),
                # color_map(evaluate_random_function(['prod', ['cos_pi', ['sin_pi', ['avg', ['sin_pi', ['x2']], ['cos_pi', ['cos_pi', ['y2']]]]]], ['cos_pi', ['prod', ['sin_pi', ['avg', ['prod', ['cos_pi', ['x2']], ['sin_pi', ['y']]], ['avg', ['x'], ['sin_pi', ['x']]]]], ['prod', ['sin_pi', ['cos_pi', ['y']]], ['sin_pi', ['sin_pi', ['sin_pi', ['y']]]]]]]], x, y))
                # color_map(evaluate_random_function(['y'], x, y)),
                # color_map(evaluate_random_function(['sin_pi', ['y']], x, y)),
                # color_map(evaluate_random_function(['prod', ['sin_pi', ['y2']], ['sin_pi', ['y']]], x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(evaluate_random_function, globals(), verbose = True)
    # doctest.run_docstring_examples(build_random_function, globals(), verbose = True)
    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
