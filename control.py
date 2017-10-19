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
	timeout = 0


control = Control()


# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
	#print(client)
	#print(userdata)
	#print(msg.topic)
	#print(msg.payload)

	if "TURNSTILE" in msg.payload:
		#print "MESSAGE FROM TURNSTILE %s" % msg.payload
		i = msg.payload.find("requests entry for passenger")
		if i > 0:
			pid = msg.payload[i+30:]
			p = Passenger(int(pid))

			if len(control.passengers) < PLATFORM_CAPACITY:
				control.passengers.append(p)
				mqtt_message = "CONTROL allow passenger #%d" % p.id
				send_message(mqtt_message)

				if len(control.passengers) == CAR_CAPACITY:
					control.state = State.WAITING_FOR_CAR
					mqtt_message = "PICKUP a %s" % control.passengers
					send_message(mqtt_message)
			else:
				mqtt_message = "CONTROL platform is full"
				send_message(mqtt_message)
	elif "CAR" in msg.payload:
		print "MESSAGE FROM CAR %s" % msg.payload
		splits = str.split(msg.payload, " ")
		if splits[4] == "a":
			if splits[5] == "ACCEPT":
				control.timeout = 0
				control.state = State.WAITING_FOR_PASSENGERS
				del control.passengers[:]

def main():

	mqtt_client.will_set(mqtt_topic, '______________Will of CONTROL_________________\n\n', 0, False)

	# other callbacks are set in shared.py
	mqtt_client.on_message = on_message

	mqtt_client.subscribe(mqtt_topic)
	mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

	while True:
		if control.state == State.WAITING_FOR_CAR:
			time.sleep(0.5)
			control.timeout = control.timeout + 1
			if control.timeout > 15:
				send_message("CONTROL timeout, re-sending")
				send_message("PICKUP a %s" % control.passengers)
				control.timeout = 0
		else:
			time.sleep(3)

main()