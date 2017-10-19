import time
from enum import Enum
from shared import *


class State(Enum):
	CAN_SEND = 0
	WAITING_FOR_ACK = 1


class Turnstile():
	state = State.CAN_SEND
	cur_passenger = 0
	timeout = 0


turnstile = Turnstile()


def on_message(client, userdata, msg):
	# we only listen for messages from CONTROL
	if "CONTROL" in msg.payload:
		if turnstile.state == State.WAITING_FOR_ACK:
			if "allow passenger" in msg.payload:
				turnstile.state = State.CAN_SEND


def main():
	mqtt_client.will_set(mqtt_topic, '___Will of TURNSTILE___', 0, False)
	mqtt_client.on_message = on_message
	mqtt_client.loop_start()

	while True:
		choice = raw_input("[TURNSTILE (%d)]: (p) for passenger, (q) to quit: " % turnstile.cur_passenger)
		if choice == 'p':
			# if we have not received acknowledgement of cur_passenger, just re-send same passenger
			if turnstile.state == State.CAN_SEND:
				turnstile.cur_passenger = turnstile.cur_passenger + 1
				turnstile.state = State.WAITING_FOR_ACK
			send_message("TURNSTILE requests entry for passenger #%d" % turnstile.cur_passenger)
		elif choice == 'q':
			exit_program()


if __name__ == '__main__': main()