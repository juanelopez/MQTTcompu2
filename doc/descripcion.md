# En este proyecto mi objetivo es armar un logger mqtt. 

- El protocolo de comunicacion mqtt es usado por muchos dispositivos de IoT para comunicaciones haciendo uso de un "broker" el cual es el punto medio entre ellos, un servidor tambien puede comunicarse con los dispositivos por este protocolo. Es un protocolo con menor consumo de bytes que http.

- Los mensajes entre dispositivos, a menos que se tenga acceso a este broker, no pueden ser guardadas facilmente por largo tiempo . Este programa desarrollado en python lo que realiza es conectarse a un broker como otro dispositivo siendo capaz de recibir los mensajes enviados en los topics a los cuales esta subscripto y guardarlos en archivos de texto y base de datos para posteriormente poder revisarlos. 

- La escucha de mensajes mqtt se hace con hilos, uno por cada topic que se subscribe y luego de iniciar el logueo se subscriben 2 topics por default("test/comp2/python" y "test/comp2/2022") en otros hilos. Cada uno de los topics que se realiza la subscripcion son ingresados como parametro al iniciar el programa ("-l topic/topic o -l topic/#). El broker al cual se realiza la subscripcion tambien se recibe como parametro, no soporta brokers con usuario y contraseña pero se puede agregar y tampoco con certificados ssl.

- El guardado de archivos se realiza en otro hilo y tiene comunicacion con todos los hilos de logueo por medio de una queue recibiendo los datos del mensaje.En el archivo de revision se tiene timestamp de horas (GMT-3), el topic donde proviene un mensaje y el mensaje propio y cada archivo tiene como nombre la fecha que se guarda en formato año-mes-dia(ej 2022-11-15 seria el 15 de noviembre de 2022). 

- Se tiene la conexion con una base de datos mysql por medio de un proceso separado el cual intenta crear la base de datos y generar la tabla necesaria, en caso de que se encuentre ya todo lo necesario para usar la base de datos creado se completa el proceso. Existe otro proceso al finalizar la creacion el cual queda funcionando y se conecta con la base de datos para empezar a añadir registros que llegan al proceso por la queue desde el hilo mqtt.

- La base de datos mysql esta deployada en docker usando Docker Desktop, tiene una tabla especifica con los campos tiempo, mensaje y topic al cual se recibio el mensaje.

- Al mismo tiempo que se realiza la lectura y el guardado tanto en archivo como en base de datos y se tiene en funcionamiento un servidor web local(accesible desde la misma red LAN ipv4/ipv6) el cual permite visualizar los archivos guardados anteriormente y el archivo que se esta escribiendo al momento. Este servidor hace uso de un hilo con asyncio y recibe variables que fueron definidas como parametros al ejecutar el programa como puerto de servidor web, directorio donde se ubican y guardan los archivos. 
