This is a change of the remoteio code that allows the simultaneous proceeding of remote pins.
You can ask for on,off,blink,pulse of several pins and then proceed them by the execute-function. See the example
Controller.py
After proceeding several pins by execute you can proceed a part of them newly by execute or other ones after defining
before. Syntax is that of original remoteio. But you must use execute to proceed.

# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero


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
import time
import logging

    
try:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name="remoteio")
    raspi1='raspy5' 
    # erstellt virtuelle Pins auf 2 verschiedenen Raspberry Pis
    remote_pi=None
    remote_pi=RemoteServer(raspi1)
    # 'g ': BCM -B e z e i c h n u n g ( G P I O 2 1 )
    remote_pin=remote_pi.pin(21,'g')
    remote_pin1=remote_pi.pin(20,'g')
    remote_pin2=remote_pi.pin(16,'g')


    
    # without time-parameter also possible
    remote_pin.on(time_ms=10000)
    remote_pin1.pulse(time_ms=10000)
    remote_pin2.blink(time_ms=10000)
    remote_pi.execute()
    time.sleep(15.0)

    
    remote_pin.on(time_ms=20000)
    remote_pi.execute()
    while True:
        pass
except Exception as e:
    logger.info(str(e))
finally:
    if remote_pi:
        remote_pi.close()
 
```

### Use Board numbering
```
remote_pin = remote_server.pin(7, 'b') # Use physical board numbering
```
### Use GPIO numbering
```
remote_pin = remote_server.pin(4, 'g') # Use GPIO numbering (e.g. GPIO4)
```

