#!/usr/bin/python3
import asyncio 
import argparse
import multiprocessing as mp
import mqtt
import webServer
import filesaver
import globales as glo
import basedata

defaultTopic =["test/comp2/python","test/comp2/2022"] #topics default a los cuales se subscribe posteriormente

def runserver(PORT,cantidad_lectura,directory):
    print("Start server")
    try:
        asyncio.run(webServer.webServer(PORT,cantidad_lectura,directory))
    except:
        print("Server no iniciado")
        exit(1)

if __name__ == '__main__':
    #print("MAIN")
    parser = argparse.ArgumentParser(description='Final computacion 2')
    parser.add_argument('-s', '--size',action="store", type= int, default=1024, help="Bloque de lectura máxima para los documentos")
    parser.add_argument('-d', '--directory',action="store", dest="file_dir", default="/", type=str, help="Directorio para guardar")
    parser.add_argument('-p', '--port',action="store", dest="port", required=True, type=int, help="Puerto en donde espera conexiones nuevas")
    parser.add_argument('-b','--b',action="store",dest = "broker",required= True,type=str , help = "Broker al cual se quiere conectar")    
    parser.add_argument('-u', '--userdb',action="store", dest="userdb", required=True,default="", type=str, help="Usuario de base de datos")
    parser.add_argument('-ps', '--passdb',action="store", dest="passdb", required=True,default="", type=str, help="Password base de datos")
    parser.add_argument('-db', '--database',action="store", dest="database", required=True,default="", type=str, help="Database a conectar/crear")
    parser.add_argument('-pdb', '--portdb',action="store", dest="portdb", required=True, type=int, help="Puerto en esta la base de datos")
    parser.add_argument('-l','--list', action='append', dest = "topic",type=str, required=True, help="todos los topics que deben guardarse usar -l 'topic/#' -l 'topic2/topicn'")    
    args = parser.parse_args()
    PORT = args.port #puerto de servidor web
    cantidad_lectura = args.size
    topics = args.topic #topics que se subscriben al principio
    broker = args.broker #broker que se define
    directory = args.file_dir #directorio donde se guardan los archivos de log
    userdb = args.userdb
    passdb = args.passdb
    database = args.database
    portdb = args.portdb
    #Cola de mensajes mqtt multiproceso
    ctx = mp.get_context('spawn')
    multiprocq = ctx.Queue()
        
    #proceso de configuracion base de datos
    configDB = ctx.Process(target=basedata.databaseStart, args=(multiprocq,userdb,passdb,database,portdb,))
    configDB.start()
    creacionDB = multiprocq.get()
    if(creacionDB == "No hay base de datos"):
        print("No hay DB, verificar")
    elif(creacionDB == "Configurado"):
        print("Base de datos lista")
    configDB.join()    

    #proceso que recibe por mqtt mensajes y los guarda en la base de datos
    saveDB = ctx.Process(target=basedata.databasePUT, args=(multiprocq,userdb,passdb,database,portdb,))
    saveDB.start()    

    #hilos para mqtt, servidor web de visualizacion y guardado en archivos    
    hilo_mqtt = glo.hilos.submit(mqtt.runmqtt,glo.query_mqtt,broker,topics,multiprocq,glo.query_coms) #hilo de monitor mqtt    
    for sub in defaultTopic: #Subscripciones mientras se esta conectado al broker
        subNew = glo.hilos.submit(mqtt.newSub,sub,glo.query_coms,glo.query_mqtt,multiprocq)    
    hilo_server = glo.hilos.submit(runserver,PORT,cantidad_lectura,directory) #hilo de servidor web 
    hilo_guardado = glo.hilos.submit(filesaver.savemqtt,glo.query_mqtt,directory) #hilo guardado de mqtt    
    hilo_server.result()
    hilo_guardado.result()                
    hilo_mqtt.result()    
    subNew.result()    
    saveDB.join()
    
    