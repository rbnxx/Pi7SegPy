import PiShiftPy as shift
import time

available_chars = {
  0: 0b11000000,
  1: 0b11111001,
  2: 0b10100100,
  3: 0b10110000,
  4: 0b10011001,
  5: 0b10010010,
  6: 0b10000011,
  7: 0b11111000,
  8: 0b10000000,
  9: 0b10011000,
  '0': 0b11000000,
  '1': 0b11111001,
  '2': 0b10100100,
  '3': 0b10110000,
  '4': 0b10011001,
  '5': 0b10010010,
  '6': 0b10000011,
  '7': 0b11111000,
  '8': 0b10000000,
  '9': 0b10011000,
  'A': 0b10001000,
  'b': 0b10000011,
  'C': 0b11000110,
  'c': 0b10100111,
  'd': 0b10100001,
  'E': 0b10000110,
  'F': 0b10001110,
  'H': 0b10001001,
  'h': 0b10001011,
  'L': 0b11000111,
  'n': 0b10101011,
  'I': 0b11111001,
  'O': 0b11000000,
  'o': 0b10100011,
  'P': 0b10001100,
  'S': 0b10010010,
  'U': 0b11000001,
  'u': 0b11100011,
  '-': 0b10111111,
  "'": 0b11011111,
  '_': 0b11110111,
  ' ': 0b11111111,
}

data = 18
clock = 23
latch = 24
chain = 2
displays = 1
common_cathode = False


def init(data_pin=18, clock_pin=23, latch_pin=24, registers=1, no_of_displays=1, common_cathode_type=False):
    global data, clock, latch, chain, common_cathode, displays
    data = data_pin
    clock = clock_pin
    latch = latch_pin
    chain = registers
    common_cathode = common_cathode_type
    displays = no_of_displays
    setup()


def setup():
    if common_cathode:
        for key in available_chars:
            available_chars[key] = ~available_chars[key]
    shift.init(data, clock, latch, chain)


def with_dot(value):
    if common_cathode:
        return value | 1 << 7
    else:
        return value & ~(1 << 7)


def show(values, dots=[]):
    length = len(values)
    if length > displays:
        raise ValueError("More Characters than available on displays")
    else:
        for i in range(length-1, -1, -1):
            try:
                char = available_chars[values[i]]
                if i+1 in dots:
                    char = with_dot(char)
                if common_cathode:
                    shift.write( (char << 8) | ((~(1 << displays-length+i)) & 0xff))
                else:
                    shift.write(char << 8 | 1 << i)
                time.sleep(0.003)
            except KeyError:
                raise ValueError("The character cannot be printed on a 7 segment display")
