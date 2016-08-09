from blinkenlightsBase import *
from MockStrip import MockStrip
from blinkenlights_quickchange  import QuickChange




class BlinkenLights(blinkenlightsBase):

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel, stuck_open_timeout, trans_time):
    self.log = logging.getLogger("BlinkenLights")
    self.out_queue = out_queue
    self.name = name
    # the pixel closest to the handle
    self.handle_pixel = int(handle_pixel)
    self.led_count=int(led_count)       # Number of LED pixels.
    self.led_pin = int(led_pin)         # GPIO pin connected to the pixels (must support PWM!).
    self.led_freq_hz = int(led_freq_hz) # LED signal frequency in hertz (usually 800khz)
    self.led_dma = int(led_dma)         # DMA channel to use for generating signal (try 5)
    self.led_brightness = int(led_brightness) # Set to 0 for darkest and 255 for brightest
    self.led_invert = led_invert.lower() in ("yes", "true", "t", "1")  # True to invert the signal (when using NPN transistor level shift)
    self.stuck_open_timeout = int(stuck_open_timeout)
    self.trans_time = float(trans_time)
    self.gui = False
    self.state = None
    self.prev_state = None
    self.curr_state = None
    # Create NeoPixel object with appropriate configuration.
    if sys.platform=='linux2':
      self.strip = Adafruit_NeoPixel(self.led_count, self.led_pin, self.led_freq_hz, self.led_dma, self.led_invert, self.led_brightness)
    #self.strip = Adafruit_NeoPixel(self.led_count, 18, 800000, 5, False, 255)

  def config_gui(self, root):
    # Set up the GUI part
    self.gui = True
    frame = LabelFrame(root, text="STATE", padx=5, pady=5)
    frame.pack(fill=X)
    self.gui_state = StringVar()
    self.gui_state.set("[STATE]")
    label = Label(frame, textvariable = self.gui_state, justify=LEFT)
    label.pack(side=LEFT)
    self.info_frame = frame
    frame2 = LabelFrame(root, text=self.name, padx=5, pady=5, bg='black')
    frame2.pack(fill=X)
    self.wait_ms = 50
    self.strip = MockStrip(self.led_count, frame2)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # Intialize the library (must be called once before other functions).
    self.strip.begin()
    self.log.debug("start called")
    self.qc = QuickChange(self.handle_pixel, self.trans_time)
    self.qc.set_strip(self.strip)
    self.qc.stuck_open_timeout = self.stuck_open_timeout
    self.thread = threading.Thread(target=self.qc.main)
    self.thread.setDaemon(True)
    self.thread.start()
    self.log.debug("thread started")
    super(BlinkenLights, self).start(self.MAIN_DOOR_CLOSED)



  # By Default - do nothing ON_MAIN_DOOR_CLOSED
  def ON_MAIN_DOOR_CLOSED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow_cycle)
    self.qc.Layer_1.set_opacity(.3)
    self.qc.Layer_1.set_next(self.qc.fireworks_white)

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_CLOSED_MAIN_DOOR_UNLOCKING(self):
    """ While in MAIN_DOOR_CLOSED, a MAIN_DOOR_UNLOCKING message is recieved. """
    self.qc.Layer_1.reset_opacity()
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_CLOSED_MAIN_DOOR_OPENED(self):
    """ While in MAIN_DOOR_CLOSED, a MAIN_DOOR_OPENED message is recieved. """
    self.qc.Layer_1.reset_opacity()
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_CLOSED_INVALID_KEY(self):
    """ While in MAIN_DOOR_CLOSED, a INVALID_KEY message is recieved. """
    self.qc.Layer_1.reset_opacity()
      
  
  # By Default - do nothing ON_MAIN_DOOR_UNLOCKING
  def ON_MAIN_DOOR_UNLOCKING(self):
    self.qc.Layer_1.set_next(self.qc.color_wipe_to_handle_white)

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_UNLOCKING_MAIN_DOOR_CLOSED(self):
    """ While in MAIN_DOOR_UNLOCKING, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_UNLOCKING_MAIN_DOOR_OPENED(self):
    """ While in MAIN_DOOR_UNLOCKING, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_INVALID_KEY
  def ON_INVALID_KEY(self):
    self.qc.Layer_1.set_next(self.qc.flash_colors_red_black)

   
  # By default - do nothing during transitions
  def ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT(self):
    """ While in INVALID_KEY, a MAIN_DOOR_INVALID_TIMEOUT message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_STUCK_OPEN
  def ON_MAIN_DOOR_STUCK_OPEN(self):
    self.qc.Layer_0.set_next(self.qc.flash_colors_red_black)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_STUCK_OPEN_MAIN_DOOR_CLOSED(self):
    """ While in MAIN_DOOR_STUCK_OPEN, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_OPENED
  def ON_MAIN_DOOR_OPENED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_OPENED_MAIN_DOOR_CLOSED(self):
    """ While in MAIN_DOOR_OPENED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_OPENED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in MAIN_DOOR_OPENED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_FORCED_OPEN
  def ON_MAIN_DOOR_FORCED_OPEN(self):
    self.qc.Layer_0.set_next(self.qc.flash_colors_blue_red)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_FORCED_OPEN_MAIN_DOOR_UNLOCKING(self):
    """ While in MAIN_DOOR_FORCED_OPEN, a MAIN_DOOR_UNLOCKING message is recieved. """
    pass