import time, socket, sys
from datetime import datetime as dt
import signal
from enum import Enum

from shared import *

MY_NAME = 'Brian W' # change to your name

class State(Enum):
	CAN_SEND = 0
	WAITING_FOR_ACK = 1
	PLATFORM_FULL = 2

class Turnstile():
	state = State.CAN_SEND
	cur_passenger = 0

# Instantiate the MQTT client
#mqtt_client = paho.Client()

turnstile = Turnstile()

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()


def on_message(client, userdata, msg):

	#print(client)
	#print(userdata)
	#print(msg.topic)
	if "CONTROL" in msg.payload:
		# we only listen for messages from CONTROL
		if turnstile.state == State.CAN_SEND:
			# we don't care about incoming messages in this state
			print msg.payload
		elif turnstile.state == State.WAITING_FOR_ACK:
			# we are looking for a response for passenger #(cur_passenger)
			if "allow passenger" in msg.payload:
				turnstile.state = State.CAN_SEND
			elif "platform is full" in msg.payload:
				turnstile.state = State.PLATFORM_FULL
				print "platform is full, try again later"
			print msg.payload
		elif turnstile.state == State.PLATFORM_FULL:
			# an "all clear" message will put us back to CAN_SEND
			print msg.payload


def main():

	broker = 'sansa.cs.uoregon.edu'

	# other handlers are set in shared.py
	mqtt_client.on_message = on_message

	mqtt_topic = 'cis650/somethingcool'

	mqtt_client.will_set(mqtt_topic, '______________Will of TURNSTILE _________________\n\n', 0, False)
	mqtt_client.connect(broker, '1883')
	mqtt_client.subscribe(mqtt_topic)
	mqtt_client.loop_start()

	while True:
		choice = raw_input("[TURNSTILE (%d)]: (p) for passenger, (q) to quit: " % turnstile.cur_passenger)
		if choice == 'p':
			if turnstile.state == State.WAITING_FOR_ACK:
				print "Turnstile is still waiting for acknowledgement of passenger #%d" % turnstile.cur_passenger
			elif turnstile.state == State.CAN_SEND:
				turnstile.cur_passenger = turnstile.cur_passenger + 1
				p = Passenger(turnstile.cur_passenger)
				timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
				mqtt_message = "[%s] %s TURNSTILE requests entry for passenger #%d" % (timestamp,ip_addr,p.id)
				mqtt_client.publish(mqtt_topic, mqtt_message)
				turnstile.state = State.WAITING_FOR_ACK	
			elif turnstile.state == State.PLATFORM_FULL:
				print "Platform is currently full, wait a while then try again"
		elif choice == 'q':
			exit_program()

# I have the loop_stop() in the control_c_handler above. A bit kludgey.
main()
