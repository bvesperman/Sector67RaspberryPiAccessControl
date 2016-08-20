from DerivedBaseClasses.mode_switchBase import *
import sys
if sys.platform=='linux2':
  import RPi.GPIO as GPIO

class mode_switchStateMachine(mode_switchBase):
  __metaclass__ = ABCMeta
  """description of class"""

  def setup(self, out_queue, name, gpio_pin):
    self.log = logging.getLogger("mode_switch")
    self.out_queue = out_queue
    self.name = name
    self.gpio_pin=int(gpio_pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    state = GPIO.input(self.gpio_pin)
    if (state == True):
      super(mode_switchStateMachine, self).start(self.LOCKED_MODE)
    else:
      super(mode_switchStateMachine, self).start(self.UNLOCKED_MODE)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)

  def WHILE_UNLOCKED_MODE(self, ev):
    """  """
    if GPIO.input(self.gpio_pin):
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LOCKED_MODE"})

  def WHILE_LOCKED_MODE(self, ev):
    """  """
    if not GPIO.input(self.gpio_pin):
      self.generate_message({"event": "REQUEST_MAIN_DOOR_UNLOCKED_MODE"})
    


def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_mode_switch"

  mode_switchTestMachine = mode_switchStateMachine(name=name)
  mode_switchTestMachine.setup(out_queue, name=name)
  mode_switchTestMachine.start()

  # Send some test messages
  
  # Start Testing sample state machine by sending some random messages
  # Current State: UNLOCKED
  # Next State: LOCKED
  # Send Message 10 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 9 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 8 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 7 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 6 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 5 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 4 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 3 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 2 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 1 after 2 seconds.
  time.sleep(2)
  mode_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  

if __name__=='__main__':
  main()
