import time
import paho.mqtt.client as mqtt


BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "emre/telemetry/test"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Bağlandı:", reason_code)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()
time.sleep(1)
for i in range(5):
    mesaj = f"merhaba {i}"
    client.publish(TOPIC, mesaj)
    print("Gönderildi:", mesaj)
    time.sleep(1)

client.loop_stop()
client.disconnect()