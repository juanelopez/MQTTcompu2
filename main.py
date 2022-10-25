#!/usr/bin/python3
import random

from paho.mqtt import client as mqtt_client
import asyncio 
import os
import argparse
import queue
from concurrent import futures
import datetime


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
        query_mqtt.put(str(var))
        query_mqtt.put(str(msg.topic))
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
    peticion = asyncio.create_task(devolver_peticion(request_recibida,writer))
    #await logger
    await peticion
    writer.close()


async def devolver_peticion(request_recibida,writer):
    directorio = "/"
    cantidad_lectura = 1024
    dividir_request = request_recibida[0].decode().split(" ")
    metodo = dividir_request[0]
    archivo = dividir_request[1]
    if(directorio == "/"):
    	directorio = ""
    '''
    if(archivo != "/"):
        archivo_dividido = []
        archivo_dividido = archivo[1:].split(".")
        dividir_500_extension = []
        dividir_500_extension = archivo_dividido[1].split('?')
        if(len(archivo_dividido) == 2):
            extension = archivo_dividido[1]
        else:
            extension = " "
        print(archivo)
    '''
    if (archivo == "/"):
        archivo = "/index.html"
        extension = "html"
        dividir_500_extension = ["html"]    
    else:
        #print("ESTO")
        #print(archivo)
        extension = "txt"        
        dividir_500_extension = ["txt"]
    version = str.encode(dividir_request[2])    
    if(len(dividir_500_extension) > 1):
        enviar_500 = version + b' 500 Internal Server Error\n'
        writer.write(enviar_500)
    else:
        if(metodo == "POST"):
            enviar_500 = version + b' 500 Internal Server Error\n'
            writer.write(enviar_500)
        elif(metodo == "GET"):
            try:
                if(archivo == "/index.html"):
                    
                    print("Pantalla de inicio")
                    request = version+b' 200 OK\n'
                    content_type = "Content-Type: text/"+extension+"\n"
                    request_lenght = b'Content-Lenght:20000\n\n'
                    writer.write(request)
                    writer.write(bytes(content_type,'utf-8'))
                    writer.write(request_lenght)
                    writer.write(bytes("<HTML><HEAD><TITLE>Pantalla de inicio</TITLE></HEAD><BODY>",'utf-8'))
                    #writer.write(bytes("<P>Hola Compu2</P>",'utf-8'))
                    for path in os.scandir():
                        if(path.is_file()):                            
                            #print(path.name)
                            #print(path)
                            link = '<a href="'+path.name+'"''</a>'+path.name+"<br>"                            
                            writer.write(bytes(link,'utf-8'))
                    writer.write(bytes("<a href='hola'>hola</a>",'utf-8'))
                    writer.write(bytes("</BODY></HTML>",'utf-8'))
                else:
                    fd1 = os.open(archivo[1:],os.O_RDONLY)
                    request = version+b' 200 OK\n'
                    content_type = "Content-Type: text/plain\n"
                    request_lenght = b'Content-Lenght:20000\n\n'
                    writer.write(request)
                    writer.write(bytes(content_type,'utf-8'))
                    writer.write(request_lenght)             
                    lectura = os.read(fd1,cantidad_lectura)
                    while(lectura != b''):
                        writer.write(lectura)
                        lectura = os.read(fd1,cantidad_lectura)
                    os.close(fd1)
                '''
                fd1 = os.open(directorio+archivo[1:],os.O_RDONLY)
                request = version+b' 200 OK\n'
                content_type = "Content-Type: text/"+extension+"\n"
                request_lenght = b'Content-Lenght:20000\n\n'
                writer.write(request)
                writer.write(bytes(content_type,'utf-8'))
                writer.write(request_lenght)             
                lectura = os.read(fd1,cantidad_lectura)
                while(lectura != b''):
                    writer.write(lectura)
                    lectura = os.read(fd1,cantidad_lectura)
                os.close(fd1)
                writer.write("HOLA")                                
                '''
                '''
                fecha = datetime.date.today()
                fd1 = os.open(str(fecha),os.O_RDONLY)
                request = version+b' 200 OK\n'
                content_type = "Content-Type: text/plain\n"
                request_lenght = b'Content-Lenght:20000\n\n'
                writer.write(request)
                writer.write(bytes(content_type,'utf-8'))
                writer.write(request_lenght)  
                lectura = os.read(fd1,cantidad_lectura)
                while(lectura != b''):
                    writer.write(lectura)
                    lectura = os.read(fd1,cantidad_lectura)
                os.close(fd1)               
                '''

            except:
                print("El archivo no existe")				
                request = version +b' 404 Not Found\n'
                writer.write(request)
    await writer.drain()






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
    #suball(client,query_mqtt)    
    client.loop_forever()
def runserver():
    print("START SERVER")
    asyncio.run(webServer())
def savemqtt(query_mqtt):
    print("GUARDADO")
    fecha = datetime.date.today()  
    fdmqtt = os.open(str(fecha),os.O_CREAT|os.O_WRONLY|os.O_APPEND)
    while True:    
        #print (query_mqtt.empty())
        while not query_mqtt.empty():
            #print("LLEGA")
            
            msg = query_mqtt.get()
            msg = msg+'\n'
            hora = datetime.datetime.now().time()
            hora = str(hora)
            os.write(fdmqtt,bytes(hora,'utf-8'))
            os.write(fdmqtt,b' - ')
            os.write(fdmqtt,bytes(msg,'utf-8'))                 
            
            #os.close(fdmqtt)
            print(msg)
            if(fecha != datetime.date.today()):
                os.write(fdmqtt,b'final del dia')
                os.close(fdmqtt)                
                fecha = datetime.date.today()
                fdmqtt = os.open(str(fecha),os.O_CREAT|os.O_WRONLY|os.O_APPEND)        

def uploadlogger():
    print("subiendo a drive")

def pruebaqueue(query_mqtt):    
    print("para enviar")    
    for i in range(10):
        #query_mqtt.put(i)      
        topico ="prod/test"+str(i)+"\n"
        query_mqtt.put(topico)    
        query_mqtt.put('{"estadisticas":true}\n')                
        #topico = "prod/test"
if __name__ == '__main__':
    print("MAIN")
    #print(datetime.datetime.now().time())
    
    query_mqtt = queue.Queue()    
    hilos = futures.ThreadPoolExecutor()
    hilo_mqtt = hilos.submit(runmqtt,query_mqtt) #hilo de monitor mqtt
    hilo_server = hilos.submit(runserver) #hilo de servidor web 
    hilo_guardado = hilos.submit(savemqtt,query_mqtt) #hilo guardado de mqtt
    #hilo_prueba_queue = hilos.submit(pruebaqueue,query_mqtt)
    hilo_mqtt.result()
    hilo_server.result()
    hilo_guardado.result()
    #hilo_prueba_queue.result()
    
    #run()
