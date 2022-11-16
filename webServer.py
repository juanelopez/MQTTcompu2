import asyncio
import os
import datetime

##########WEBSERVER############
async def handle(reader, writer,cantidad_lectura,directory):
    data = await reader.read(100)
    request_recibida = []
    request_recibida = data.split(b'\r\n')
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("ADRESS:",addr)
    #logger = asyncio.create_task(complementarias.mostrar_direccion(addr,directorio))
    peticion = asyncio.create_task(devolver_peticion(request_recibida,writer,cantidad_lectura,directory))
    #await logger
    await peticion
    writer.close()    


async def devolver_peticion(request_recibida,writer,cantidad_lectura,directory):
    #directory = "/"    
    dividir_request = request_recibida[0].decode().split(" ")
    metodo = dividir_request[0]
    archivo = dividir_request[1]
    print(dividir_request)
    if(directory == "/"):
        directory = ""
    if (archivo == "/"):
        archivo = "/index.html"
        extension = "html"
        dividir_500_extension = ["html"]    
    else:
        extension = "txt"        
        dividir_500_extension = ["txt"]
    version = str.encode(dividir_request[2])        
    if(len(dividir_500_extension) > 1):
        enviar_500 = version + b' 500 Internal Server Error\n'
        writer.write(enviar_500)
    else:
        if(metodo == "POST"):
            enviar_500 = version + b' 500 Internal Server Error\n'
            writer.write(enviar_500)
        elif(metodo == "GET"):
            try:
                if(archivo == "/index.html"):                    
                    print("Pantalla de inicio")
                    request = version+b' 200 OK\n'
                    content_type = "Content-Type: text/"+extension+"\n"
                    request_lenght = b'Content-Lenght:20000\n\n'
                    writer.write(request)
                    writer.write(bytes(content_type,'utf-8'))
                    writer.write(request_lenght)
                    writer.write(bytes("<HTML><HEAD><TITLE>MQTT LOGGER</TITLE>",'utf-8'))
                    writer.write(bytes("<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3' crossorigin='anonymous'>",'utf-8'))
                    writer.write(bytes("</HEAD><BODY>",'utf-8'))                    
                    writer.write(bytes("<div class='page-header'><h1 > Logger mqtt computacion 2</h1></div>",'utf-8'))                    
                    if (directory == ''):
                        buscar_dir = os.scandir()
                    else:
                        buscar_dir = os.scandir(directory)
                    for path in buscar_dir:
                        if(path.is_file()):                            
                            link = '<div class="w-100"><a class="btn btn-outline-success btn-lg btn-block"  href="'+path.name+'"''</a>'+path.name
                            link = link + '</div>'
                            writer.write(bytes(link,'utf-8'))
                    writer.write(bytes("</BODY></HTML>",'utf-8'))
                else:
                    if(directory != ''):
                        file_open = directory+'/'+archivo[1:]
                    else:
                        file_open = archivo[1:]
                    print("Archivo mostrado",file_open)
                    fd1 = os.open(file_open,os.O_RDONLY)
                    request = version+b' 200 OK\n'
                    content_type = "Content-Type: text/plain\n"
                    request_lenght = b'Content-Lenght:20000\n\n'
                    writer.write(request)
                    writer.write(bytes(content_type,'utf-8'))
                    writer.write(request_lenght)             
                    lectura = os.read(fd1,cantidad_lectura)
                    while(lectura != b''):
                        writer.write(lectura)
                        lectura = os.read(fd1,cantidad_lectura)
                    os.close(fd1)
            except:
                print("El archivo no existe")				
                request = version +b' 404 Not Found\n'
                writer.write(request)
    await writer.drain()    

async def webServer(PORT,cantidad_lectura,directory):
    server = await asyncio.start_server(lambda r,w: handle(r,w,cantidad_lectura,directory), ('::','0.0.0.0'),PORT)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')  
    async with server:
        await server.serve_forever()