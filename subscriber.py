import json
import queue
import threading
import time

import paho.mqtt.client as mqtt

from config import BROKER, PORT, TOPIC


stop = threading.Event()
msg_q = queue.Queue()


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected:", reason_code)
    client.subscribe(TOPIC)


def on_message(client, userdata, message):
    data = json.loads(message.payload)
    msg_q.put(data)
    print(data)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Shut down cleanly")