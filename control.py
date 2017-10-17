import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal
from enum import Enum

MY_NAME = 'Brian W' # change to your name
NUM_PASSENGERS = 3

class State(Enum):
	WAITING_FOR_PASSENGERS = 0
	WAITING_FOR_CAR = 1

class Control():
	state = State.WAITING_FOR_PASSENGERS
	passengers = 0

# Deal with control-c
def control_c_handler(signum, frame):
	#print('saw control-c')
	mqtt_client.disconnect()
	mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
	#print ("Now I am done.")
	sys.exit(0)

signal.signal(signal.SIGINT, control_c_handler)

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

control = Control()

def on_connect(client, userdata, flags, rc):
	print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
	#print(client)
	#print(userdata)
	print(msg.topic)
	print(msg.payload)
	i = msg.payload.find("requests passenger entry")
	if i > 0:
		if control.passengers < NUM_PASSENGERS:
			control.passengers = control.passengers + 1
			print("allow passenger, send ack")
		else:
			print("platform is full, reject")

	# Here is where you write to file and unsubscribe
	#with open("test.txt", "a+") as myfile:
		#if name not in myfile.read():
			#myfile.write(name+"\n")
		#myfile.close()

def on_disconnect(client, userdata, rc):
	print("Disconnected in a normal way")
	#graceful so won't send will

def on_log(client, userdata, level, buf):
	print("log: {}".format(buf)) # only semi-useful IMHO

def setup_client(client):
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_disconnect = on_disconnect
	client.on_log = on_log

def main():
	# Instantiate the MQTT client
	mqtt_client = paho.Client()

	setup_client(mqtt_client)
	mqtt_topic = 'cis650/somethingcool'

	mqtt_client.will_set(mqtt_topic, '______________Will of CONTROL_________________\n\n', 0, False)
	broker = 'sansa.cs.uoregon.edu'
	mqtt_client.connect(broker, '1883')

	# You can subscribe to more than one topic: https://pypi.python.org/pypi/paho-mqtt#subscribe-unsubscribe.
	# If you do list more than one topic, consdier using message_callback_add for each topic as described above.
	# For below, wild-card should do it.
	mqtt_client.subscribe('cis650/somethingcool')  # subscribe to all students in class

	mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

	while True:
		choice = raw_input("[CONTROL]: (r) request pickup (q) quit: ")

		# passenger arrive
		#if int(choice) == 1:
		#	if control.passengers == NUM_PASSENGERS:
		#		print("platform is full")
		#	else:
		#		control.passengers = controlpassengers + 1
		#		timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
		#		mqtt_message = "[%s] %s passenger arrived on platform (%d passengers waiting)" % (timestamp,ip_addr,control.passengers)
		#		mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
		#		print("add passenger")
		#elif int(choice) == 2:
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

