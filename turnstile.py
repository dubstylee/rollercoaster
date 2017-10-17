import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal
from enum import Enum

MY_NAME = 'Brian W' # change to your name

class State(Enum):
	CAN_SEND = 0
	WAITING_FOR_ACK = 1
	PLATFORM_FULL = 2

class Turnstile():
	state = State.CAN_SEND

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

def on_connect(client, userdata, flags, rc):
	print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
	#print('on_message')
	#print(client)
	#print(userdata)
	print(msg.topic)
	print(msg.payload)
	#i = msg.payload.find("====")
	#name = msg.payload[i+5:]
	# Here is where you write to file and unsubscribe
	#with open("test.txt", "a+") as myfile:
		#if name not in myfile.read():
			#myfile.write(name+"\n")
		#myfile.close()

def on_disconnect(client, userdata, rc):
	print("Disconnected in a normal way")

def on_log(client, userdata, level, buf):
	print("log: {}".format(buf)) # only semi-useful IMHO

def main():
	# Instantiate the MQTT client
	mqtt_client = paho.Client()
	turnstile = Turnstile()

	# set up handlers
	mqtt_client.on_connect = on_connect
	mqtt_client.on_message = on_message
	mqtt_client.on_disconnect = on_disconnect
	mqtt_client.on_log = on_log

	mqtt_topic = 'cis650/somethingcool'

	# See https://pypi.python.org/pypi/paho-mqtt#option-functions.
	mqtt_client.will_set(mqtt_topic, '______________Will of TURNSTILE _________________\n\n', 0, False)

	broker = 'sansa.cs.uoregon.edu'
	mqtt_client.connect(broker, '1883')

	mqtt_client.subscribe('cis650/somethingcool')
	mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

	while True:
		choice = raw_input("[TURNSTILE]: (p) for passenger, (q) to quit: ")
		if choice == 'p':
			timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
			mqtt_message = "[%s] %s TURNSTILE requests passenger entry" % (timestamp,ip_addr)
			mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
			turnstile.state = State.WAITING_FOR_ACK	
		elif choice == 'q':
			print("close down the shop")

# I have the loop_stop() in the control_c_handler above. A bit kludgey.
main()
