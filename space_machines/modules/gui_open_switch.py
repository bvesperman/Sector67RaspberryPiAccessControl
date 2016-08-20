from DerivedBaseClasses.open_switchBase import *

class open_switchStateMachine(open_switchBase):
  __metaclass__ = ABCMeta
  """description of class"""
  
  

    
  def setup(self, out_queue, name):
    self.log = logging.getLogger("open_switch")
    self.out_queue = out_queue
    self.name = name

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    state = self.state.get()
    if (state == True):
      super(open_switchStateMachine, self).start(self.CLOSED)
    else:
      super(open_switchStateMachine, self).start(self.OPEN)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.state = IntVar()
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)
    c = Checkbutton(frame, text=self.checkbutton_text, variable=self.state)
    c.pack(side=LEFT)
    c.select()

  def WHILE_OPEN(self, ev):
    """  """
    if self.state.get():
      self.generate_message({"event": "DETECTED_MAIN_DOOR_CLOSED"})

  def WHILE_CLOSED(self, ev):
    """  """
    if not self.state.get():
      self.generate_message({"event": "DETECTED_MAIN_DOOR_OPENED"})

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_open_switch"

  open_switchTestMachine = open_switchStateMachine(name=name)
  open_switchTestMachine.setup(out_queue, name=name)
  open_switchTestMachine.start()

  # Send some test messages
  
  # Start Testing sample state machine by sending some random messages
  # Current State: UNLOCKED
  # Next State: LOCKED
  # Send Message 10 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 9 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 8 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 7 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 6 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 5 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 4 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 3 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 2 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 1 after 2 seconds.
  time.sleep(2)
  open_switchTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  

if __name__=='__main__':
  main()