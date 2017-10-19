import time
from enum import Enum
from shared import *


class State(Enum):
	WAITING_FOR_PASSENGERS = 0
	WAITING_FOR_CAR = 1


class Control():
	state = State.WAITING_FOR_PASSENGERS
	passengers = []
	cars = Queue()
	timeout = 0

	def request_pickup(self):
		if self.cars.count() > 0:
			send_message("PICKUP %s %s" % (self.cars.get(), self.passengers))


control = Control()


def on_message(client, userdata, msg):
	if "TURNSTILE" in msg.payload:
		print "MESSAGE FROM TURNSTILE %s" % msg.payload
		splits = str.split(msg.payload, " ")
		if splits[4] == "requests" and splits[5] == "entry":
			pid = splits[8][1:]
			p = Passenger(int(pid))

			if len(control.passengers) < PLATFORM_CAPACITY:
				control.passengers.append(p)
				send_message("CONTROL allow passenger #%d" % p.id)

				if len(control.passengers) == CAR_CAPACITY:
					control.state = State.WAITING_FOR_CAR
					control.request_pickup()
			else:
				send_message("CONTROL platform is full")

	elif "CAR" in msg.payload:
		print "MESSAGE FROM CAR %s" % msg.payload
		splits = str.split(msg.payload, " ")
		if splits[5] == "READY":
			control.cars.put_distinct(splits[4])
		elif splits[5] == "ACCEPT":
			control.timeout = 0
			control.state = State.WAITING_FOR_PASSENGERS
			del control.passengers[:]

def main():
	mqtt_client.will_set(mqtt_topic, '___Will of CONTROL___', 0, False)
	mqtt_client.on_message = on_message
	mqtt_client.loop_start()

	while True:
		if control.state == State.WAITING_FOR_CAR:
			time.sleep(0.5)
			control.timeout = control.timeout + 1
			if control.timeout > 20:
				send_message("CONTROL timeout, requesting another car")
				control.request_pickup()
				control.timeout = 0
		else:
			print "CARs ready: %s" % control.cars.items
			time.sleep(3)


if __name__ == '__main__': main()
