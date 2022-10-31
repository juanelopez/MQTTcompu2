#!/usr/bin/python3



import asyncio 
import argparse
import queue
import mqtt
import webServer
import filesaver
import globales as glo
import os

def runserver(PORT,cantidad_lectura,directory):
    print("Start server")
    try:
        asyncio.run(webServer.webServer(PORT,cantidad_lectura,directory))
    except:
        print("Server no iniciado")
def uploadlogger():
    print("subiendo a drive")

if __name__ == '__main__':
    #print("MAIN")
    parser = argparse.ArgumentParser(description='Final computacion 2')
    parser.add_argument('-s', '--size',action="store", type= int, default=1024, help="Bloque de lectura máxima para los documentos")
    parser.add_argument('-d', '--directory',action="store", dest="file_dir", default="/", type=str, help="Directorio para guardar")
    parser.add_argument('-p', '--port',action="store", dest="port", required=True, type=int, help="Puerto en donde espera conexiones nuevas")
    parser.add_argument('-b','--b',action="store",dest = "broker",required= True,type=str , help = "Broker al cual se quiere conectar")    
    parser.add_argument('-l','--list', action='append', dest = "topic",type=str, required=True, help="todos los topics que deben guardarse usar -l 'topic/#' -l 'topic2/topicn'")    
    args = parser.parse_args()
    PORT = args.port
    cantidad_lectura = args.size
    topics = args.topic
    broker = args.broker
    directory = args.file_dir
    query_mqtt = queue.Queue()    
    #hilos
        
    hilo_mqtt = glo.hilos.submit(mqtt.runmqtt,query_mqtt,broker,topics) #hilo de monitor mqtt
    hilo_server = glo.hilos.submit(runserver,PORT,cantidad_lectura,directory) #hilo de servidor web 
    hilo_guardado = glo.hilos.submit(filesaver.savemqtt,query_mqtt,directory) #hilo guardado de mqtt    
    hilo_mqtt.result()
    hilo_server.result()
    hilo_guardado.result()            
    
