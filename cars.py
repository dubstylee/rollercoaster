from enum import Enum
import paho.mqtt.client as paho
import time,threading
from shared import *

NUM_CARS = 1

class State(Enum):
  READY = 0
  RIDING_AND_BONDING = 1
  ARRIVE = 2
  FORM_SOCIAL_GROUP = 3

class Car:
  identifier = 0;
  state = State.READY
  passangers = []

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
    print "Car %d " + self.identifier + " is now vacant"
      
cars = []
for i in range(NUM_CARS):
  car = Car()
  car.identifier = i+1
  cars.append(car)

def on_message(client, userdata, msg):
  message = msg.payload
  print message
  if "PICKUP" in message :
    #pessangers = getPessangers();
    car = getVacantCar();
    if(car != None):
      car.pessangers = pessangers
      mqtt_client.publish(mqtt_topic, "ACCEPT %s" % car.pessangers)
      #perform the dispatch on another thread
      thread = threading.Thread(target=car.dispatch())
      thread.start()
    else:
      mqtt_client.publish(mqtt_topic, "REJECT %s" % car.pessangers)

def on_log(client, userdata, level, buf):
        receivedLog = "log: {}".format(buf)
        print(receivedLog)

mqtt_client.on_message = on_message 
mqtt_client.will_set(mqtt_topic, 'These cars be messed up dawg!!!!\n\n', 0, False) 
qtt_client.loop_start()

def getVacantCar() :
  for car in cars:
    if(car.status == READY):
      return car
  return None
 
def main():
  while True:
    time.sleep(1)

if __name__ == "__main__": main()
