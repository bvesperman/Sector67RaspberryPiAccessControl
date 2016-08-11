import ConfigParser
import logging
import logging.config
import Queue
import threading
import time
import datetime
import sys
import space_machines

from Tkinter import *


class MessageThread:
  """ Since the tkinter thread wants to be the main loop, create a thread
    to handle messages
  """

  def config_gui(self, root):
    self.root = root
    logFrame = LabelFrame(root, text="events", padx=5, pady=5)
    logFrame.pack(fill=X)
    scrollb  = Scrollbar(logFrame, orient=VERTICAL)
    self.events = Text(logFrame, wrap=WORD)
    self.events.pack(fill=X)
    self.events.config(yscrollcommand = scrollb.set)
    self.events.pack(side=LEFT, fill=BOTH, expand=True)
    scrollb.config(command = self.events.yview) 
    scrollb.pack(side=RIGHT, fill=Y)

  def start_thread(self):
    self.thread = threading.Thread(target=self.do_work)
    self.thread.setDaemon(True)
    self.thread.start()

  def do_work(self):
    # loop and forward events to all machines
    while True:
      try:
        message = out_queue.get(True, 0.1)
        logger.info(str(message))
        logger.debug("got event:" + str(message))
        if show_gui:
          self.events.insert('end', str(datetime.datetime.now()) + " event: " + str(message)  + "\n")
          self.events.see(END)
        for machine in machines:
          logger.debug("sending " + str(message) + " to " + str(machine))
          machine.send_message(message)
        out_queue.task_done()
      except Queue.Empty:
        # keep handling events
        #logger.debug("no event seen")
        pass

# Determine the configuration file to read

config_file_name='machine.conf'
if len(sys.argv) >= 2:
   config_file_name = sys.argv[1]

# Read the configuration file
config = ConfigParser.RawConfigParser()
config.read(config_file_name)
show_gui = False
if config.getboolean('Main', 'show_gui'):
  show_gui = True

# Initialize logging
log_file_name='s_m_logging.conf'
if len(sys.argv) == 3:
   log_file_name = sys.argv[2]

logging.config.fileConfig(log_file_name)
logger = logging.getLogger('main')

# Read all machines in the config file and initialize them
# extract parameters from the file and call the constructor of the class 
# with those parameters.
machines = []
# the queue that all machines write to to send messages to each other
out_queue = Queue.Queue()

logger.info("reading machine configuration")
for section in config.sections():
  if section.startswith("Machine"):
    logger.info("initializing " + section)
    classname = config.get(section, 'classname')
    module_name = config.get(section, 'module')
    module = getattr(space_machines, module_name)
    logger.info("  machine class: " + classname)
    logger.info("  machine module: " + module_name)
    setup_params = {}
    for key, val in config.items(section):
      logger.info('    ' + key + '=' + val)
      # Create a dictionary of params from the configuration file for 
      # initialization of the reader.
      if key not in ['classname','module']:
          setup_params[key] = val
    constructor = getattr(module, classname)
    machine = constructor()
    # set the same output queue for each machine so that they can coordinate
    machine.setup(out_queue=out_queue, **setup_params)
    machines.append(machine)

logger.info("machine setup completed")

broker = MessageThread()

if show_gui: 
  logger.info("starting gui configuration")
  root = Tk()
  for machine in machines:
    logger.info("configuring gui " + str(machine))
    try:
      machine.config_gui(root)
    except AttributeError:
      pass
  broker.config_gui(root)


# everything is configured, start each individual machine
logger.info("starting machines")
for machine in machines:
  logger.info("starting " + str(machine))
  machine.start()

logger.info("machine start completed")

broker.start_thread()
logger.info("broker start completed")

if show_gui: 
  root.mainloop()
  #root.destroy() 
else:
  while True:
    time.sleep(60)
