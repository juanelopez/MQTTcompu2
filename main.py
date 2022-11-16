#!/usr/bin/python3



import asyncio 
import argparse
import queue
import os
import multiprocessing as mp
import time

import mqtt
import webServer
import filesaver
import globales as glo
import multiproceso
import basedata

defaultTopic =["test/comp2/python","test/comp2/2022"]

def runserver(PORT,cantidad_lectura,directory):
    print("Start server")
    try:
        asyncio.run(webServer.webServer(PORT,cantidad_lectura,directory))
    except:
        print("Server no iniciado")
        exit(1)
def meterDatos(q):
    for i in range (0,10):
        q.put(i)

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
        
    #print(type(glo.query_mqtt))
    #Cola de mensajes mqtt multiproceso
    ctx = mp.get_context('spawn')
    multiprocq = ctx.Queue()
    
    
    print('I AM process id:', os.getpid())
    #proceso de creacion de base de datos
    p = ctx.Process(target=basedata.databaseStart, args=(multiprocq,))
    p.start()
    creacionDB = multiprocq.get()
    if(creacionDB == "No hay base de datos"):
        print("No hay DB, verificar")
    elif(creacionDB == "Configurado"):
        print("Base de datos lista")
    p.join()    
    #proceso que recibe por mqtt mensajes y los guarda en la base de datos
    p2 = ctx.Process(target=basedata.databasePUT, args=(multiprocq,))
    p2.start()    
    #meterDatos(multiprocq)
    #hilos para mqtt, servidor web de visualizacion y guardado en archivos    
    hilo_mqtt = glo.hilos.submit(mqtt.runmqtt,glo.query_mqtt,broker,topics,multiprocq,glo.query_coms) #hilo de monitor mqtt
    
    for sub in defaultTopic:
        subNew = glo.hilos.submit(mqtt.newSub,sub,glo.query_coms,glo.query_mqtt,multiprocq)
    #subNew = glo.hilos.submit(mqtt.newSub,"comp2/test/#",glo.query_coms,glo.query_mqtt,multiprocq)    
    hilo_server = glo.hilos.submit(runserver,PORT,cantidad_lectura,directory) #hilo de servidor web 
    hilo_guardado = glo.hilos.submit(filesaver.savemqtt,glo.query_mqtt,directory) #hilo guardado de mqtt    
    hilo_server.result()
    hilo_guardado.result()                
    hilo_mqtt.result()
    #subNew.result()
    p2.join()
#otro proceso que agregue hilos o procesos(mejor) con ipc en caliente
#escuchar en ipv4 y v6
#agregar base de datos con libreria mysql con docker