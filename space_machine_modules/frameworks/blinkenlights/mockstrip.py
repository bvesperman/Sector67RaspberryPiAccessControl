from Tkinter import *


class MockStrip:
  def __init__(self, led_count, frame):
    self.led_count = led_count
    self.pending = []
    self.labels = []

    for i in range(led_count):
      self.pending.append("#000000")

    for i in range(led_count):
      lbl = Label(frame, text=str(i), width = 2)
      self.labels.append(lbl)
      lbl.pack(side=LEFT, expand = True, fill = X)
      lbl.configure(bg="#000000")

    self.show() 

  def show(self):
    i=0
    for label in self.labels:
      #print "i is " + str(i)
      #print "color is " + self.pending[i]
      label.configure(bg=self.pending[i])
      i=i+1

  def begin(self):# mimicing neopixel;
    pass

  def setPixelColor(self, pixel, color):
    self.pending[pixel]=self.tk_color(color)

  def getPixelColor(self, pixel):
    return self.pending[pixel]

  def getPixelColorRGB(self, pixel):
    n = self.pending[pixel][1:]
    n = int(n, base=16)
    c = lambda: None
    setattr(c, 'r', n >> 16 & 0xff)
    setattr(c, 'g', n >> 8  & 0xff) 
    setattr(c, 'b', n & 0xff)
    return c

  def tk_color(self,color):
    red=(color & 0xff0000) >> 16
    green=(color & 0x00ff00) >> 8
    blue=(color & 0x0000ff)
    newcolor='#%02X%02X%02X' % (red,green,blue)
    return newcolor

  def numPixels(self):
    return self.led_count
