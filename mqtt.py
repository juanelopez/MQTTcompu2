from paho.mqtt import client as mqtt_client
import random
import globales as glo
import queue
port = 1883
client = None
client_id = f'python-mqtt-{random.randint(0, 100)}'
def connect_mqtt(broker) -> mqtt_client:
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
def subscribe(client: mqtt_client,query_mqtt,topic):
    def on_message(username,password,msg):        
        query_mqtt.put(str(msg.topic))
        query_mqtt.put(str(msg.payload.decode()))        
        print(f"Mensaje `{msg.payload.decode()}` de `{msg.topic}` topic")               
    client.subscribe(topic)
    print("TOPIC SUB = ",topic)
    client.on_message = on_message
def runmqtt(query_mqtt,broker,topic):
    print("START MQTT")
    client = connect_mqtt(broker)  
    print("Cliente es",client)  
    for sub in topic:        
        glo.hilos.submit(subscribe,client,query_mqtt,sub) #creando un hilo por topic
    client.loop_forever()
def newSub(topic):
    print("Agregando topic: ",topic)
    topic = "raspberry/#"
    while True:
        if(client != 0):
            print("Nuevo topic iniciado")
            #glo.hilos.submit(subscribe,client,glo.query_mqtt,topic)
            #client.on_message = on_message            
            break
        else:
            #print("Todavia no inicia el broker")
            pass