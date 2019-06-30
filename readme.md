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
python.exe --version
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

El servidor TCP se encuentra en el archivo `tcpServer.py`.

#### Uso

```bash
python.exe .\tcpServer.py --help

USO:

  python ./tcpServer.py -h hostIp -p puerto -s tamanoBufer
  python ./tcpServer.py --host-ip hostIp --port puerto --buffer-size tamanoBufer

Ejemplo:

  python ./tcpServer.py -h 127.0.0.1 -p 5005 -s 20
```

### Cliente TCP

El cliente TCP espera un mensaje ingresado por el usuario para enviar a la dirección y puerto seleccionados(por defecto `127.0.0.1:5005`). Se crea la conexión y cuando se envía el mensaje, el cliente queda pendiente a la respuesta del servidor. Como sabe que la longitud de la respuesta es la misma que la del mensaje enviado, el cliente toma tantas respuestas como sean necesarias para haber recibido todos los datos de vuelta. Luego de esto cierra la conexión.

El cliente TCP se encuentra en el archivo `tcpClient.py`.

#### Uso

```bash
python.exe .\tcpClient.py --help

USO:

  python ./tcpClient.py -h hostIp -p puerto -s tamanoBufer
  python ./tcpClient.py --host-ip hostIp --port puerto --buffer-size tamanoBufer

Ejemplo:

  python ./tcpClient.py -h 127.0.0.1 -p 5005 -s 1024
```

### Conexión TCP

Para crear la conexión, se debe abrir dos terminales en la misma ruta donde se tienen los archivos `tcpClient.py` y `tcpServer.py`. Se ejecuta el cliente en una terminal y el servidor en otra.
```bash
#
# terminal A
#
python.exe .\tcpClient.py

#
# terminal B
#
python.exe .\tcpServer.py

```

En la terminal A, es decir, en el cliente, se puede ingresar un mensaje y presionar enter, el servidor devolverá el mensaje en mayúsculas.
El cliente queda esperando otro mensaje para enviar.

```bash
#
# terminal A
#
python.exe .\tcpClient.py
Cliente TCP
IP: 127.0.0.1
Puerto: 5005
Tamano de Buffer: 32

Mensaje: hola
    Datos Enviados: hola
    Datos Recibidos: HOLA

Mensaje:
```

En la terminal B, es decir, en el servidor, aparecen los datos de la conexión y los datos recibidos y enviados.

```bash
python.exe .\tcpServer.py
Servidor TCP
IP: 127.0.0.1
Puerto: 5005
Tamano de Buffer: 32

Direccion de conexion: ('127.0.0.1', 52715)
    Datos Recibidos: hola
    Datos Enviados: HOLA
```

### Aplicación

Para las aplicaciones del servidor tanto TCP como UDP, se utiliza una mismo método que se encarga de pasar el texto a mayúscula. Además comparte con el cliente la habilidad de ser cerrado, para esto se envía el mensaje `$$ exit`.

#### Revisión con Wireshark

En el archivo [`ws-tcpdump.md`](ws-tcpdump.md) se muestra una captura en wireshark para el ejemplo de uso mostrado. Los 3 primeros _frames_ son el _three-way_ _handshake_, se identifican por la bandera `SYN` las dos primeras, la tercera por la bandera `ACK` y longitud del paquete igual a cero. Las tramas 8, 9, 10 y 11 encargan de finalizar la conexión.

Resumen de _three-way handshake_:

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 1 | 127.0.0.1 | 127.0.0.1 | TCP | 66 | 52715 → 5005 [SYN] Seq=0 Win=64240 Len=0 MSS=65495 WS=256 SACK_PERM=1 |
| 2 | 127.0.0.1 | 127.0.0.1 | TCP | 66 | 5005 → 52715 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=65495 WS=256 SACK_PERM=1 |
| 3 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [ACK] Seq=1 Ack=1 Win=525568 Len=0 |

Resumen de desconexión:

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 8 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [FIN, ACK] Seq=5 Ack=5 Win=525568 Len=0 |
| 9 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 52715 [ACK] Seq=5 Ack=6 Win=525568 Len=0 |
| 10 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 52715 [FIN, ACK] Seq=5 Ack=6 Win=525568 Len=0 |
| 11 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [ACK] Seq=6 Ack=6 Win=525568 Len=0 |

#### Mayor Cantidad de Conexiones

#### Mayor Tamaño del Datagrama
