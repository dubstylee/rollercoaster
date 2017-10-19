from enum import Enum
import paho.mqtt.client as paho
import time,threading
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

  def advance_state(self):
    self.state = State((self.state.value + 1) % 4)
    print self.identifier + " " + self.state.name

  def print_state(self):
    print "********** %s" %self.state.name

  def dispatch(self):
    print "Car Dispatching"
    while(True):
      self.advance_state()
      #self.print_state()
      if(self.state == State.READY):
        break
      else:
        time.sleep(randint(1, 10))
    print "Car %s is now vacant" % self.identifier

car = Car()
      
def on_message(client, userdata, msg):
  message = msg.payload
  if "PICKUP" in message:
    splits = message.split(' ', 5)
    if(splits[4] == car.identifier): 
      send_message("CAR %s ACCEPT" % car.identifier)
      car.passengers = Passenger.list_from_string(splits[5])
      target=car.dispatch()

mqtt_client.on_message = on_message
mqtt_client.will_set(mqtt_topic, 'These cars be messed up dawg!!!!\n\n', 0, False)
mqtt_client.loop_start()

def main():
  identifier = sys.argv[1]
  car.identifier = identifier
  while True:
    if car.state == State.READY:
      send_message("CAR %s READY" %car.identifier);
    time.sleep(3);

if __name__ == "__main__": main()
