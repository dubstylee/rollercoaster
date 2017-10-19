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
	passengers = []


# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

control = Control()

# Instantiate the MQTT client
#mqtt_client = paho.Client()
#mqtt_topic = 'cis650/somethingcool'


# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
	#print(client)
	#print(userdata)
	print(msg.topic)
	print(msg.payload)
	i = msg.payload.find("requests entry for passenger")
	if i > 0:
		pid = msg.payload[i+30:]
		#print pid
		p = Passenger(int(pid))
		#timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')

		print "count == %d" % len(control.passengers)
		if len(control.passengers) < NUM_PASSENGERS:
			control.passengers.append(p)
			mqtt_message = "CONTROL allow passenger #%d" % p.id
		else:
			mqtt_message = "CONTROL platform is full"
		send_message(mqtt_message)
		#mqtt_client.publish(mqtt_topic, mqtt_message)

	# Here is where you write to file and unsubscribe
	#with open("test.txt", "a+") as myfile:
		#if name not in myfile.read():
			#myfile.write(name+"\n")
		#myfile.close()

def main():

	mqtt_client.will_set(mqtt_topic, '______________Will of CONTROL_________________\n\n', 0, False)
	#broker = 'sansa.cs.uoregon.edu'
	#mqtt_client.connect(broker, '1883')

	# other callbacks are set in shared.py
	mqtt_client.on_message = on_message

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
				#timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
				mqtt_message = "PICKUP %s" % control.passengers
				send_message(mqtt_message)
				#mqtt_client.publish(mqtt_topic, mqtt_message)
		elif choice == "q":
			exit_program()

# I have the loop_stop() in the control_c_handler above. A bit kludgey.

main()