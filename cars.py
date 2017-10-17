from enum import Enum
import paho.mqtt.client as paho
import time

NUM_CARS = 1

class State(Enum):
  READY = 0
  RIDING_AND_BONDING = 1
  ARRIVE = 2
  FORM_SOCIAL_GROUP = 3

class Car:
  state = State.READY

  def advanceState(self):
    self.state = State((self.state.value + 1) % 4)
    print self.state.name

cars = []
for i in range(NUM_CARS):
  cars.append(Car())

def on_connect(client, userdata, flags, rc):
  print "Connected"

def on_message(client, userdata, msg):
  message = msg.payload
  print message
  if "PICKUP" in message :
    car.advanceState()
        
def on_disconnect(client, userdata, rc):
  print "Disconnected"

def on_log(client, userdata, level, buf):
        receivedLog = "log: {}".format(buf)
        print(receivedLog)

mqtt_client = paho.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log
mqtt_topic = 'cis650/somethingcool'
 
mqtt_client.will_set(mqtt_topic, 'These cars be messed up dawg!!!!\n\n', 0, False) 
broker = 'sansa.cs.uoregon.edu'  # Boyana's server 
mqtt_client.connect(broker, '1883') 
mqtt_client.subscribe('cis650/somethingcool') 
mqtt_client.loop_start()


def getVacantCar() :
  print "Searching a free car"
  for i in range(NUM_CARS):
    if(cars[i].status == READY):
      return i
  return (-1)

def main():
  print "I am here"
  while True:
    time.sleep(1)

if __name__ == "__main__": main()
