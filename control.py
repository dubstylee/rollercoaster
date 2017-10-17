import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal
from enum import Enum

from shared import *

MY_NAME = 'Brian W' # change to your name
NUM_PASSENGERS = 3

class State(Enum):
	WAITING_FOR_PASSENGERS = 0
	WAITING_FOR_CAR = 1

class Control():
	state = State.WAITING_FOR_PASSENGERS
	passengers = 0

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

control = Control()

# Instantiate the MQTT client
#mqtt_client = paho.Client()
mqtt_topic = 'cis650/somethingcool'


# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
	#print(client)
	#print(userdata)
	print(msg.topic)
	print(msg.payload)
	i = msg.payload.find("requests passenger entry")
	if i > 0:
		timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
		if control.passengers < NUM_PASSENGERS:
			control.passengers = control.passengers + 1
			mqtt_message = "[%s] %s CONTROL allow passenger" % (timestamp,ip_addr)
		else:
			mqtt_message = "[%s] %s CONTROL platform is full" % (timestamp,ip_addr)
		mqtt_client.publish(mqtt_topic, mqtt_message)

	# Here is where you write to file and unsubscribe
	#with open("test.txt", "a+") as myfile:
		#if name not in myfile.read():
			#myfile.write(name+"\n")
		#myfile.close()

def main():

	# other callbacks are set in shared.py
	mqtt_client.on_message = on_message

	mqtt_client.will_set(mqtt_topic, '______________Will of CONTROL_________________\n\n', 0, False)
	broker = 'sansa.cs.uoregon.edu'
	mqtt_client.connect(broker, '1883')

	# You can subscribe to more than one topic: https://pypi.python.org/pypi/paho-mqtt#subscribe-unsubscribe.
	# If you do list more than one topic, consdier using message_callback_add for each topic as described above.
	# For below, wild-card should do it.
	mqtt_client.subscribe(mqtt_topic)
	mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

	while True:
		choice = raw_input("[CONTROL]: (r) request pickup (q) quit: ")

		if choice == "r":
			if control.state == State.WAITING_FOR_CAR:
				print("already waiting for a car")
			elif control.passengers < NUM_PASSENGERS:
				print("not ready for pickup yet")
			else:
				control.state = State.WAITING_FOR_CAR
				timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
				mqtt_message = "[%s] %s PICKUP %d passengers" % (timestamp,ip_addr,control.passengers)
				mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
				print("request pickup")
		elif choice == "q":
			exit()

# I have the loop_stop() in the control_c_handler above. A bit kludgey.

main()

