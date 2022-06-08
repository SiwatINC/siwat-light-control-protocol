def validate_rgb(r: int, g: int, b: int) -> list:
    if(r < 0):
        print(
            "The value %d specified is too low for r, r has been automatically set to 0" % (r))
        r = 0
    if(r > 255):
        print(
            "The value %d specified is too high for r, r has been automatically set to 255" % (r))
        r = 255
    if(g < 0):
        print(
            "The value %d specified is too low for g, g has been automatically set to 0" % (g))
        g = 0
    if(g > 255):
        print(
            "The value %d specified is too high for g, g has been automatically set to 255" % (g))
        g = 255
    if(b < 0):
        print(
            "The value %d specified is too low for b, b has been automatically set to 0" % (b))
        b = 0
    if(b > 255):
        print(
            "The value %d specified is too high for b, b has been automatically set to 255" % (b))
        b = 255

    return [r,g,b]

def index_is_valid(index: int, num_leds: int) -> bool:
    if index >= num_leds or index < 0:
        return False
    return True

def range_is_valid(range_start: int, range_stop: int, num_leds: int) -> bool:
    if(range_start < 0 or range_stop < 0):
        print("index must be greater than 0!")
        return False
    elif(range_start >= num_leds or range_stop >= num_leds):
        print("range %d to %d is invalid (out of bound)" % (range_start,range_stop))
        return False
    if(range_start > range_stop):
        print("segment start (%d) cannot be more than segment stop (%d)" % (range_start,range_stop))
        return False
    return True

class LEDOutOfBoundError(Exception):
    """The Specified LED Number is too large"""
    pass