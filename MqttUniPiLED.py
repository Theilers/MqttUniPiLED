#!/usr/bin/env python
import paho.mqtt.client as mqtt
from jsonrpclib import Server
from thread import start_new_thread
import time

unipi=Server("http://127.0.0.1:8100/rpc")
kitchenDimVal = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("Unipi/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if "reduitlamp" in msg.topic:
        onoff=int(msg.payload)
        switchReduitLamp(onoff)
    if "kitchenlamp" in msg.topic:
        dimval=int(msg.payload)
        switchKitchenSpots(dimval)
        print("set dim val of ktichen to "+str(kitchenDimVal))


def switchKitchenSpots(dimValue):
    if (dimValue <= 0):
        unipi.relay_set(1,0)
        print("kitchen spots off")
    else:
        unipi.relay_set(1,1)
        if (dimValue > 100):
            dimValue = 100
        d = float(dimValue) / 10
        unipi.ao_set_value(1,d)
        print("set kitchen dim value to "+str(d)+" volt")

def switchReduitLamp(onOff):
    if (onOff > 0):
        unipi.relay_set(2,1)
        print("reduit lamp on")
    else:
        print("reduit lamp off")
        unipi.relay_set(2,0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
