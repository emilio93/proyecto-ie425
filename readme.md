# Trabajo Final IE425

## Contenido

- [Parte 2: Trabajo de Investigación y Programación de Sockets con TCP y UDP](#parte-2-trabajo-de-investigación-y-programación-de-sockets-con-tcp-y-udp)
  - [Enunciado](#enunciado)
  - [Plataformas Utilizadas](#plataformas-utilizadas)
    - [Windows](#windows)
      - [Python](#python)
  - [Proceso Cliente-Servidor en una Computadora](#proceso-cliente-servidor-en-una-computadora)
  - [Servidor TCP](#servidor-tcp)
    - [Uso](#uso)
  - [Cliente TCP](#cliente-tcp)
    - [Uso](#uso-1)
  - [Conexión TCP](#conexión-tcp)
    - [Revisión con Wireshark](#revisión-con-wireshark)
    - [Mayor Cantidad de Conexiones](#mayor-cantidad-de-conexiones)
    - [Mayor Tamaño del Datagrama](#mayor-tamaño-del-datagrama)
  - [Servidor UDP](#servidor-udp)
    - [Uso](#uso-2)
  - [Cliente UDP](#cliente-udp)
    - [Uso](#uso-3)
  - [Conexión UDP](#conexión-udp)
    - [Revisión con Wireshark](#revisión-con-wireshark-1)
    - [Mayor Cantidad de Conexiones](#mayor-cantidad-de-conexiones-1)
    - [Mayor Tamaño del Datagrama](#mayor-tamaño-del-datagrama-1)
  - [Aplicación](#aplicación)


## Parte 2: Trabajo de Investigación y Programación de Sockets con TCP y UDP

### Enunciado

> Trabajo Básico
>
> Los procesos de aplicación envían mensajes a través de sockets. Existen dos protocolos en el nivel de transporte, TCP y UDP.
>
> Una aplicación típica de red, consiste en dos programas, un programa cliente y un programa servidor. Cuando estos dos programas se ejecutan, se crean un proceso cliente y un proceso servidor. Estos procesos se comunican entre sí leyendo de y escribiendo en sockets.
>
> Típicamente, todo esto se hace en dos computadoras (hosts), pero también se pueden hacer en una sola computadora o host. Investigar y explicar como se hace en una sola computadora.
>
> Estos programas deben de hacerse en Python versión 2.7.
>
> Se debe investigar los conceptos de cómo hacer estos 4 programas, en TCP servidor TCP, cliente TCP, servidor UDP y cliente UDP. Buscar en Internet los conceptos de cómo escribir estos programas. El trabajo debe de explicar estos conceptos.
>
> En TCP (orientado a conexión y con confiabilidad), el servidor tiene que estar listo para responder pedidos del cliente y debe de tener un socket de bienvenida. El cliente crea un socket y especifica el destino. Debe de crear el 3 way handshake.
>
> En UDP (sin conexión y sin confiabilidad), el servidor no tiene que estar listo ya que no hay un handshake. El servidor crea un socket y no hay un socket de bienvenida. El cliente crea un socket e inicia.
>
> Existen ejemplos de esto en la literatura. El estudiante debe de explicar cada instrucción de los programas, explicar las instrucciones utilizadas, y hacer un diagrama de bloques de los programas.
>
> Lo ideal es hacerlo para ambiente MAC, pero sino puede hacerse en otras plataformas.
>
> Para probar los programas, se deben de transmitir una serie de caracteres desde el cliente y estos deben de ser recibidos en el servidor y cambiados a mayúsculas y volverlos a enviar en mayúscula al cliente desde el servidor.
>
> Debe de tener una forma para terminar el envio de caracteres. Deben de especificar cuantas conexiones cliente/servidor son posibles. Cual es el tamaño máximo del datagrama.

### Plataformas Utilizadas

#### Windows

Al ejecutar:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture
```
Se obtiene:
```powershell
Caption                  Version    OSArchitecture
-------                  -------    --------------
Microsoft Windows 10 Pro 10.0.17134 64-bit
```

##### Python

Al ejecutar:
```bash
python --version
```
Se obtiene:
```bash
Python 2.7.16
```

### Proceso Cliente-Servidor en una Computadora

Para lograr ejecutar una comunicación cliente-servidor en una computadora, se utiliza la dirección IP de _loopback_, `127.0.0.1`, esta dirección se refiera al dispositivo en que se ejecuta la aplicación.

Se puede tener un proceso escuchando un _socket_ en la dirección de _loopback_ y puerto arbitrario. Otro proceso inicia la conexión y envía datos a un _socket_ en la misma dirección y puerto, de esta manera se logra el proceso cliente-servidor en una computadora.

Otra manera de lograr este proceso, es utilizar una máquina virtual, estableciendo una conexión ethernet entre el sistema operativo anfitrión y huésped.

Los lenguajes de programación suelen proveer una interfaz para crear _sockets_ , es decir, permite crear conexiones TCP y UDP. En el caso de python, se provee el paquete `socket` con la instalación, este paquete se encarga de crear las conexiones utilizando el _three-way handshake_ y transmitir los datos.

### Servidor TCP

El servidor TCP espera una conexión en la dirección y puerto seleccionados(por defecto `127.0.0.1:5005`). Cuando recibe una conexión, debe aceptarla y luego comienza a recibir datos en trozos del tamaño del buffer(por defecto 32). Conforme recibe los datos, el servidor los manipula(pasa el texto a mayúsculas) y los devuelve. Al finalizar el trasiego de los datos, el servidor cierra la conexión.

El servidor TCP se encuentra en el archivo [`src/tcpServer.py`](src/tcpServer.py).

#### Uso

```bash
python src/tcpServer.py --help
Servidor TCP
USO:

  python tcpServer.py -h hostIp -p puerto -s tamanoBufer
  python tcpServer.py --host-ip hostIp --port puerto --buffer-size tamanoBufer

Ejemplo:

  python tcpServer.py -h 127.0.0.1 -p 5005 -s 20
```

### Cliente TCP

El cliente TCP espera un mensaje ingresado por el usuario para enviar a la dirección y puerto seleccionados(por defecto `127.0.0.1:5005`). Se crea la conexión y cuando se envía el mensaje, el cliente queda pendiente a la respuesta del servidor. Como sabe que la longitud de la respuesta es la misma que la del mensaje enviado, el cliente toma tantas respuestas como sean necesarias para haber recibido todos los datos de vuelta. Luego de esto cierra la conexión.

El cliente TCP se encuentra en el archivo [`src/tcpClient.py`](src/tcpClient.py).

#### Uso

```bash
python src/tcpClient.py --help
Cliente TCP
USO:

  python tcpClient.py -h hostIp -p puerto -s tamanoBufer
  python tcpClient.py --host-ip hostIp --port puerto --buffer-size tamanoBufer

Ejemplo:

  python tcpClient.py -h 127.0.0.1 -p 5005 -s 1024
```

### Conexión TCP

Para crear la conexión, se debe abrir dos terminales en la misma ruta donde se tienen los archivos `tcpClient.py` y `tcpServer.py`. Se ejecuta el cliente en una terminal y el servidor en otra.
```bash
#
# terminal A
#
python src/tcpClient.py

#
# terminal B
#
python src/tcpServer.py

```

En la terminal A, es decir, en el cliente, se puede ingresar un mensaje y presionar enter, el servidor devolverá el mensaje en mayúsculas.
El cliente queda esperando otro mensaje para enviar.

```bash
#
# terminal A
#
python src/tcpClient.py
Cliente TCP
IP: 127.0.0.1
Puerto: 5005
Tamano de Buffer: 32

Mensaje: hola
  Mensaje enviado: hola
    Trozo recibido: HOLA
  Mensaje recibido: HOLA
  Cliente TCP: Conexion cerrada

Mensaje:
```

En la terminal B, es decir, en el servidor, aparecen los datos de la conexión y los datos recibidos y enviados.

```bash
#
# terminal B
#
python src/tcpServer.py
Servidor TCP
IP: 127.0.0.1
Puerto: 5005
Tamano de Buffer: 32

Direccion de conexion: ('127.0.0.1', 56601)
    Trozo recibido: hola
    Trozo enviado: HOLA
  Mensaje recibido: hola
  Mensaje enviado: HOLA
  Servidor TCP: Conexion cerrada.
```

#### Revisión con Wireshark

En el archivo [`wireshark-data/ws-tcpdump.md`](wireshark-data/ws-tcpdump.md) se muestra una captura en wireshark para el ejemplo de uso mostrado. Los 3 primeros _frames_ son el _three-way_ _handshake_, se identifican por la bandera `SYN` las dos primeras, la tercera por la bandera `ACK` y longitud del paquete igual a cero. Las tramas 8, 9, 10 y 11 encargan de finalizar la conexión.

Resumen de _three-way handshake_:

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 1 | 127.0.0.1 | 127.0.0.1 | TCP | 66 | 56601 → 5005 [SYN] Seq=0 Win=64240 Len=0 MSS=65495 WS=256 SACK_PERM=1 |
| 2 | 127.0.0.1 | 127.0.0.1 | TCP | 66 | 5005 → 56601 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=65495 WS=256 SACK_PERM=1 |
| 3 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 56601 → 5005 [ACK] Seq=1 Ack=1 Win=525568 Len=0 |

Resumen de desconexión:

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 8 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 56601 → 5005 [FIN, ACK] Seq=5 Ack=5 Win=525568 Len=0 |
| 9 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 56601 [ACK] Seq=5 Ack=6 Win=525568 Len=0 |
| 10 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 56601 [FIN, ACK] Seq=5 Ack=6 Win=525568 Len=0 |
| 11 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 56601 → 5005 [ACK] Seq=6 Ack=6 Win=525568 Len=0 |

#### Mayor Cantidad de Conexiones

#### Mayor Tamaño del Datagrama

### Servidor UDP

El servidor UDP espera una conexión en la dirección y puerto seleccionados(por defecto `127.0.0.1:5005`).

El servidor UDP se encuentra en el archivo [`src/udpServer.py`](src/udpServer.py).

#### Uso

```bash
python src/udpServer.py --help
Servidor UDP
USO:

  python udpServer.py -h hostIp -p puerto -s tamanoBufer
  python udpServer.py --host-ip hostIp --port puerto --buffer-size tamanoBufer

Ejemplo:

  python udpServer.py -h 127.0.0.1 -p 5005 -s 20
```

### Cliente UDP

El cliente UDP espera un mensaje ingresado por el usuario para enviar a la dirección y puerto seleccionados(por defecto `127.0.0.1:5005`). Se crea la conexión y cuando se envía el mensaje, el cliente queda pendiente a la respuesta del servidor.

El cliente UDP se encuentra en el archivo [`src/udpClient.py`](src/udpClient.py).

#### Uso

```bash
python src/udpClient.py --help
Cliente UDP
USO:

  python udpClient.py -h hostIp -p puerto -s tamanoBufer
  python udpClient.py --host-ip hostIp --port puerto --buffer-size tamanoBufer

Ejemplo:

  python udpClient.py -h 127.0.0.1 -p 5005 -s 1024
```

### Conexión UDP

Para crear la conexión, se debe abrir dos terminales en la misma ruta donde se tienen los archivos [`src/udpClient.py`](src/udpClient.py) y [`src/udpServer.py`](src/udpServer.py). Se ejecuta el cliente en una terminal y el servidor en otra.
```bash
#
# terminal A
#
python src/udpClient.py

#
# terminal B
#
python src/udpServer.py

```

En la terminal A, es decir, en el cliente, se puede ingresar un mensaje y presionar enter, el servidor devolverá el mensaje en mayúsculas.
El cliente queda esperando otro mensaje para enviar.

```bash
#
# terminal A
#
Cliente UDP
  IP: 127.0.0.1
  Puerto: 5005
  Tamano de Buffer: 32

Mensaje: hola
  Mensaje enviado: hola
  Mensaje recibido: HOLA

Mensaje:
```

En la terminal B, es decir, en el servidor, aparecen los datos de la conexión y los datos recibidos y enviados.

```bash
#
# terminal B
#
Servidor UDP
  IP: 127.0.0.1
  Puerto: 5005
  Tamano de Buffer: 32

Direccion de conexion: ('127.0.0.1', 55860)
  Mensaje recibido: hola
  Mensaje enviado: HOLA

```

#### Revisión con Wireshark

En el archivo [`wireshark-data/ws-udpdump.md`](wireshark-data/ws-udpdump.md) se muestra una captura en wireshark para el ejemplo de uso mostrado. Solo se tienen dos tramas, una enviada por el cliente y la otra enviada por el servidor.

#### Mayor Cantidad de Conexiones

#### Mayor Tamaño del Datagrama

### Aplicación

Para las aplicaciones del servidor tanto TCP como UDP, se utiliza una mismo método que se encarga de pasar el texto a mayúscula y responder esto al cliente. Además comparte con el cliente la habilidad de ser cerrado, para esto se recibe el mensaje `$$ exit`. Se puede ver la informacion de los hosts con `$$ info` y se puede actualizar el valor del buffer, por ejemplo a 64, `$$ update -s 64`.

Para las aplicaciones del cliente tanto TCP como UDP, se analiza el mensaje enviado para determinar si se trata de un comando, los mismos que se han indicado para el servidor.

Cuando se quiere aplicar un comando solo al cliente o solo al servidor, se utilizan las palabras `local` y `remote` respectivamente, justo luego del comando. Por ejemplo se cierra el servidor con `$$ exit remote`, o el cliente con `$$ exit local`. Para actualizar el buffer, de nuevo a 64, solo el el servidor, se usaría `$$ update remote -s 64`. En el último caso, se utiliza la bandera `-s`, que indica el tamaño del buffer, para el comando `$$ info`, se permiten las banderas `-h`, `-p` y `-s`, para imprimir solo la dirección ip, puerto, o tamano de buffer respectivamente. Por ejemplo `$$ info local -h`
