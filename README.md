# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero

# remotio delegating to gpiozero
A remoteio device needs the remote server, where the device is situated, further an ident to identify it on the server for actions.
Last not least the obj_type of the device is needed to work with the right gpiozero device.
The client transfers the following parameter to the server to work with a gpiozero device:
  ident,obj_type,*args,**kwargs
While ident and obj_type are needed by remoteio the parameter *args and **kwargs are directly delegated to the gpiozero device

1. creating a gpiozero device
   rs=RemoteServer(ip_adress,port)
   led=Remote_XXX(rs,*args,**args), where xxx is the name of a gpiozero device like LED,PWMLED,RGBLED etc.
   The ident is automatically generated for the handling with the server, obj_type is just XXX

3. A command like blink(**kwargs) or on(*args) is to be used as described in the API of gpiozero.
   Further remoteio supports on(on_time) for a short impuls realized by blink(on_time=on_time,off_time=0,n=1).

4. remoteio supports a Remoteio_Compositum device, defined by having the attributes on,off,toggle,blink. It supports
  pulse for the gpiozero devices of the Compositum that can pulse. The functions getClientDevice(), setClientDevice() are used to make messages more readable by
  the user. At this purpose gpiozero offers **namedpins and *_order.

5. remoteio supports expressions like led.value=... by the use of properties.
   The attributes of a gpiozero device are reflected in the corresponding remoteio device. Remoteio differs between functions, attributes that are only readable and writeable attributes.
   The remoteio_client.py acts as a kernel for all devices, so that all remote devices are programmed in the same manner.

For details study the examples in controller.py
      

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
from remoteio import RemoteServer

if __name__ == "__main__":
    server_ip = "192.168.1.38"
    server_port = 1234

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = Remote_LED(remote_server,pinNr)
    remote_pin.on(on_time=2.0) # (Optional) Time until switch off in sec
    remote_pin.blink() # Blink LED
    remote_pin.pulse() # Pulse LED
    remote_pin.off()
    remote_server.close()
# A complete set of examples is in controller.py
```

### Use Board numbering
```
pinNr = map_bg(7, 'b') # physical board number is translated to GPIO4
```
### Use GPIO numbering
```
pinNr = 4 # GPIO numbering (e.g. GPIO4) is default
```

