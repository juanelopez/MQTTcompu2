# Logger mqtt computación 2.


## EJECUCION.
Para ejecutar la publicacion con todos las dependencias y docker deployado se ejecuta main.py.
Los parametros que se usan son:
- -s 1024 (tamaño de lectura para servidor web).
- -d guardado(carpeta donde se guardan los archivos de texto con el logueo mqtt), debe estar creada.
- -p 3000 (puerto de servidor web)
- -b broker.hivemq.com (broker al que se quiere conectar)
- -l esp/# -l raspberry/# (topicos a los que se quiere subscribir, se puede subscribir a mas escribiendo -l y el topic)

### Ejemplo comando
- $python main.py -s 1024 -d guardado -p 3000 -b broker.hivemq.com -l test/# -l t/# -l sys/# -l testtopic/# -l debug/# -l raspberry/# -l esp/# -u test -ps test -db test -pdb 1010

### Acceso desde navegador.

Para acceder al servidor web por ipv4 localmente se usa:
http://localhost:3000
Para acceder por ipv6 se usa:
http://[::1]:3000
En caso de querer acceder desde un equipo en la red LAN se usa:
http://"ipLAN":3000
siendo ipLAN reemplazado por la ip del dispositivo en la red que se puede encontrar con ifconfig en linux o ipconfig en windows desde sus terminales.

## PROBLEMAS-SOLUCION.

**Problema: No guarda en base de datos.**
- Solucion: Base de datos sin ejecutar.
- Solucion2: Parametros de base de datos incorrectos.
- Solucion3: Puerto ocupado.

**Problema: No se ejecuta el servidor web.**
- Solucion: Puerto ocupado.

**Problema: No se muestran los archivos en el servidor web.**
- Solucion: No se elegio la carpeta correcta.

**Problema: No se subscribe al broker.**
- Solucion: Revisar la conexion a internet.
- Solucion2: Revisar si realmente el broker funciona.
- Solucion3: Revisar si esta bien escrita la direccion.
