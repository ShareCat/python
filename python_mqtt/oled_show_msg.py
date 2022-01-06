import paho.mqtt.client as mqtt
import time
import ssd1306 as oled
from PIL import ImageFont
import cv2 as cv

font_small = ImageFont.truetype('DejaVuSansMono.ttf', 10)
screen = oled.device(bus=0, width=64, height=32)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("device/oled")


def on_message(client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload, encoding='utf-8'))
    screen.clear()
    screen.draw.text((0, 0), str(msg.payload, encoding='utf-8'), font=font_small, fill=255)
    screen.update()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="oled", password="299792458")
client.connect(host="127.0.0.1", port=1883, keepalive=60)
client.loop_forever()
