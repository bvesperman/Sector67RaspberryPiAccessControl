import requests

import json
import datetime
import sys
import time 
import datetime 
import io 
import select
from time import gmtime, strftime
import subprocess
import os
import logging 
import serial
import sys
print("wakeup")

try: 
   
   #loop forever
   logging.info("Beginning main loop")
   print("Initializing serial device")
   #ser = serial.Serial('/dev/ttyAMA0',2400, timeout=None)
   #ser = serial.Serial('/dev/ttyAMA0',2400, timeout=1.0, interCharTimeout=None)
   ser = serial.Serial('/dev/ttyAMA0',2400, timeout=None, interCharTimeout=None)
   #ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),  newline = '\r', line_buffering = True)
   key = ""

   while True:
       # read the standard input to see if the RFID has been swiped
       #while sys.stdin in select.select([sys.stdin],[],[],0)[0]:
       s = ser.read()
       key = key + s
       if s == "\r": 
         bytes = ":".join("{:02x}".format(ord(c)) for c in key)
         print(key)
         print(bytes)
         key = ""
         bytes = ""

except:
   print("Main exception")
   raise
