import ConfigParser
import logging
import logging.config
import Queue

# Read the configuration file
config = ConfigParser.RawConfigParser()
config.read('machine.conf')

# Initialize logging
logging.config.fileConfig('logging.conf')
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
    module = map(__import__, [module_name])
    logger.info("  machine class: " + classname)
    logger.info("  machine module: " + module_name)
    setup_params = {}
    for key, val in config.items(section):
      logger.info('    ' + key + '=' + val)
      # Create a dictionary of params from the configuration file for 
      # initialization of the reader.
      if key not in ['classname','module']:
          setup_params[key] = val
    constructor = getattr(module[0], classname)
    machine = constructor()
    # set the same output queue for each machine so that they can coordinate
    machine.setup(out_queue=out_queue, **setup_params)
    machines.append(machine)

logger.info("machine setup completed")

# everything is configured, start each individual machine
logger.info("starting machines")
for machine in machines:
  logger.info("starting " + str(machine))
  machine.start()

logger.info("machine start completed")

# loop and forward events to all machines
while True:
  try:
    message = out_queue.get(True, 0.1)
    logger.debug("got event:" + str(message))
    for machine in machines:
      logger.debug("sending " + str(message) + " to " + str(machine))
      machine.send_message(message)
    out_queue.task_done()
  except Queue.Empty:
    # keep handling events
    #logger.debug("no event seen")
    pass
