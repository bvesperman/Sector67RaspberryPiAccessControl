#!/usr/bin/python
import json
import requests
from suds.client import Client

class SectorAdmin:



    def GetAuthorizedUsers( self, MachineID):

 	#url = "https://www.pinsoft.net/sectorbilling/payments.asmx?wsdl"
	#client = Client(url)
	#data = client.service.GetMachineAuthorizationByMachineIDForPI(MachineID)
        #result = json.loads(data)
        response = requests.get('http://www.sector67.org/blog/api/machine/get_rfids_for_machine/?machine_id={0}'.format(MachineID))
	return response.json()



    def UpdateMachine(self, MachineID):

	myFile = open("/home/pi/sysinfo/ipinfo.txt")

	ipAddress = ""
	macAddress = ""
	
	
	i = 0

	for myLine in myFile:
		if i==1	:
			print()
			ipAddress = myLine[20:35]

			i = i + 1


		if i==0	:
			print()
			macAddress  = myLine[38:60]

			i = i + 1
	print("ipAddress" + ipAddress)
	print("macAddress" + macAddress)
	url = "https://www.pinsoft.net/sectorbilling/payments.asmx?wsdl"
	client = Client(url)
	client.service.UpdateMachine(MachineID, ipAddress, macAddress)



    def AddMachinePayment ( self, RFID, Amount, MachineID, Description, Image):

 	url = "https://www.pinsoft.net/sectorbilling/payments.asmx?wsdl"
	client = Client(url)
	data = client.service.AddMachinePayment(RFID,Amount,MachineID, Description, 0)
        #result = json.loads(data)
	#return result
