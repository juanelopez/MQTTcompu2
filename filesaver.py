import os
import datetime

def savemqtt(query_mqtt,directory):
    print("Start file logger")
    fecha = datetime.date.today()  
    if(directory != ''):
        file_open = directory+'/'+str(fecha)
    fdmqtt = os.open(str(file_open),os.O_CREAT|os.O_WRONLY|os.O_APPEND)
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
                if(directory != ''):
                    file_open = directory+'/'+str(fecha)
                fdmqtt = os.open(str(file_open),os.O_CREAT|os.O_WRONLY|os.O_APPEND)        
