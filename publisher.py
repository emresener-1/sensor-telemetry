import json
import queue
import threading
import time

import paho.mqtt.client as mqtt

from sensors import BikeSimulator


BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "emre/telemetry/bike"


stop = threading.Event()
data_q = queue.Queue()
bike = BikeSimulator()


def sensor_loop(name, hz, read_fn):
    while not stop.is_set():
        data_q.put({"sensor": name, "t": time.time(), "value": read_fn()})
        stop.wait(1 / hz)


def publisher_loop(client):
    while not stop.is_set():
        try:
            msg = data_q.get(timeout=1)
        except queue.Empty:
            continue
        client.publish(TOPIC, json.dumps(msg))
        print(msg)


def on_connect(client, userdata, flags, reason_code, properties):
    print("Bağlandı:", reason_code)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()


sensors = [
    ("power", 10, bike.read_power),
    ("hr", 1, bike.read_hr),
    ("cadence", 1, bike.read_cadence),
    ("speed", 1, bike.read_speed),
    ("gps", 1, bike.read_gps),
]

threads = []
for name, hz, read_fn in sensors:
    t = threading.Thread(target=sensor_loop, args=(name, hz, read_fn))
    threads.append(t)
threads.append(threading.Thread(target=publisher_loop, args=(client,)))


for t in threads:
    t.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop.set()
    for t in threads:
        t.join()
    client.loop_stop()
    client.disconnect()
    print("Program Temiz Kapandı")