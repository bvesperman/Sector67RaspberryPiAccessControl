import requests

import json
import datetime
import RFIDDataAccess
import SectorAdminSite
import sys
import time 
import datetime 
import RPi.GPIO as io 
import select
from time import gmtime, strftime
import subprocess
import os
import MachineLogic
import logging 
import serial
print("wakeup")

FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename='/home/pi/' + time.strftime("%Y%m%d") + ".txt" , level=logging.INFO, format=FORMAT)

#log to console as well
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)-15s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

localRFID = ""
rebootTime = time.time() + 86400

logging.info("Before MachineLogic call")
machine = MachineLogic.MachineLogic()
logging.info("After MachineLogic call")
logging.info("Before machine.Setup call")
machine.Setup()
logging.info("machine.Setup call complete")

logging.info("Before RFIDAccess call")
access = RFIDDataAccess.DataAccess()
logging.info("RFIDAccess call complete")
logging.info("Before authService call")
authService = SectorAdminSite.SectorAdmin()
logging.info("authService call complete")

try:

	#Pull down the current list of authorized users
	logging.info("Before GetAuthorizedUsers call")
	data = authService.GetAuthorizedUsers(machine.machineID)
	#authService.UpdateMachine(machineID)
	logging.info("GetAuthorizedUsers call complete")

	#Delete Current Cache of Authorized users
	logging.info("Before DeleteAllAuthorizedUsers call")
	access.DeleteAllAuthorizedUsers()
	logging.info("DeleteAllAuthorizedUsers call complete")


	#add the users to the cache
	logging.info("Before InsertAuthorizedUsers loop")
	users = []
	for user in data["message"]:
		logging.info("Before InsertAuthorizedUsers call")
		#access.InsertAuthorizedUser(user["rfid"],0,user["display_name"])  
		users.append({"rfid":user["rfid"], "uid":0, "username":user["display_name"]})
		logging.info("InsertAuthorizedUsers call complete [" + user["rfid"] + "] [" + user["display_name"] + "]")
	logging.info("InsertAutorizedUsers loop complete")
	access.InsertAuthorizedUsers(users)
	logging.info("InsertAutorizedUsers call complete")


except:
	logging.exception("Init died")
	print('exception')
#rebootTime = time.time() + 60

  
try: 
   
   #loop forever
   logging.info("Beginning main loop")

   while True:
       #print("loop")
       logging.debug("Initializing serial device")
       ser = serial.Serial('/dev/ttyAMA0',2400, timeout=1.0)
       time.sleep(.25)
       # read the standard input to see if the RFID has been swiped
       #while sys.stdin in select.select([sys.stdin],[],[],0)[0]:
       #localRFID = sys.stdin.readline()
       
       logging.debug("Before RFID serial read")
       sys.stdout.write('.')
       sys.stdout.flush()
       localRFID = ser.read(12)
       sys.stdout.write(':')
       sys.stdout.flush()
       
       logging.debug("After RFID serial read: [" + localRFID + "]")
       #print(localRFID)
       #if localRFID:
       if len(localRFID) != 0 :
              #print(localRFID)
              localRFID = ''.join(localRFID.splitlines())
              logging.info("Read swipe [" + localRFID + "]")
 
              #RFID has been swiped now check if authorized
              try:
                 logging.info("Checking if the ID is authorized")
	         #print(int(localRFID, 16)& 0x00FFFFFFFF )
	         machine.rfid = int(localRFID, 16)& 0x00FFFFFFFF 
	      except:
                 logging.exception("Exception when checking authorization")
                 #print(localRFID)
                 machine.rfid = 0

              if access.IsRFIDAuthorized(int(machine.rfid)):
                 logging.info("The ID is authorized")
                 machine.DoAuthorizedWork()
              else:
                 logging.info("The ID is unauthorized")

       logging.debug("Before the DoUnAuthorizedContinuousWork call")
       machine.DoUnAuthorizedContinuousWork()
       logging.debug("The DoUnAuthorizedContinuousWork call is complete")
       #machine.CheckBeam()


       logging.debug("Before the serial close call")
       ser.close()
       logging.debug("After the serial close call")
       time.sleep(.25)
       logging.debug("After the sleep call")


       #if  time.time() > rebootTime and not machine.Busy():
       #   print("rebooting")
       #   os.system("reboot")

except:
   print("Main exception")
   logging.exception("Main loop died")
   raise
