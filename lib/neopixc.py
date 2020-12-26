import board
from neopixel import NeoPixel
from collections import deque

class NeoPixC(NeoPixel):
  def __init__(self):
    self.num_pixels = 100
    self.pin = board.D18
    self.color_mod = deque([
      self.green,
      self.red,
      self.yellow
    ])

    super().__init__(
      self.pin,
      self.num_pixels,
      brightness=0.2,
      auto_write=False
    )
  
  def green(self,pixel):
    self[pixel] = (255,0,0)

  def red(self,pixel):
    self[pixel] = (0,255,0)

  def yellow(self,pixel):
    self[pixel] = (255,255,0)

  def walk(self):
    curr_pixel = 0
    while curr_pixel < self.num_pixels:
        mod = curr_pixel % 3
        self.color_mod[mod](curr_pixel)
        curr_pixel += 1
    self.show()

  def rotate(self):
    self.color_mod.rotate()

  def down(self):
    self.fill((0,0,0))
    self.show()
