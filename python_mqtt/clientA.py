import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("chat/B_msg")


def on_message(client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))
    time.sleep(3)
    client.publish("chat/A_msg", "I'm fine thank you!", 2)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="admin", password="299792458")
client.connect(host="127.0.0.1", port=1883, keepalive=60)

client.loop_start()

while True:
    pass
