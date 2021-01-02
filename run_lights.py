import time
import signal
import sys
from pathlib import Path
import json
from lib.neopixc import NeoPixC

def get_colors():
    color_file = '/home/pi/colors'
    try:
        colorsF = open(color_file, 'r')
    except FileNotFoundError:
        raise Exception(f"{color_file} not found")

    colors = json.load(colorsF)
    colorsF.close()
    return colors

def get_state():
    state_file = '/home/pi/state'
    try:
        current_state = Path(state_file).read_text().rstrip()
    except FileNotFoundError:
        # default
        current_state = 'static'
    return current_state

def signal_handler(sig, frame):
    pixels.down()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

pixels = NeoPixC()
last_state = None
last_colors = None
while True:
    current_colors = get_colors()
    if current_colors != last_colors:
        pixels.set_colors(current_colors)
        last_colors = current_colors

    current_state = get_state()
    if current_state != last_state:
        if current_state == 'blink':
            pixels.walk()
            pixels.rotate()
        elif current_state == 'static':
            pixels.walk()
        elif current_state == 'down':
            pixels.down()
    time.sleep(0.5)
