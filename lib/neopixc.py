import board
from neopixel import NeoPixel
from collections import deque

class NeoPixC(NeoPixel):
  def __init__(self, colors=[]):
    self._num_pixels = 100
    self.colors = deque(colors)

    super().__init__(
      board.D18,
      self._num_pixels,
      brightness=0.2,
      auto_write=False
    )
  
  def set_colors(self, colors):
    self.colors = deque(colors)

  def walk(self):
    curr_pixel = 0
    while curr_pixel < self._num_pixels:
        mod = curr_pixel % len(self.colors)
        self[curr_pixel] = self.colors[mod]
        curr_pixel += 1
    self.show()

  def rotate(self):
    self.colors.rotate()

  def down(self):
    self.fill((0,0,0))
    self.show()
