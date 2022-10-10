#!/usr/bin/python3
import random

from paho.mqtt import client as mqtt_client
import asyncio 
import os
import argparse
import queue
from concurrent import futures
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


def subscribe(client: mqtt_client,query_mqtt):
    def on_message(client, userdata, msg):        
        var = msg.payload.decode()
        query_mqtt.put(var)
        print(f"Received `{var}` from `{msg.topic}` topic")               
    client.subscribe(topic)
    client.on_message = on_message

def suball(client: mqtt_client,query_mqtt):
    def onmsg(client, userdata,msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(alltopic)
    client.on_message = onmsg
##########WEBSERVER############
async def handle(reader, writer):
    data = await reader.read(100)
    request_recibida = []
    request_recibida = data.split(b'\r\n')
    message = data.decode()
    addr = writer.get_extra_info('peername')
    #logger = asyncio.create_task(complementarias.mostrar_direccion(addr,directorio))
    #peticion = asyncio.create_task(devolver_peticion(request_recibida,writer,directorio,cantidad_lectura))
    #await logger
    #await peticion
    writer.close()
async def webServer():
    PORT = 5000
    server = await asyncio.start_server(lambda r,w: handle(r,w), ('::','0.0.0.0'),PORT)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')  
    async with server:
        await server.serve_forever()
def runmqtt(query_mqtt):
    print("START MQTT")
    client = connect_mqtt()
    subscribe(client,query_mqtt)
    suball(client,query_mqtt)    
    client.loop_forever()
    #asyncio.run(webServer())
def runserver():
    print("START SERVER")
    asyncio.run(webServer())
def savemqtt(query_mqtt):
    print("GUARDADO")
    while True:    
        print (query_mqtt.empty())
        while not query_mqtt.empty():
            print("LLEGA")
            msg = query_mqtt.get()
            print(msg)
if __name__ == '__main__':
    print("MAIN")
    query_mqtt = queue.Queue()
    
    hilos = futures.ThreadPoolExecutor()
    hilo_mqtt = hilos.submit(runmqtt,query_mqtt)
    hilo_server = hilos.submit(runserver)
    hilo_guardado = hilos.submit(savemqtt,query_mqtt)
    hilo_mqtt.result()
    hilo_server.result()
    hilo_guardado.result()
    
    #run()
