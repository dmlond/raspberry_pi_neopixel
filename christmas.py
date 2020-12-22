# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import signal
import sys

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 100

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, pixel_order=ORDER
)

def signal_handler(sig, frame):
    pixels.fill((0,0,0))
    sys.exit(0)

while True:
    signal.signal(signal.SIGINT, signal_handler)

    curr_pixel = 0
    while curr_pixel < num_pixels:
        mod = curr_pixel % 3
        if mod == 0:
            # green
            pixels[curr_pixel] = (255,0,0)
        elif mod == 1:
            # red
            pixels[curr_pixel] = (0,255,0)
        else:
            # yellow
            pixels[curr_pixel] = (255,255,0)
        curr_pixel += 1
    signal.pause()