import logging
import time
import Queue
import threading
import serial

from pystates import StateMachine

class SerialRfidReader(StateMachine):

  def READING(self):
    while True:
      # no state transitions for this class, read keys and send messages
      while True:
        ev = yield
        self.log.debug('before serial readline')
        key = self.ser.readline()
        key = key.strip()
        self.log.debug("read key [" + key + "]")
         
        self.log.debug("After RFID serial read")
        message = {"event": "KEY_READ", "key": key}
        self.logger.debug("generating message: " + str(message))
        self.generate_message(message)

  def setup(self, out_queue, name, port, baud):
    self.log = logging.getLogger("SerialRfidReader")
    self.out_queue = out_queue
    self.name = name
    self.port = port
    self.baud = baud

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    self.ser = serial.Serial(self.port,self.baud, timeout=None)
    super(SerialRfidReader, self).start(self.READING)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "SERIAL_READER"
  machine = SerialRfidReader(name=name)
  machine.setup(out_queue, name=name, port='/dev/ttyAMA0', baud='2400')
  machine.start()

  time.sleep(15)

if __name__=='__main__':
  main()
