from DerivedBaseClasses.door_lightsBase import *
from frameworks.mockstrip import MockStrip
from frameworks.quickchange  import QuickChange
if sys.platform=='linux2':
  from neopixel import *

class door_lightsStateMachine(door_lightsBase):
  __metaclass__ = ABCMeta
  """description of class"""
  
  

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel, stuck_open_timeout, trans_time):
    self.log = logging.getLogger("BlinkenLights_Door")
    self.out_queue = out_queue
    self.name = name
    self.handle_pixel = int(handle_pixel) # the pixel closest to the handle
    self.led_count=int(led_count) # Number of LED pixels.
    self.led_pin = int(led_pin) # GPIO pin connected to the pixels (must support PWM!).
    self.led_freq_hz = int(led_freq_hz) # LED signal frequency in hertz (usually 800khz)
    self.led_dma = int(led_dma) # DMA channel to use for generating signal (try 5)
    self.led_brightness = int(led_brightness) # Set to 0 for darkest and 255 for brightest
    self.led_invert = led_invert.lower() in ("yes", "true", "t", "1") # True to invert the signal (when using NPN transistor level shift)
    self.stuck_open_timeout = int(stuck_open_timeout)
    self.trans_time = float(trans_time)
    self.gui = False
    self.state = None
    self.prev_state = None
    self.curr_state = None
    # Create NeoPixel object with appropriate configuration.
    if sys.platform=='linux2':
      self.strip = Adafruit_NeoPixel(self.led_count, self.led_pin, self.led_freq_hz, self.led_dma, self.led_invert, self.led_brightness)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    self.strip.begin()
    self.log.debug("start called")
    self.qc = QuickChange(self.handle_pixel, self.trans_time)
    self.qc.set_strip(self.strip)
    self.qc.stuck_open_timeout = self.stuck_open_timeout
    self.thread = threading.Thread(target=self.qc.main)
    self.thread.setDaemon(True)
    self.thread.start()
    self.log.debug("thread started")
    time.sleep(.1) #was having  occasional issue with qc not fully initiated when it tries to call ON_ENTER_CLOSED
    super(door_lightsStateMachine, self).start(self.CLOSED)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)
    frame2 = Frame(root, padx=5, pady=5)
    frame2.pack(fill=X)
    self.wait_ms = 50
    self.strip = MockStrip(self.led_count, frame2)

  def ON_ENTER_CLOSED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_ENTER"})
    self.qc.Layer_0.set_next(self.qc.rainbow_cycle)
    self.qc.Layer_1.clear()

  def ON_ENTER_GRANTING(self):
    """  """
    self.generate_message({"event": self.name + "_GRANTING_ENTER"})
    self.qc.Layer_1.set_next(self.qc.color_wipe_to_handle_white)

  def ON_ENTER_OPENED(self):
    """  """
    self.generate_message({"event": self.name + "_OPENED_ENTER"})
    self.qc.Layer_0.set_next(self.qc.rainbow)
    self.qc.Layer_1.clear()

  def ON_ENTER_REJECTING(self):
    """  """
    self.generate_message({"event": self.name + "_REJECTING_ENTER"})
    self.qc.Layer_1.set_next(self.qc.flash_colors_red_black)

  def ON_ENTER_STUCK(self):
    """  """
    self.generate_message({"event": self.name + "_STUCK_ENTER"})
    self.qc.Layer_0.set_next(self.qc.flash_colors_red_black)
    self.qc.Layer_1.clear()

  def WHILE_CLOSED(self, ev):
    """  """
    if ev['event'] == "OPEN_SWITCH_OPEN_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_OPENED"})
    elif ev['event'] == "VALID_KEY":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_GRANT"})
    elif ev['event'] == "INVALID_KEY":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_REJECT"})

  def WHILE_GRANTING(self, ev):
    """  """
    if ev['event'] == "OPEN_SWITCH_OPEN_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_OPENED"})

  def WHILE_OPENED(self, ev):
    """  """
    if ev['event'] == "OPEN_SWITCH_CLOSED_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_CLOSED"})

  def WHILE_STUCK(self, ev):
    """  """
    if ev['event'] == "OPEN_SWITCH_CLOSED_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_CLOSED"})


def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_door_lights"

  door_lightsTestMachine = door_lightsStateMachine(name=name)
  door_lightsTestMachine.setup(out_queue, name=name)
  door_lightsTestMachine.start()

  # Send some test messages
  
  # Start Testing sample state machine by sending some random messages
  # Current State: UNLOCKED
  # Next State: LOCKED
  # Send Message 10 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})
    
  # Current State: LOCKED
  # Next State: GRANTING
  # Send Message 9 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: GRANTING
  # Next State: LOCKED
  # Send Message 8 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: GRANTING
  # Send Message 7 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: GRANTING
  # Next State: LOCKED
  # Send Message 6 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: GRANTING
  # Send Message 5 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: GRANTING
  # Next State: LOCKED
  # Send Message 4 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: GRANTING
  # Send Message 3 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: GRANTING
  # Next State: LOCKED
  # Send Message 2 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: GRANTING
  # Send Message 1 after 2 seconds.
  time.sleep(2)
  door_lightsTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  

if __name__=='__main__':
  main()
