# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero


# new behavior of remoteio: simultaneous processing of remote pins
The idea is to use some remote server for manipulating e.g. an idustrial process in the case where you need more pins than the client raspberry pi can offer.
The bahavior of led.on(),led.off(),led.pulse() on the remote rpi is the same as when the client would perform them itself.
For industrial processes there is beside constant signal the necessity of impulses. Therefore led.on(time_ms) is possible. Naturally led.pulse(time_ms) and led.blink(time_ms) are also
allowed, perhaps of advantage for some visualization. The use of threads for realisation shows problems for blinking and pulsing. Because threads have no effective time sharing multiprocessing is used
in order to guarantee the right bevavior of pulsing and blinking. For one pin, if several tasks are send to the server, all these tasks are executed one after the other as given by the client. A task pin.close() is forbidden. Tasks for different pins are treated independently, simultaneous. The remoteio project forces the use of a set of pins. These pins are closed together, when the communication to the server is closed. But this closing is a soft closing, that guarantees that all tasks transferred from the client are perfomed before closing the leds.  

The main ideas in remoteio_server.py are the use of 
  1. queing of received data to avoid time loss in receiving data
  2. an own process for each pin for treating pins simultaneously
  3. multiprocessing safe queues for each pin as input to the pin-specific processes
  4. the getattr function to find led-funtions only by knowing the name of the function
  5. synchronization technics necessary because of multiprocessing
  6. the communication with the reveive-buffer, necessary because when more data then receive-buffer(size)=1024 come in together, there were problems of interpretating the data. 


Main ideas in remote_client.py 
1. internal pin numbering is board numbering. Gpio-numbering is internally translated in board numbering. This simplifies the verification whether someone wants to define a remotr pin two times.
   Further, the internal pin numbering is 'b', by the aid of a conversion dictionary. This allows to suppress the establishing of the sam pin two times by different representations by 'b' and 'g'
   The syntax to operate the pins is the same as that of remoteio.
2. led.cose() is not allowed
3. led.blink(tims_ms,arg1,arg2) is allowed, for defining different on and off times.
4. led.value(arg1) is allowed for a constant light which is not the maximum possible light of a led.



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
    remote_pin.blink(arg1=0.1,arg2=0.1)    # fast blinking
    remote_pin.pulse() # Pulse LED
    remote_pin.value(arg1=0.5)              # half brightness
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

