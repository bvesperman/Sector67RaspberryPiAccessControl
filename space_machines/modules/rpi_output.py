from DerivedBaseClasses.switchBase import *
import sys
if sys.platform=='linux2':
  import RPi.GPIO as GPIO


class RpiGpioOutput(StateMachine):

  def ON_ON(self):
    GPIO.output(self.gpio_pin, 1)

  def ON_OFF(self):
    GPIO.output(self.gpio_pin, 0)

  def setup(self, out_queue, name, gpio_pin, on_message, off_message, initial_state):
    self.logger = logging.getLogger("RpiGpioOutput")
    self.out_queue = out_queue
    self.name = name
    self.gpio_pin=int(gpio_pin)
    self.on_message = on_message
    self.off_message = off_message
    self.initial_state = initial_state

  def start(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.OUT)
    if (self.initial_state == "ON"):
      self.logger.debug("initial state: " + self.on_message)
      super(RpiGpioOutput, self).start(self.ON)
    else:
      self.logger.debug("initial state: " + self.off_message)
      super(RpiGpioOutput, self).start(self.OFF)

  def config_gui(self, root):
    self.show_gui = True
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)
