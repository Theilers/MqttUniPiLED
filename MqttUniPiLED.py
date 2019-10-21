#!/usr/bin/python
import paho.mqtt.client as mqtt
from jsonrpclib import Server
from thread import start_new_thread
import time

LastDimValue = 50
print("Start Mqtt Unipi LED")
unipi=Server("http://127.0.0.1:8100/rpc")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("Unipi/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if "reduitlamp" in msg.topic:
        onoff = 0
        if "ON" in msg.payload:
            onoff = 1
        elif "on" in msg.payload:
            onoff = 1
        elif "OFF" in msg.payload:
            onoff = 0
        elif "off" in msg.payload:
            onoff = 0
        else:
            onoff=int(msg.payload)
        switchReduitLamp(onoff)
    if "kitchenlamp" in msg.topic:
        dimval = 0
        print("evaluate kitchenlamp value")
        global LastDimValue
        if "ON" in msg.payload:
            print("received ON cmd for kitchenlamp")
            dimval = LastDimValue
        elif "on" in msg.payload:
            print("received ON cmd for kitchenlamp")
            dimval = LastDimValue
        elif "off" in msg.payload:
            print("received OFF cmd for kitchenlamp")
            dimval = 0
        elif "OFF" in msg.payload:
            print("received OFF cmd for kitchenlamp")
            dimval = 0
        else:
            print("set dimvalue for kitchenlamp (and turn on if necessary")
            dimval=int(msg.payload)
            LastDimValue = dimval
        print("set now dim value of kitchen: "+str(dimval))
        switchKitchenSpots(dimval)


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

switchKitchenSpots(0)
time.sleep(0.5)
switchKitchenSpots(50)
time.sleep(0.5)
switchKitchenSpots(100)
time.sleep(0.5)
switchKitchenSpots(0)

client.loop_forever()
