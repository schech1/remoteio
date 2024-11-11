# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero

# remoteio comparable to remote gpiozero
The user interface is similar to that of gpiozero. You may use the parameters of gpiozero.
You can write device.value=... or x=device.value depending on whether value is only readable or writeabale.
You can use remote_device.source = another remote device or a device on the client computer. Also when_... properties
or wait_... functions are syntactically useable like with gpiozero.
For creation of a remote Device we use the positional parameters remote_server,pin_1,...,pin_k. Beside these parameters the numbering ('g' or 'b' for gpio-numbering resp. board-numbering) is a twitter.
When you omitt it completely Gpio-numbering is supposed. You can also write numbering='g'. Internally all arguments without remote_server and pins are treated as named parameters. So we start with
create(*args,**kwargs). Firstly remote_server and pins are expected as (positional) parameters. By a simple argument translation the desired internal represenatation is reached.
LEDBoard, LETBarGraph use on, off, toggle in the form f(*args). Remoteio changes this in f(**kwargs), where kwargs['args']=args to have a unified internal representation. Note that at the actual state of art we consider pin devices, i.e. devices that are identified by pins. E.g. MCP3208 is identified by the select_pin Therefore this pin is expected as positional parameter. Channel is expected in the form channel=... The examples show that the interface is near gpiozero. Note that you can use all named parameters of gpiozero as named parameters too.
See the examples. Not all devices of gpiozero are supported until now. But with remoteio_devices.py there is a tool, where all devices are treated in the same manner. The idea is to support other devices like temperature measuring, SPI- and I2C-devices. With such an extension you have an overview over the state of a system and may react to changes of its state in the best way. It is interesting that tcp/ip-connection makes no problems.There are not much data but much transfers. The connection between server and client is safe by a multiprocessing lock. Remoteio_server treats all devices anonymously. Remoteio_client works more as a kernel or abstract super class that allows the creation of devices in the same manner. From a technical point of view the usage of generators and properties is important for similarity to gpiozero. Try the examples. Remote_LightSensor could not be tested at all, because there is no lightsensor in the archive. This feature is often similarily realized by an analog digital converter and a photoresistor. It is recommended to look to the examples.
Attention,when defining a device: remote server is now a parameter of the device to be created. For details see client usage or the examples.

    remote_pin = Remote_LED(remote_server,7, 'b')


## Server (remote Raspberry Pi)
Use this all-in-one command to install remoteio as deamon on port `8509`.
The server can be updated with this command.
```
bash -c "$(wget -qLO - https://github.com/schech1/remoteio/raw/master/install.sh)"

```

##  Using pip
```
pip install remoteio
```
When you want to create the server by yourself, you can install the library via
pip and use the examples below, for server- and client usage.



## Server usage
Start a remote server on port `1234`.
If no port is specified default port `8509` will be used

```
from remoteio import run_server

if __name__ == "__main__":
    run_server(port=1234)

```


## Client usage
```
from remoteio import RemoteServer,

if __name__ == "__main__":
    server_ip = "192.168.1.38"
    server_port = 1234

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = Remote_LED(remote_server,7, 'b')

    #you can say Remote_LED, remote_PWMLED, Remote_xxx,
    #where xxx is the name of a supported gpiozero device

    remote_pin.on(time_ms=2000) # (Optional) Time until switch off
    remote_pin.blink() # Blink LED
    remote_pin.pulse() # Pulse LED
    remote_pin.off()
    remote_server.close()
```

### Use Board numbering
```
remote_pin = remote_LED(remote_server,7, 'b') # Use physical board numbering
```
### Use GPIO numbering
```
remote_pin = remote_LED(remote_server,4, 'g') # Use GPIO numbering (e.g. GPIO4)
```
### GPIO numbering Default
...

remote_pin = remote_LED(remote_server,4)  # Use GPIO numbering (e.g. GPIO4)
...

