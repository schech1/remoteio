# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero

# New behavior of remoteio: simultaneity
When remoteio proceeds 2 pins, the second pin must wait until the first one has made his work on the server. This may take time, if the first pin has a long timer and the second pin cannot start its work.
A pin blocks itself in the same way. In this modification of remoteio, different pins can work simultaneously. If a pin has two tasks and the second one is asked to start before the first one has finished,
the second one interrupts the first one.
The main modifications are the use of 
  1. a list of maps, that allows sending of tasks of several pins to the server
  2. an own thread for each pin for treating
  3. thread safe queues for each pin as input to the pin-specific threads
  4. a thread.Timer in handle_timer instead of time.sleep in order to make the interruption of a task with a time_ms>0 possible
  5. the getattr function to find led-funtions only by knowing the name of the function 

Further, the internal pin numbering is 'b', by the aid of a conversion dictionary. This allows to suppress the establishing of the same pin two times by different representations by 'b' and 'g'
The syntax to operate the pins is the same as that of remoteio.


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
    remote_pin = remote_server.pin(7, 'b')
    remote_pin.on(time_ms=2000) # (Optional) Time until switch off
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

