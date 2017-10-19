import time
from shared import *


def on_message(client, userdata, msg):
  message = msg.payload
  print message

mqtt_client.on_message = on_message
mqtt_client.will_set(mqtt_topic, 'Monitor Down! Monitor Down!\n\n', 0, False)
mqtt_client.loop_start()

def main():
  while True:
    time.sleep(3)

if __name__ == "__main__": main()
