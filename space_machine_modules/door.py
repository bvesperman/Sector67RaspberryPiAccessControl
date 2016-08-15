import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

from DerivedBaseClasses.doorBase import *

class DoorState(doorBase):
  __metaclass__ = ABCMeta
  """description of class"""
  
  

    
  def setup(self, out_queue, name, unlock_timeout=5, open_unlock_timeout=1, stuck_open_timeout=15):
    self.log = logging.getLogger("DoorState")
    self.out_queue = out_queue
    self.name = name
    self.unlock_timeout = int(unlock_timeout)
    self.open_unlock_timeout = int(open_unlock_timeout)
    self.stuck_open_timeout = int(stuck_open_timeout)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # assume a starting state of CLOSED_LOCKED and appropriate messages will send it to the correct state
    super(DoorState, self).start(self.CLOSED_LOCKED)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)


  # By Default - do nothing ON_CLOSED_LOCKED
  def ON_CLOSED_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_INVALID_KEY(self):
    """ While in CLOSED_LOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in CLOSED_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_VALID_KEY(self):
    """ While in CLOSED_LOCKED, a VALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_LOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_CLOSED_UNLOCKED
  def ON_CLOSED_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_INVALID_KEY(self):
    """ While in CLOSED_UNLOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_UNLOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in CLOSED_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_VALID_KEY(self):
    """ While in CLOSED_UNLOCKED, a VALID_KEY message is recieved. """
    pass
      
  
  # By Default - do nothing ON_CLOSED_GRANTING_LOCKED
  def ON_CLOSED_GRANTING_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in CLOSED_GRANTING_LOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_GRANTING_LOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in CLOSED_GRANTING_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  
  # By Default - do nothing ON_OPEN_GRANTING_LOCKED
  def ON_OPEN_GRANTING_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in OPEN_GRANTING_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT(self):
    """ While in OPEN_GRANTING_LOCKED, a MAIN_DOOR_OPEN_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in OPEN_GRANTING_LOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_OPEN_LOCKED
  def ON_OPEN_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in OPEN_LOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in OPEN_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_LOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in OPEN_LOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_OPEN_UNLOCKED
  def ON_OPEN_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_OPEN_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in OPEN_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in OPEN_UNLOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_UNLOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in OPEN_UNLOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_CLOSED_GRANTING_UNLOCKED
  def ON_CLOSED_GRANTING_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_STUCK_OPEN_LOCKED
  def ON_STUCK_OPEN_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in STUCK_OPEN_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_LOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in STUCK_OPEN_LOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_STUCK_OPEN_UNLOCKED
  def ON_STUCK_OPEN_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_UNLOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in STUCK_OPEN_UNLOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in STUCK_OPEN_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  
  # By Default - do nothing ON_INVALID_KEY
  def ON_INVALID_KEY(self):
    """  """
    pass

   
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
