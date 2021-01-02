import time
import signal
import sys
from pathlib import Path
import json
from lib.neopixc import NeoPixC

try:
  color_file = sys.argv[1]
except IndexError:
  print(f"usage: {sys.argv[0]} color_json_file")
  exit(1)

try:
  colorsF = open(color_file, 'r')
except FileNotFoundError:
    print(f"{color_file} not found")
    exit(1)

colors = json.load(colorsF)
colorsF.close()

state_file = '/home/pi/state'
pixels = NeoPixC(colors)

def signal_handler(sig, frame):
    pixels.down()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

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
