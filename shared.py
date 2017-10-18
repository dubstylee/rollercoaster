import time, socket, sys
import paho.mqtt.client as paho
import signal

mqtt_client = paho.Client()

def exit_program():
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
	sys.exit(0)

def control_c_handler(signum, frame):
	#print "saw control-c"
	#print "now I am done"
	exit_program()

signal.signal(signal.SIGINT, control_c_handler)

def on_connect(client, userdata, flags, rc):
	print "connected"

def on_disconnect(client, userdata, rc):
	print "disconnected in a normal way"

def on_log(client, userdata, level, buf):
	print "log: {}".format(buif)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log

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


#test = []
#test.append(Passenger(3))
#test.append(Passenger(5))
#test.append(Passenger(121))

#text = str(test)
#print(text)

#new_test = Passenger.list_from_string(text)

#print(new_test)