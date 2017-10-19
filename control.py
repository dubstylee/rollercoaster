import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal
from enum import Enum

from shared import *

MY_NAME = 'Brian W'

class State(Enum):
	WAITING_FOR_PASSENGERS = 0
	WAITING_FOR_CAR = 1


class Control():
	state = State.WAITING_FOR_PASSENGERS
	passengers = []


control = Control()


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
		p = Passenger(int(pid))

		if len(control.passengers) < PLATFORM_CAPACITY:
			control.passengers.append(p)
			mqtt_message = "CONTROL allow passenger #%d" % p.id
			send_message(mqtt_message)

			if len(control.passengers) == CAR_CAPACITY:
				mqtt_message = "PICKUP a %s" % control.passengers
				send_message(mqtt_message)
		else:
			mqtt_message = "CONTROL platform is full"
			send_message(mqtt_message)


def main():

	mqtt_client.will_set(mqtt_topic, '______________Will of CONTROL_________________\n\n', 0, False)

	# other callbacks are set in shared.py
	mqtt_client.on_message = on_message

	mqtt_client.subscribe(mqtt_topic)
	mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

	while True:
		time.sleep(3)
		#choice = raw_input("[CONTROL]: (r) request pickup (q) quit: ")

		#if choice == "r":
		#	if control.state == State.WAITING_FOR_CAR:
		#		print("already waiting for a car")
		#	elif control.passengers < NUM_PASSENGERS:
		#		print("not ready for pickup yet")
		#	else:
		#		control.state = State.WAITING_FOR_CAR
		#		mqtt_message = "PICKUP %s" % control.passengers
		#		send_message(mqtt_message)
		#elif choice == "q":
		#	exit_program()

main()