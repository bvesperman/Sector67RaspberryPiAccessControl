# Copyright (c) 2009 Eric Gradman (Monkeys & Robots)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
pystates - A simple and powerful python state machine framework using coroutines

Example:

  from pystates import StateMachine, State

  class MyMachine(StateMachine):
    def IDLE(self):
      while True:
        ev = yield
        if ev.type == pygame.KEYDOWN:
          self.transition("RUNNING", ev.key)

    class RUNNING(State):
      def eval(self, key):
        print "you pressed the %s key" % key
        while True:
          ev = yield
          if self.duration() > 5.0:
            self.transition("COUNTDOWN")

    class COUNTDOWN(State):
      def eval(self):
        i = 10
        while True:
          ev = yield
          print "i = %d" % i
          if i == 0:
            self.transition("IDLE")
          i -= 1

See the README for a details on how to implement your own StateMachines
"""

import time 
import logging
import Queue
import threading

class ThreadedExecutor(threading.Thread):
  def __init__(self, machine, in_queue):
    threading.Thread.__init__(self)
    self.in_queue = in_queue
    self.machine = machine
    self.logger = logging.getLogger("pystate.ThreadedExecutor")

  def run(self):
    while True:
      try:
        event = self.in_queue.get(True, 0.1)
        self.machine.handle(event)
        self.in_queue.task_done()
      except Queue.Empty:
        # allow the state machine to keep handling events
        event = {"event":""}
        self.machine.handle(event)

class StateMachine(object):
  """StateMachine
  Do not instantiate this class directly.  Instead, make a subclass.  Your
  subclass should contain nested subclasses of State that implement the states
  your machine can achieve.
  """

  def __init__(self, name=None, time=time.time):
    """
    Keyword arguments:
      name: The name by which your StateMachine is known. It defaults to the name of
            the class
      time: An alternative function used to tell time.  For example, sometimes with
            pygame its useful to use pygame.ticks for consistency.  It defaults to
            time.time()
    """
    self.name = name and name or str(self.__class__.__name__)
    self.time = time
    self.logger = logging.getLogger("pystate.StateMachine")
    self.show_gui = False

  def handle(self, ev):
    """
    When you call this method, this machine's current state will resume with
    the supplied ev object.
    """
    try:
      return self.state_gen.send(ev)
    except StopIteration, exc:
      self.state_gen = exc.args[0]

  def start(self, state_func, *state_args):
    """
    If this machine has a state named by the state_func argument, then the machine
    will activate the named state.  This is essentially a transition from a NULL
    state to the named state.

    Any args are passed to the eval method of the named state.
    """
    self.logger.debug("pystate start called")
    self.state_gen = self.activate_state(state_func, state_args)
    self.in_queue = Queue.Queue()
    self.thread = ThreadedExecutor(self, self.in_queue)
    self.thread.setDaemon(True)
    self.thread.start()

  def send_message(self, message):
    if self.in_queue != None:
      self.in_queue.put(message)

  def generate_message(self, message):
    if self.out_queue != None:
      self.out_queue.put(message)

  def transition(self, state_func, *state_args):
    """
    If this machine has a state named by the state_func argument, then the machine
    will transition to the named state.

    Any args are passed to the new state_func.
    """
    state_gen = self.activate_state(state_func, state_args)
    raise StopIteration(state_gen)

  def activate_state(self, state_func, state_args):
    self.logger.debug("%s activating state %s", str(self), state_func.__name__)

    self.state_start_time = self.time()
    state_gen = state_func(*state_args)
    state_gen.next()
    return state_gen

  def duration(self):
    return self.time() - self.state_start_time

  def current_state(self):
    return self.state_gen.__name__

  def __str__(self):
    return "<StateMachine:%s>" % self.name
