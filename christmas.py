import time
import signal
import sys
from pathlib import Path

from lib.neopixc import NeoPixC

state_file = '/home/pi/state'
pixels = NeoPixC()

def signal_handler(sig, frame):
    pixels.down()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

try:
    last_state = Path(state_file).read_text().rstrip()
except FileNotFoundError:
    last_state = None

while True:
    try:
        current_state = Path(state_file).read_text().rstrip()
    except FileNotFoundError:
        # default
        current_state = 'static'

    if current_state != last_state:
        if current_state == 'blink':
            pixels.walk()
            pixels.rotate()
        elif current_state == 'static':
            pixels.walk()
        elif current_state == 'down':
            pixels.down()
        time.sleep(0.5)
