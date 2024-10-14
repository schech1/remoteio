# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero

# new behavior of remoteio: simultaneous processing of remote pins
The idea is to use some remote server for manipulating e.g. an idustrial process in the case where you need more pins than the client raspberry pi can offer.
The behavior of led.on(),led.off(),led.pulse() on the remote rpi is the same as when the client would perform them itself.
For industrial processes there is beside constant signal the necessity of impulses. Therefore led.on(time_ms) is possible. Naturally led.pulse(time_ms) and led.blink(time_ms) are also
allowed, perhaps of advantage for some visualization. The use of threads for realisation shows problems for blinking and pulsing. Because threads have no effective time sharing, multiprocessing is used
in order to guarantee the right bevavior of pulsing and blinking. For one pin, if several tasks are send to the server, all these tasks are executed one after the other as given by the client. A task pin.close() is allowed. Tasks for different pins are treated independently, simultaneously. The remoteio project forces the use of a set of pins. These pins are closed together, when the communication to the server is closed by the client. But this closing is a soft closing, that guarantees that all tasks transferred from the client are perfomed before closing the leds. The function run_server of remoteio_server has two modi. One mode ('wait') garantees that each manipulating of a remote pin is executed, the other mode ('nowait') interrupts a preceeding manipulate-task when a new manipulating of the same pin reaches the server before the preceeding task is finished.  

The main technical ideas in remoteio_server.py are the use of 
  1. queing of received data to avoid time loss in receiving data
  2. an own process for each pin for treating pins simultaneously
  3. multiprocessing safe queues for each pin as input to the pin-specific processes
  4. the getattr function to find led-funtions only by knowing the name of the function
  5. synchronization technics necessary because of multiprocessing
  6. special treating of the reveive-buffer, necessary when more data then the length of the receive-buffer(size)=1024 come in.
  7. communication of success to the client: remoteio_server.handle_client(...) <----> remoteio_client.remote_pin.execute()
  8. use of the queue from handle_client ---> handle_led in the other direction in order to synchronize led creation and process generation.

Main ideas in remoteio_server
  1. def run_server(port=PORT,mode='wait') with a further parameter mode, that defaults to 'wait'.
     In the mode 'wait' each pin-manipulation that reaches the server is executed, even if the connection is interrupted.
     In the mode 'nowait' a pin-manipulation interrupts the preceeding one, even if time_ms is not finished.
     
Main ideas in remote_client.py 
1. internal pin numbering is board numbering. Gpio-numbering is internally translated in board numbering. This simplifies the verification whether someone wants to define a remotr pin two times.
2. led.cose() is allowed, all tasks for a closed pin are ignored. This is communicated to the client.
3. led.blink(tims_ms,arg1,arg2) is allowed, for defining different on and off times.
4. led.value(time_ms,arg1) is allowed for a constant light which is not the maximum possible light of a led.
5. led.off(time_ms) is allowed.
   
By the above changes you can fully use the time of the remote server


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

