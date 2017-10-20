import time
from shared import *

messages = open("messagelogs", "a+")

def on_message(client, userdata, msg):
  message = msg.payload
  messages.write(message + "\n")

def control_c_handler(signum, frame):
  messages.close()
  exit_program()
signal.signal(signal.SIGINT, control_c_handler)

mqtt_client.on_message = on_message
mqtt_client.will_set(mqtt_topic, 'Will of Monitor\n\n', 0, False)
mqtt_client.loop_start()

def main():
  while True:
    time.sleep(3)

if __name__ == "__main__": main()
