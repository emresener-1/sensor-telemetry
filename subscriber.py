import json
import queue
import threading
import time
import csv
import os


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


def writer_loop():
    os.makedirs("data", exist_ok=True)
    files = {}
    writers = {}

    while not stop.is_set():
        try:
            msg = msg_q.get(timeout=1)
        except queue.Empty:
            continue
        
        sensor = msg["sensor"]

        if sensor not in writers:
            f = open(f"data/{sensor}.csv", "w", newline="")
            files[sensor] = f
            writers[sensor] = csv.writer(f)
            if sensor == "gps":
                writers[sensor].writerow(["t", "lat", "lon"])
            else:
                writers[sensor].writerow(["t", "value"])

        if sensor == "gps":
            lat, lon = msg["value"]
            writers[sensor].writerow([msg["t"], lat, lon])
        else:
            writers[sensor].writerow([msg["t"], msg["value"]])
        files[sensor].flush()
    
    for f in files.values():
        f.close()
    print("Writer stopped")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

writer_thread = threading.Thread(target=writer_loop)
writer_thread.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop.set()
    writer_thread.join()
    client.loop_stop()
    client.disconnect()
    print("Shut down cleanly")