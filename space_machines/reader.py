import logging
import time
import Queue
import threading
import serial

from expiringdict import ExpiringDict

from pystates import StateMachine

class SerialRfidReader(StateMachine):

  def READING(self):
    while True:
      # no state transitions for this class, read keys and send messages
      while True:
        ev = yield
        # Python serial has some sort of internal buffer that is resulting in
        # data not being sent right away.  Initializing with interCharTimeout
        # seems to resolve that.  Reading character by character is a necessary
        # hack to resolve that
        key = ""
        try:
          while True:
            s = self.ser.read()
            key = key + s
            if s == "\r":
              #bytes = ":".join("{:02x}".format(ord(c)) for c in key)
              self.log.debug("read key KEY_READ [" + key + "]")
              break
          # clear all extra input
          key = key.strip()
          if key == "":
            break 
          if self.cache.get(key) == key:
            self.log.debug("ignoring duplicate key read [" + key + "]")
            break 
          #attempt to parse the key in the same manner as downstream
          decimal_id = int(key, 16)& 0x00FFFFFFFF
          message = {"event": "KEY_READ", "key": key}
          self.cache[key] = key
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)
        except:
          self.logger.exception("An exception was encountered while reading a key")

  def setup(self, out_queue, name, port, baud, cache_timeout):
    self.log = logging.getLogger("SerialRfidReader")
    self.out_queue = out_queue
    self.name = name
    self.port = port
    self.baud = baud
    self.cache_timeout = cache_timeout

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    self.ser = serial.Serial(self.port,self.baud, timeout=None, interCharTimeout=None)
    # use an ExpiringDict to de-duplicate
    self.cache = ExpiringDict(max_len=100, max_age_seconds=5)
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
