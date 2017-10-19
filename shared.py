import time, socket, sys
import paho.mqtt.client as paho
import signal
import mraa
from datetime import datetime as dt


CAR_CAPACITY 	= 3
PLATFORM_CAPACITY = 3
OVERLAP_DELAY 	= 0.03
WAIT_DELAY 	= 0.1
TOTAL_DELAY 	= WAIT_DELAY + OVERLAP_DELAY

# for leds
ON 	= 0
OFF 	= 1


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
s.close()

broker = 'sansa.cs.uoregon.edu'
mqtt_topic = 'cis650/somethingcool'
mqtt_client = paho.Client()
mqtt_client.connect(broker, '1883') 
mqtt_client.subscribe(mqtt_topic)


def exit_program():
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
	sys.exit(0)


def control_c_handler(signum, frame):
	print "using shared ctrl-c handler"
	exit_program()


signal.signal(signal.SIGINT, control_c_handler)


def on_connect(client, userdata, flags, rc):
	print "connected"


def on_disconnect(client, userdata, rc):
	print "disconnected in a normal way"


def on_log(client, userdata, level, buf):
	print "log: {}".format(buf)


def send_message(message):
	timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
	mqtt_client.publish(mqtt_topic, "[%s] %s %s" % (timestamp, ip_addr, message))


mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
#mqtt_client.on_log = on_log


class Passenger():
	id = 0

	def __init__(self, id):
		self.id = id

	def __repr__(self):
		return "Passenger #%d" % self.id

	@staticmethod
	def from_string(text):
		if "Passenger" in text:
			pid = int(text[11:])
			print pid
			return Passenger(pid)

	@staticmethod
	def list_from_string(text):
		passengers = []
		text = text[1:-1]
		split_text = str.split(text, ",")
		for p in split_text:
			p = p.strip()
			passengers.append(Passenger.from_string(p))
		return passengers


class Queue:
	def __init__(self):
		self.items = []

	def is_empty(self):
		return self.items == []

	def put(self, item):
		self.items.insert(0, item)

	def put_distinct(self, item):
		if item not in self.items:
			self.items.insert(0, item)

	def get(self):
		return self.items.pop()

	def count(self):
		return len(self.items)
