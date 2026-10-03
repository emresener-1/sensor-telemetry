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
msg_count = 0
count_lock = threading.Lock()


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected:", reason_code)
    client.subscribe(TOPIC)


def on_disconnect(client, userdata, flags, reason_code, properties):
    print("Disconnected:", reason_code)


def on_message(client, userdata, message):
    global msg_count
    with count_lock:
        msg_count += 1
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
client.on_disconnect = on_disconnect
client.reconnect_delay_set(min_delay=1, max_delay=30)
client.connect(BROKER, PORT)
client.loop_start()

writer_thread = threading.Thread(target=writer_loop)
writer_thread.start()


try:
    while True:
        time.sleep(1)
        with count_lock:
            n = msg_count
            msg_count = 0
        print(f"{n} msg/s")
except KeyboardInterrupt:
    stop.set()
    writer_thread.join()
    client.loop_stop()
    client.disconnect()
    print("Shut down cleanly")