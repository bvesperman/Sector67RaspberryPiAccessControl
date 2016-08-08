import time


class Layer:
  """Manages a layer of the lights."""
  def __init__(self, None_func, curr_func, opacity, trans_time):
    self.trans_time = float(trans_time)
    self.opacity = opacity
    self.time_0 = None
    self.curr_func = curr_func
    self.set_next(self.curr_func)
    self.None_func = None_func
    self.func_opacities = (1,1)

  def get_data(self, j):
    """Returns the data of the layer at iteration j."""
    if (self.curr_func or self.next_func):
      if self.curr_func == self.next_func:
        _data_out = self.curr_func(j)
      else:
        _data_out = self.mix(self.curr_func(j), self.next_func(j), self.fade_weights(self.trans_time))
        if not self.time_0:
          self.curr_func = self.next_func
      return _data_out

  def fade_weights(self, duration): #! if there are multiple fades active/ this is called when another fade is in progress, it will use its time. self.time_0 conflict
    """Returns a tuple of two multipliers; used to weight color values."""
    if not self.time_0: #if fade not active
      self.time_0 = time.time()
    self.duration = time.time() - self.time_0
    if self.duration >= duration: #if fade complete
      self.time_0 = None
      temp = (0,1)
      self.func_opacities = temp
      return temp
    else:
      temp = (1. - self.duration/duration, self.duration/duration)
      self.func_opacities = temp
      return temp

  def mix(self, data1, data2, multipliers=(.50,.50)):
    """Displays multiple functions at once, weighted with the multipliers (m1, m2).
    If a color value is (0,0,0) it will mix the other color; if it is 'None' it will simply yield the other color.
    Both being 'None' yields 'None'."""
    _data = []
    for i in range(len(data1)): #! if data1 and data2 are not the same length, this could be problematic (they should always be the same though).
      color = []
      if not (data1[i] or data2[i]):
        color = None
      else:
        if not data1[i]: data1[i] = (0,0,0)
        if not data2[i]: data2[i] = (0,0,0)
        for v in range(3):
          color.append(multipliers[0]*data1[i][v] + multipliers[1]*data2[i][v])
          if color[-1] > 255:
            color[-1] = 255
      if color: color = tuple(color)
      _data.append(color)
    return _data

  def set_next(self, next_func):
    """Sets the next function to be displayed."""
    self.next_func = next_func

  def get_next(self):
    """Returns the next function of the layer."""
    return self.next_func

  def set_opacity(self, opacity):
    """Sets the opacity of the layer, where 0 is clear and 1 is opaque."""
    self.opacity = opacity

  def get_opacity(self):
    """Returns the current opacity of the layer."""
    if self.curr_func == self.next_func == self.None_func:
      curr = 0
    elif self.curr_func == self.next_func:
      curr = 1
    elif self.curr_func == self.None_func:
      curr = self.func_opacities[1]
    else:
      curr = self.func_opacities[0]
    return curr*self.opacity

  def clear(self):
    """Resets the layer to the 'None' function. (filled with 'None')"""
    self.next_func = self.None_func