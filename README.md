# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero


## Install remote server as deamon
Use this all-in-one command to install remoteio as deamon on port `8509`.
If remoteio is already installed, this command will update all files.
```
bash -c "$(wget -qLO - https://github.com/schech1/remoteio/raw/master/install.sh)"

```

## Install using pip
```
pip install remoteio
```
When using pip, the server needs to be set up manually. 
See the examples below.



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
    remote_pin = remote_server.pin(7, 'b')
    remote_pin.on(time_ms=2000) # Time until switch off
    remote_pin.blink() # Blink LED
    remote_pin.pulse() # Pulse LED
    remote_pin.off()
    remote_server.close()
```

### Use Board numbering
```
remote_pin = remote_server.pin(7, 'b') # Use physical board numbering
```
### Use GPIO numbering
```
remote_pin = remote_server.pin(4, 'g') # Use GPIO numbering (e.g. GPIO4)
```

