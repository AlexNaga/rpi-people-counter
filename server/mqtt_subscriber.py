import paho.mqtt.client as mqtt
import datetime

# Config the area to receive data from
physical_area = "lnu/campus"


# MQTT handlers
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(physical_area + "/+")


def on_message(client, userdata, msg):
    print(str(datetime.datetime.now()) + ": " +
          msg.topic + " " + str(msg.payload))


# Config the MQTT client
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the MQTT broker
mqtt_server = "192.168.10.235"
mqtt_port = 1883
mqttc.connect(mqtt_server, mqtt_port)

mqttc.loop_forever()
