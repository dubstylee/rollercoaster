import time, socket, sys
from datetime import datetime as dt
#import paho.mqtt.client as paho
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
	passengers = 0

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
	print(msg.topic)
	print(msg.payload)
	i = msg.payload.find("CONTROL")
	if i > 0:
		if "allow passenger" in msg.payload:
			turnstile.passengers = turnstile.passengers + 1
		elif "platform is full" in msg.payload:
			print("platform is full, try again later")

	#i = msg.payload.find("====")
	#name = msg.payload[i+5:]
	# Here is where you write to file and unsubscribe
	#with open("test.txt", "a+") as myfile:
		#if name not in myfile.read():
			#myfile.write(name+"\n")
		#myfile.close()

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
		choice = raw_input("[TURNSTILE (%d sent)]: (p) for passenger, (q) to quit: " % turnstile.passengers)
		if choice == 'p':
			timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
			mqtt_message = "[%s] %s TURNSTILE requests passenger entry" % (timestamp,ip_addr)
			mqtt_client.publish(mqtt_topic, mqtt_message)
			turnstile.state = State.WAITING_FOR_ACK	
		elif choice == 'q':
			exit_program()

# I have the loop_stop() in the control_c_handler above. A bit kludgey.
main()
