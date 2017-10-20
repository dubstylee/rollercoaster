from enum import Enum
import paho.mqtt.client as paho
import time
from shared import *
from random import *

class State(Enum):
  READY = 0
  RIDING_AND_BONDING = 1
  ARRIVE = 2
  FORM_SOCIAL_GROUP = 3

class Car:
  identifier = ''
  state = State.READY
  passengers = []
  led = None

  def advance_state(self):
    self.state = State((self.state.value + 1) % 4)
    send_message("Car %s : %s" %(self.identifier,self.state.name))

  def print_state(self):
    print "********** %s" %self.state.name

  def dispatch(self):
    send_message("Car %s dispatching" %self.identifier)
    while(True):
      self.advance_state()
      if(self.state == State.READY):
        self.led.write(ON)
        break
      else:
        i = 0
        while i < randint(10, 20):
          self.led.write(OFF)
          time.sleep(0.25)
          self.led.write(ON)
          time.sleep(0.25)
          i = i + 1
    send_message("Car %s is now vacant" % self.identifier)

car = Car()
dispatch = False

def control_c_handler(signum, frame):
  car.led.write(OFF)
  exit_program()
signal.signal(signal.SIGINT, control_c_handler)

def on_message(client, userdata, msg):
  global dispatch
  message = msg.payload
  if "PICKUP" in message and car.state == State.READY:
    splits = message.split(' ', 5)
    if(splits[4] == car.identifier): 
      send_message("CAR %s ACCEPT" % car.identifier)
      car.passengers = Passenger.list_from_string(splits[5])
      dispatch = True

mqtt_client.on_message = on_message
mqtt_client.will_set(mqtt_topic, "Will of Car %s\n\n" %car.identifier, 0, False)
mqtt_client.loop_start()

def main():
  if len(sys.argv) != 3:
    print "Invalid number of arguments"
    exit_program()
  identifier = sys.argv[1]
  lednum = int(sys.argv[2])
  car.identifier = identifier
  car.led = mraa.Gpio(lednum+1)
  car.led.dir(mraa.DIR_OUT)
  car.led.write(ON)
  global dispatch
  while True:
    if dispatch == True:
       car.dispatch()
       dispatch = False
    if car.state == State.READY:
      send_message("CAR %s READY" %car.identifier);
    time.sleep(3);

if __name__ == "__main__": main()
