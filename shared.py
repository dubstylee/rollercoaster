import time, socket, sys
import paho.mqtt.client as paho
import signal

mqtt_client = paho.Client()
print(mqtt_client)
print(type(mqtt_client))

def exit_program():
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
	sys.exit(0)

def control_c_handler(signum, frame):
	#print "saw control-c"
	#print "now I am done"
	exit_program()

def get_client():
	mqtt_client

signal.signal(signal.SIGINT, control_c_handler)

def on_connect(client, userdata, flags, rc):
	print "connected"

def on_disconnect(client, userdata, rc):
	print "disconnected in a normal way"

def on_log(client, userdata, level, buf):
	print "log: {}".format(buf)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log
