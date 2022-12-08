# Funcionalidades.
## Lado servidor.
- Guardar mensajes mqtt en archivos.
- Creacion base de datos y tabla.
- Guardar mensajes mqtt en base de datos.
- Mostrar mensajes mqtt en terminal donde se ejecuta.
- Atender peticiones GET hacia el servidor web.

## Lado cliente .
- Revisar registros desde servidor web.

## Descripcion de funcionalidad por archivo
### Archivo mqtt.py.
- Realiza conexion al broker mqtt.
- Realiza subscripciones a los topics del broker con un hilo por subscripcion.
- Envio por queue a otros hilos/proceso de mensajes y topic.

### Archivo basedata.py.
- Realiza la creacion de la base de datos mysql.
- Realiza la creacion de la tabla dentro de la base de datos mysql.
- Inserta los registros que llegan desde la queue mqtt a la tabla con su correspondiente timestamp.

### Archivo filesaver.py.
- Crea cada dia un archivo con el nombre del dia (formato "año-mes-dia").
- Escribe con timestamp(solo hora) el topic y mensaje mqtt que se recibe por la queue mqtt.

### Archivo webServer.py.
- Ejecuta un webserver local.
- Procesa solicitudes GET de texto plano y html(pantalla principal).
- Pantalla principal con botones donde se eligen los archivos a visualizar.

### Archivo main.py.
- Parseo de los argumentos tamaño de lectura, directorio de guardado, puerto de servidor web, broker y lista de topics.
- Ejecucion de proceso de creacion de base de datos/tabla.
- Ejecucion de proceso de logueo en base de datos.
- Creacion de queue de hilos y queue de proceso.
- Ejecucion de hilo de coneccion mqtt.
- Ejecucion de hilos de subscripcion a topic default.
- Ejecucion de hilo de servidor web.
- Ejecucion de hilo de guardado de archivos.




