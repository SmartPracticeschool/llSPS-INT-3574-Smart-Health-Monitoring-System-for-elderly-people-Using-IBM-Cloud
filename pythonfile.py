import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "6prp7r"
deviceType = "WEARABLESMARTBAND"
deviceId = "wsb123"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        hum=random.randint(60, 77)
        #print(hum)
        temp =random.randint(96, 98)
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Ratepulse': hum }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Ratepulse= %s %%" % hum, "to IBM Watson")

        success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
