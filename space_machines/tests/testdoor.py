import unittest
import time
import Queue
import logging
import sys
import xmlrunner

sys.path.append('../space_machines')
sys.path.append('space_machines')
from door import DoorState

class DoorTests(unittest.TestCase):

  def setUp(self):
    logging.basicConfig(level=logging.WARN)
    self.doorstate = DoorState()
    self.doorstate.setup(None, name="TEST_DOOR")
    self.doorstate.start()
    
  def test_quick_open_close(self):
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")
    self.doorstate.send_message({"event": "VALID_KEY"})
    time.sleep(0.1)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_UNLOCKING")
    self.doorstate.send_message({"event":"DOOR_OPENED"})
    time.sleep(0.1)
    self.assertEqual(self.doorstate.current_state(), "OPEN_UNLOCKING")
    self.doorstate.send_message({"event":"DOOR_CLOSED"})
    time.sleep(0.1)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")

  def test_open_wait_close(self):
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")
    self.doorstate.send_message({"event": "VALID_KEY"})
    time.sleep(2)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_UNLOCKING")
    self.doorstate.send_message({"event":"DOOR_OPENED"})
    time.sleep(0.2)
    self.assertEqual(self.doorstate.current_state(), "OPEN_UNLOCKING")
    time.sleep(2)
    self.assertEqual(self.doorstate.current_state(), "OPEN_LOCKED")
    self.doorstate.send_message({"event":"DOOR_CLOSED"})
    time.sleep(2)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")

  def test_open_longwait_close(self):
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")
    self.doorstate.send_message({"event": "VALID_KEY"})
    time.sleep(2)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_UNLOCKING")
    self.doorstate.send_message({"event":"DOOR_OPENED"})
    time.sleep(20)
    self.assertEqual(self.doorstate.current_state(), "STUCK_OPEN")
    self.doorstate.send_message({"event":"DOOR_CLOSED"})
    time.sleep(2)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")

  def test_force_open(self):
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")
    self.doorstate.send_message({"event":"DOOR_OPENED"})
    time.sleep(0.2)
    self.assertEqual(self.doorstate.current_state(), "FORCED_OPEN")
    self.doorstate.send_message({"event":"DOOR_CLOSED"})
    time.sleep(0.2)
    self.assertEqual(self.doorstate.current_state(), "CLOSED_LOCKED")

if __name__ == '__main__':
    unittest.main()
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))