#!/usr/bin/python3
import random

from paho.mqtt import client as mqtt_client


broker = 'qrio.com.ar'
port = 1883
topic = "prod/#"
alltopic ="all/#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    
    client.on_message = on_message

def suball(client: mqtt_client):
    def onmsg(client, userdata,msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(alltopic)
    client.on_message = onmsg
def run():
    client = connect_mqtt()
    subscribe(client)
    suball(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
