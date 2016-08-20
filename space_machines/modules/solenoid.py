from DerivedBaseClasses.solenoidBase import *
import sys
if sys.platform=='linux2':
  import RPi.GPIO as GPIO

class solenoidStateMachine(solenoidBase):
  __metaclass__ = ABCMeta
  """description of class"""
  
  

    
  def setup(self, out_queue, name, gpio_pin):
    self.log = logging.getLogger("solenoid")
    self.out_queue = out_queue
    self.name = name
    self.gpio_pin = int(gpio_pin)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.OUT)
    super(solenoidStateMachine, self).start(self.EXTENDED)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)

  def ON_ENTER_EXTENDED(self):
    """  """
    GPIO.output(self.gpio_pin, 1)
    self.generate_message({"event": self.name + "_EXTENDED_ENTER"})

  def ON_ENTER_RETRACTED(self):
    """  """
    GPIO.output(self.gpio_pin, 0)
    self.generate_message({"event": self.name + "_RETRACTED_ENTER"})

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_solenoid"

  solenoidTestMachine = solenoidStateMachine(name=name)
  solenoidTestMachine.setup(out_queue, name=name)
  solenoidTestMachine.start()

  # Send some test messages
  
  # Start Testing sample state machine by sending some random messages
  # Current State: UNLOCKED
  # Next State: LOCKED
  # Send Message 10 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 9 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 8 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 7 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 6 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 5 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 4 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 3 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 2 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 1 after 2 seconds.
  time.sleep(2)
  solenoidTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  

if __name__=='__main__':
  main()
