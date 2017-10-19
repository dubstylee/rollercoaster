import time
from enum import Enum
from random import randint
from shared import *


# set up leds
leds = []
for i in range(2+PLATFORM_CAPACITY, 10):
	led = mraa.Gpio(i)
	led.dir(mraa.DIR_OUT)
	led.write(OFF)
	leds.append(led)
print "turnstile has %d leds" % len(leds)


class State(Enum):
	CAN_SEND = 0
	WAITING_FOR_ACK = 1


class Turnstile():
	state = State.CAN_SEND
	cur_passenger = 0
	timeout = 0

	def clear_lights(self):
		for led in leds:
			led.write(OFF)

	def send_passenger(self):
		self.clear_lights()
		send_message("TURNSTILE requests entry for passenger #%d" % self.cur_passenger)

		leds[-1].write(ON)
		for i in range(len(leds)-2, -1, -1):
			leds[i].write(ON)
			time.sleep(OVERLAP_DELAY)
			leds[i+1].write(OFF)
			time.sleep(WAIT_DELAY)
		time.sleep(OVERLAP_DELAY)
		leds[0].write(OFF)

turnstile = Turnstile()

def control_c_handler(signum, frame):
	turnstile.clear_lights()
	exit_program()

def on_message(client, userdata, msg):
	# we only listen for messages from CONTROL
	if "CONTROL" in msg.payload:
		print "MESSAGE FROM CONTROL %s" % msg.payload
		if turnstile.state == State.WAITING_FOR_ACK:
			if "allow passenger" in msg.payload:
				turnstile.state = State.CAN_SEND
			elif "platform is full" in msg.payload:
				time.sleep(TOTAL_DELAY*(7-PLATFORM_CAPACITY))
				for i in range(0, len(leds)-1):
					leds[i+1].write(ON)
					time.sleep(OVERLAP_DELAY)
					leds[i].write(OFF)
					time.sleep(WAIT_DELAY)				
				leds[-1].write(OFF)

def run_auto():
	while True:
		time.sleep(randint(2,10))
		if turnstile.state == State.CAN_SEND:
			turnstile.cur_passenger = turnstile.cur_passenger + 1
			turnstile.state = State.WAITING_FOR_ACK
		turnstile.send_passenger()
		#send_message("TURNSTILE requests entry for passenger #%d" % turnstile.cur_passenger)

def run_manually():
	while True:
		choice = raw_input("[TURNSTILE (%d)]: (p) for passenger, (q) to quit: " % turnstile.cur_passenger)
		if choice == 'p':
			# if we have not received acknowledgement of cur_passenger, just re-send same passenger
			if turnstile.state == State.CAN_SEND:
				turnstile.cur_passenger = turnstile.cur_passenger + 1
				turnstile.state = State.WAITING_FOR_ACK
			turnstile.send_passenger()
		elif choice == 'q':
			turnstile.clear_lights()
			exit_program()


def main():
	if len(sys.argv) != 2:
		print "Usage: turnstile (auto|manual)"
		exit_program()
	else:
		mqtt_client.will_set(mqtt_topic, '___Will of TURNSTILE___', 0, False)
		mqtt_client.on_message = on_message
		mqtt_client.loop_start()

		if sys.argv[1] == "auto":
			run_auto()
		elif sys.argv[1] == "manual":
			run_manually()
		else:
			exit_program()


if __name__ == '__main__': main()
