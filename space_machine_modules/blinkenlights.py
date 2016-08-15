from DerivedBaseClasses.doorBase import *
from _mockstrip import MockStrip
from _blinkenlights_quickchange  import QuickChange
if sys.platform=='linux2':
  from neopixel import *

class BlinkenLights(doorBase):
  __metaclass__ = ABCMeta
  """description of class"""
  
  

    
def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel, stuck_open_timeout, trans_time):
    self.log = logging.getLogger("BlinkenLights_Door")
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

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # assume a starting state of CLOSED_LOCKED and appropriate messages will send it to the correct state
    self.strip.begin()
    self.log.debug("start called")
    self.qc = QuickChange(self.handle_pixel, self.trans_time)
    self.qc.set_strip(self.strip)
    self.qc.stuck_open_timeout = self.stuck_open_timeout
    self.thread = threading.Thread(target=self.qc.main)
    self.thread.setDaemon(True)
    self.thread.start()
    self.log.debug("thread started")
    super(BlinkenLights, self).start(self.CLOSED_LOCKED)

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

      
  # By Default - do nothing ON_DOOR_CLOSED_LOCKED
  def ON_DOOR_CLOSED_LOCKED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow_cycle)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_INVALID_KEY(self):
    """ While in DOOR_CLOSED_LOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_CLOSED_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_VALID_KEY(self):
    """ While in DOOR_CLOSED_LOCKED, a VALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_LOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_CLOSED_UNLOCKED
  def ON_DOOR_CLOSED_UNLOCKED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow_cycle)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_INVALID_KEY(self):
    """ While in DOOR_CLOSED_UNLOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_UNLOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_CLOSED_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_VALID_KEY(self):
    """ While in DOOR_CLOSED_UNLOCKED, a VALID_KEY message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_CLOSED_GRANTING_LOCKED
  def ON_DOOR_CLOSED_GRANTING_LOCKED(self):
    self.qc.Layer_1.set_next(self.qc.color_wipe_to_handle_white)

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in DOOR_CLOSED_GRANTING_LOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_GRANTING_LOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_CLOSED_GRANTING_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_OPEN_GRANTING_LOCKED
  def ON_DOOR_OPEN_GRANTING_LOCKED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_OPEN_GRANTING_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT(self):
    """ While in DOOR_OPEN_GRANTING_LOCKED, a MAIN_DOOR_OPEN_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_OPEN_GRANTING_LOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_OPEN_LOCKED
  def ON_DOOR_OPEN_LOCKED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in DOOR_OPEN_LOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_OPEN_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_LOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_OPEN_LOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_OPEN_UNLOCKED
  def ON_DOOR_OPEN_UNLOCKED(self):
    self.qc.Layer_0.set_next(self.qc.rainbow)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_OPEN_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in DOOR_OPEN_UNLOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_OPEN_UNLOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_CLOSED_GRANTING_UNLOCKED
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED(self):
    self.qc.Layer_1.set_next(self.qc.color_wipe_to_handle_white)

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in DOOR_CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_STUCK_OPEN_LOCKED
  def ON_DOOR_STUCK_OPEN_LOCKED(self):
    self.qc.Layer_0.set_next(self.qc.flash_colors_red_black)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_STUCK_OPEN_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_LOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_STUCK_OPEN_LOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_STUCK_OPEN_UNLOCKED
  def ON_DOOR_STUCK_OPEN_UNLOCKED(self):
    self.qc.Layer_0.set_next(self.qc.flash_colors_red_black)
    self.qc.Layer_1.clear()

   
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_UNLOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_STUCK_OPEN_UNLOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_STUCK_OPEN_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  
  # By Default - do nothing ON_INVALID_KEY
  def ON_INVALID_KEY(self):
    self.qc.Layer_1.set_next(self.qc.flash_colors_red_black)

   
  # By default - do nothing during transitions
  def ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT(self):
    """ While in INVALID_KEY, a MAIN_DOOR_INVALID_TIMEOUT message is recieved. """
    pass


def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_DOOR"

  doorstate = DoorState(name=name)
  doorstate.setup(out_queue, name=name)
  doorstate.start()

  doorstate.send_message({"event": "VALID_KEY"})

  logging.info('unlock the door, open then close it')
  doorstate.send_message({"event":"VALID_KEY"})
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_OPENED"})
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

  logging.info('current state:' + doorstate.current_state())
  logging.info('unlock the door but do not open it')
  time.sleep(2)
  doorstate.send_message({"event":"VALID_KEY"})
  time.sleep(10)


  logging.info('open the door and close it quickly')
  time.sleep(0.1)
  doorstate.send_message({"event":"VALID_KEY"})
  doorstate.send_message({"event":"DOOR_OPENED"})
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

  logging.info('open the door and leave it open for 30 seconds')
  time.sleep(2)
  doorstate.send_message({"event":"VALID_KEY"})
  doorstate.send_message({"event":"DOOR_OPENED"})
  time.sleep(30)

  time.sleep(2)
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

  logging.info('force the door open')
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_OPENED"})
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

if __name__=='__main__':
  main()
