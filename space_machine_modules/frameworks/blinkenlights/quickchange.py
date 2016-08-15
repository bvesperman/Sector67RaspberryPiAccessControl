import time
import random
from layer import Layer


class QuickChange:
  def __init__(self, handle_pixel=20, trans_time=1.5):
    self.wait_ms = 50
    self.handle_pixel = handle_pixel
    self.trans_time = float(trans_time)
    self.fireworks_points = [] #!temp solution..

  def main(self):
    self.Layer_0 = Layer(None_func = self.set_color_None, curr_func = self.rainbow_cycle, opacity = 1, trans_time = self.trans_time)
    self.Layer_1 = Layer(None_func = self.set_color_None, curr_func = self.set_color_None, opacity = .65, trans_time = self.trans_time)
    j = 0 #iterator for all functions run by main
    while True:
      _data_out = self.stack_layers(j, self.Layer_0, self.Layer_1)
      self.update_strip(_data_out)
      time.sleep(self.wait_ms/1000.0)
      j += 1
      if j >= self.strip.numPixels()*18000:
        j=0

  def update_strip(self, data):
    """Updates the strip then shows the new strip."""
    for i in range(self.strip.numPixels()):
      if not (data or data[i]):
        self.strip.setPixelColor(i, self.Color(0,0,0))
      else:
        self.strip.setPixelColor(i, self.Color(*[int(round(n)) for n in data[i]]))
    self.strip.show()

  def stack_layers(self, j, *layers):
    """Displays multiple functions at once, weighted with the multipliers."""
    _data = self.mix(self.set_color_None(j), layers[0].get_data(j), (1 - layers[0].get_opacity(), layers[0].get_opacity()))
    for i in range(1, len(layers)):
      _data = self.mix(_data, layers[i].get_data(j), (1 - layers[i].get_opacity(), layers[i].get_opacity()))
      #print(1 - layers[i].get_opacity(), layers[i].get_opacity())
    return _data

  def mix(self, data1, data2, multipliers):
    """Displays multiple functions at once, weighted with the multipliers
    (m1, m2). If a color value is (0,0,0) it will mix the other color;
    if it is 'None' it will simply yield the other color.
    Both being 'None' yields 'None'."""
    _data = []
    for i in range(self.strip.numPixels()):
      color = []
      if not data1[i]:
        color = data2[i]
      elif not data2[i]:
        color = data1[i]
      else:
        for v in range(3):
          color.append(multipliers[0]*data1[i][v] + multipliers[1]*data2[i][v])
          if color[-1] > 255:
            color[-1] = 255
      if color: color = tuple(color)
      _data.append(color)
    return _data

  def set_strip(self, strip):
    """Sets the LED strip instance."""
    self.strip = strip

  def Color(self,red, green, blue):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (red << 16) | (green << 8) | blue

  def wheel(self, pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
      return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return (255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return (0, pos * 3, 255 - pos * 3)

#-------------------------------------------------------------------------------
  '''def fade_to_green(self, j):
          """Fades to green."""
          return self.fade_to_color(j, (0,255,0))
      
        def fade_to_red(self, j):
          """Fades to red."""
          return self.fade_to_color(j, (255,0,0),fade_time=self.stuck_open_timeout)'''

  def color_wipe_to_handle_green(self, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe_to_handle(j, (0,255,0))

  def color_wipe_to_handle_white(self, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe_to_handle(j, (255,255,255))

  def theatre_chase_white(self, j):
    """Movie theatre light style chaser animation."""
    return self.theatre_chase(j, (255,255,255))

  def flash_colors_blue_red(self, j):
    """Cycle between two colors"""
    return self.flash_colors(j, (0,0,255), (255,0,0))

  def flash_colors_red_black(self, j):
    """Cycle between two colors"""
    return self.flash_colors(j, (255,0,0), (96,0,0))
 
  def color_wipe_red(self, j):
    """Wipe red across display a pixel at a time."""
    return self.color_wipe(j, (255, 0, 0))

  def color_wipe_green(self, j):
    """Wipe green across display a pixel at a time."""
    return self.color_wipe(j, (0, 255, 0))

  def color_wipe_blue(self, j):
    """Wipe blue across display a pixel at a time."""
    return self.color_wipe(j, (0, 0, 255))

  def set_color_red(self, j):
    """Sets the color of all pixels to red."""
    return self.set_color(j, (255, 0, 0))

  def set_color_green(self, j):
    """Sets the color of all pixels to green."""
    return self.set_color(j, (0,255,0))

  def set_color_black(self, j):
    """Sets the color of all pixels to black."""
    return self.set_color(j, (0,0,0))

  def set_color_None(self, j):
    """Sets the color of all pixels to 'None'."""
    return self.set_color(j, None)
#-------------------------------------------------------------------------------
  def rainbow(self, j):
    """Draw rainbow that fades across all pixels at once."""
    _data = []
    for i in range(self.strip.numPixels()): #initialize pixel data
      _data.append(self.wheel((i+j) & 255))
    return _data

  def rainbow_cycle(self, j):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    _data = []
    for i in range(self.strip.numPixels()): #initialize pixel data
      _data.append(self.wheel((i * 256 / self.strip.numPixels()) + j & 255))
    return _data

  def color_wipe_to_handle(self, j, color, pointing=10):
    """Wipe color across display a pixel at a time."""
    handle = self.handle_pixel
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(None)
    _data[handle - (-j)%pointing] = color
    _data[handle + (-j)%pointing] = color
    return _data

  def flash_colors(self, j, color1, color2):
    """Cycle between two colors"""
    _data = []
    for i in range(self.strip.numPixels()):
      if i%2==0:
        if j%2==0:
          _data.append(color1)
        else:
          _data.append(color2)
      else:
        if j%2==0:
          _data.append(color2)
        else:
          _data.append(color1)
    return _data

  def theatre_chase(self, j, color1, color2=None):
    """Movie theatre light style chaser animation."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(color2)
    for i in range(self.strip.numPixels()-1):
      if i%3==0:
        _data[i+j%3] = color1
    return _data

  def color_wipe(self, j, color):
    """Wipe color across display a pixel at a time."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(None)
    _data[j%self.strip.numPixels()] = color
    return _data

  def set_color(self, j, color):
    """Sets the color of all pixels."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(color)
    return _data

  '''def fireworks(self, j, color):
          _data = []
          for i in range(self.numPixels):
            _data.append(None)
      
          if random.random() >.95 and len(self.fireworks_points)<3:
            size = random.randint(1,10)
            origin = random.randint(0, self.numPixels-1)
            self.fireworks_points.append((size, origin, range(size)))
          for n, (size, origin, a) in enumerate(self.fireworks_points):
            if size < 1:
              self.fireworks_points.remove((size, origin, a))
            else:
              _data[origin] = (215 + (size)*4, 215 + (size)*4, 215 + (size)*4)
      
              for i in range(a[0]):
                if origin - i >= 0:
                  _data[origin - i]= (215 + (size - i)*4, 215 + (size - i)*4, 215 + (size - i)*4)
                if origin + i < len(_data):
                  _data[origin + i]= (215 + (size - i)*4, 215 + (size - i)*4, 215 + (size - i)*4)
              self.fireworks_points[n] = (size - 1 , origin, a[1:])
      
          return _data
      
        def fireworks_white(self, j):
          return self.fireworks(j, (255,255,255))'''
    






































