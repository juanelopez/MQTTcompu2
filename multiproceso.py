import multiprocessing
import os
import mqtt 
import globales as glo
def startProcess(targetProc):#args es lista
    #argsProc = ["test/#","esp/#"]
    #argsProc = "test/#"
    argsProc = 0
    print("LLEGANDO")
    p1 = multiprocessing.Process(target=hola)
    p1.start()
    #p1.join()
    #return p1
def hola():
    #print("Estos son mis argumentos",argsProc)
    print("Este es mi pid",os.getpid())
    topic = "raspberry/#"
    nuevoTopic = glo.hilos.submit(mqtt.newSub,topic) #hilo de monitor mqtt
    nuevoTopic.result()