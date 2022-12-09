# Dependencias necesarias para ejecutar:

## python3
```shell
$ pip install mysql-connector-python
$ pip install paho-mqtt
$ pip install setuptools
```

## En windows instalar "Docker desktop" con container mysql con los siguientes parametros:
- MYSQL_ROOT_PASSWORD 123456
- MYSQL_DATABASE Logger
- MYSQL_USER python
- MYSQL_PASSWORD 123456
- PORT 5000

Guia de instalacion docker desktop: https://docs.docker.com/desktop/install/windows-install/

## En ubuntu se ejecuta el siguiente comando:
- $ sudo docker run -d -p 5000:3306 --name mysql-db -e MYSQL_ROOT_PASSWORD=12345 -e MYSQL_DATABASE=Logger -e MYSQL_USER=python -e MYSQL_PASSWORD=123456 mysql
Podemos ver si realmente se ejecuta con:
- $ sudo docker ps 
Para eliminar el container usamos:
- $ sudo docker rm -f mysql-db
