import time, socket, sys
from datetime import datetime as dt
import signal
from enum import Enum

from shared import *

MY_NAME = 'Brian W' # change to your name

class State(Enum):
	CAN_SEND = 0
	WAITING_FOR_ACK = 1

class Turnstile():
	state = State.CAN_SEND
	cur_passenger = 0
	timeout = 0


turnstile = Turnstile()


def on_message(client, userdata, msg):

	if "CONTROL" in msg.payload:
		# we only listen for messages from CONTROL
		if turnstile.state == State.CAN_SEND:
			# we don't care about incoming messages in this state
			print msg.payload
		elif turnstile.state == State.WAITING_FOR_ACK:
			# we are looking for a response for passenger #(cur_passenger)
			if "allow passenger" in msg.payload:
				turnstile.state = State.CAN_SEND
			#elif "platform is full" in msg.payload:
			#	print "platform is full, try again later"
			print msg.payload
		#elif turnstile.state == State.PLATFORM_FULL:
			# an "all clear" message will put us back to CAN_SEND
			#print msg.payload


def main():

	broker = 'sansa.cs.uoregon.edu'

	# other handlers are set in shared.py
	mqtt_client.on_message = on_message

	mqtt_client.will_set(mqtt_topic, '______________Will of TURNSTILE_________________\n\n', 0, False)
	mqtt_client.connect(broker, '1883')
	mqtt_client.subscribe(mqtt_topic)
	mqtt_client.loop_start()

	while True:
		choice = raw_input("[TURNSTILE (%d)]: (p) for passenger, (q) to quit: " % turnstile.cur_passenger)
		if choice == 'p':
			if turnstile.state == State.WAITING_FOR_ACK:
				p = Passenger(turnstile.cur_passenger)
				send_message("TURNSTILE requests entry for passenger #%d" % p.id)
				#print "Turnstile is still waiting for acknowledgement of passenger #%d" % turnstile.cur_passenger
			elif turnstile.state == State.CAN_SEND:
				turnstile.cur_passenger = turnstile.cur_passenger + 1
				p = Passenger(turnstile.cur_passenger)
				send_message("TURNSTILE requests entry for passenger #%d" % p.id)
				turnstile.state = State.WAITING_FOR_ACK	
		elif choice == 'q':
			exit_program()

main()