from colour import Color


def is_light(hex):
    color = Color('#' + hex)
    # see http://stackoverflow.com/a/596243 for info on perceptive luminance
    perceptive_luminance = 0.299 * color.red + \
        0.587 * color.green + 0.114 * color.blue

    return perceptive_luminance > 0.5
