import asyncio
from bleak import BleakClient, BleakScanner
import time
import json
import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
# from awscrt import io, mqtt, auth, http      #for AWS
# from awsiot import mqtt_connection_builder 	#for AWS

SERVICE_uuid="12345678-1234-1234-1234-123456789012"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-210987654321"

'''
#for AWS
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint="a44c85l039mit-ats.iot.us-east-1.amazonaws.com",
    cert_filepath="/home/aws-test/Adarsh_Narendran_Test/certs/device.pem.crt",
    pri_key_filepath="/home/aws-test/Adarsh_Narendran_Test/certs/private.pem.key",
    ca_filepath="/home/aws-test/Adarsh_Narendran_Test/certs/AmazonRootCA1.pem",
    client_id="RaspberryPiClient",
    clean_session=False,
    keep_alive_secs=30
)
'''

'''
# for AWS
print("Connecting to AWS IoT...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

topic = "Topic1"
'''
def publish(message):
	client = mqtt.Client()
	client.connect("192.168.81.254" , 1883 , 60)

	msg = message
	client.publish("test/topic" , msg)
	print(f"Published message: {msg}");

	client.disconnect()

try:


	async def main():
		devices = await BleakScanner.discover()
		for device in devices:		
			if device.name =="ESP32_BLE_Client1":
				print(" device name recoganized")
				async with BleakClient(device.address) as client:
					while True:
						value = await client.read_gatt_char(CHARACTERISTIC_UUID)
						print(f"Received: {value.decode('utf-8')}")
						
						message=value.decode('utf-8')
						publish(message)			
						
						'''
						def show_message():
							root=tk.Tk()
							root.title("Message")
							label=tk.Label(root, text=message, padx=30, pady=30)
							label.pack()
    
							root.mainloop()
							
						if __name__=="__main__":
							show_message()
							
						'''
						# mqtt_connection.publish(topic=topic,payload=json.dumps(message),qos=mqtt.QoS.AT_LEAST_ONCE) #for AWS 
						await asyncio.sleep(2)
    
	asyncio.run(main())
	print("completed")

	# Wait for the message to be sent
	time.sleep(2)

	'''
	#for AWS 
	print("Disconnecting...")
	disconnect_future = mqtt_connection.disconnect()
	disconnect_future.result()
	print("Disconnected!")
	'''
except Exception as e:
	print(f"An error occured: {e}")


