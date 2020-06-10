import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
import serial

t = np.arange(0, 100)
delta = np.zeros((100))



# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client


# MQTT broker hosted on local machine

mqttc = paho.Client()

#setting array
sample_num = 20
t = np.arange(0, sample_num)
gravity = np.zeros((sample_num, 3))
gtime = np.zeros((sample_num))
tilt = np.zeros(sample_num)


# Settings for connection

host = "10.0.2.15"

topic = "Mbed"

i = 0

j = 0

# Callbacks

def draw() :
      print('dick')
      fig, ax = plt.subplots(2, 1)
      print('dick')
      ax[0].plot(gtime, gravity)
      print('dick')
      ax[1].plot(t, tilt, 'bo') 
      print('dick')
      plt.show()
      print('dick')

def on_connect(self, mosq, obj, rc):

      print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):
      global i
      global j

      if(j < 3):
            gravity[i][j] = float(msg.payload)
            print((gravity[i][j]))
            j = j + 1
      elif(j == 3):
            gtime[i] = float(msg.payload)
            j = j + 1
      else:
            tilt[i] = float(msg.payload)
            print(tilt[i])
            print("----------")
            j = 0
            i = i + 1
      if i == sample_num :
            print('dick')
            draw()

      


def on_subscribe(mosq, obj, mid, granted_qos):

      print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

      print("Unsubscribed OK")


# Set callbacks

mqttc.on_message = on_message

mqttc.on_connect = on_connect

mqttc.on_subscribe = on_subscribe

mqttc.on_unsubscribe = on_unsubscribe


# Connect and subscribe

print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=1883, keepalive=60)

mqttc.subscribe(topic, 0)


# Publish messages from Python

num = 0

while num != 5:

      ret = mqttc.publish(topic, "Message from Python!\n", qos=0)

      if (ret[0] != 0):

            print("Publish failed")

      mqttc.loop()

      time.sleep(1.5)

      num += 1


# Loop forever, receiving messages

mqttc.loop_forever()