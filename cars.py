from enum import Enum
import paho.mqtt.client as paho
import time,threading
from shared import *

class State(Enum):
  READY = 0
  RIDING_AND_BONDING = 1
  ARRIVE = 2
  FORM_SOCIAL_GROUP = 3

class Car:
  identifier = ''
  state = State.READY
  passengers = []

  def advanceState(self):
    self.state = State((self.state.value + 1) % 4)
    print seld.identifier + " " + self.state.name

  def dispatch(self):
    while(True):
      self.advanceState()
      if(self.state == READY):
        break
      else:
        time.sleep(1)
    print "Car %s " + self.identifier + " is now vacant"

car = Car()
      
def on_message(client, userdata, msg):
  message = msg.payload
  print message
  if "PICKUP" in message and car.state == State.READY:
    splits = message.split(' ', 4)
    if(splits[2] == car.identifier): 
      send_message("ACCEPT %s" % car.identifier)
      car.passengers = Passanger.list_from_string();
      car.dispatch()

mqtt_client.on_message = on_message
mqtt_client.will_set(mqtt_topic, 'These cars be messed up dawg!!!!\n\n', 0, False)
mqtt_client.loop_start()

def main():
  identifier = sys.argv[1]
  car.identifier = identifier
  while True:
    if car.state == State.READY:
      send_message("READY %s" %car.identifier);
    time.sleep(3);

if __name__ == "__main__": main()
