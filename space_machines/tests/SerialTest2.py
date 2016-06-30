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
   #ser = serial.Serial('/dev/ttyAMA0',2400, timeout=1.0)
   #ser = serial.Serial('/dev/ttyAMA0',2400, timeout=None)
   ser = serial.Serial('/dev/ttyAMA0',2400, timeout=1.0, interCharTimeout=None)
   #ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),  newline = '\r', line_buffering = True)

   while True:
       # read the standard input to see if the RFID has been swiped
       #while sys.stdin in select.select([sys.stdin],[],[],0)[0]:

       bytesToRead = ser.inWaiting()
       #print("bytes:" + str(bytesToRead))
       if bytesToRead > 0:
         s = ser.read(bytesToRead)
         bytes = ":".join("{:02x}".format(ord(c)) for c in s)
         print(bytes)
       
       #print("Before RFID serial read")
       #byte = ser.read(1)
       #sys.stdout.write(byte)
       #print("{:02x}".format(ord(byte)))

       #bytesToRead = ser.inWaiting()
       #if (bytesToRead > 0):
           #print("Reading " + str(bytesToRead) + " bytes")
           #raw_data = ser.read(bytesToRead)
           #print(raw_data)
           #time.sleep(0.2)
       #print("After RFID serial read")
       time.sleep(0.1)
       

except:
   print("Main exception")
   raise
