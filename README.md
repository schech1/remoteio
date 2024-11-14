# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero

# remoteio comparable to remote gpiozero
This version brings deep changes in order to harmonize with gpiozero. A remote device is created with the three positioning
parameters remote_server, ident,o bj_type in order to manage the passthrough to gpiozero on the server side. These 3 postional parameter
are followed by *args,**kwargs which are given to gpiozero as they are. So you can use the gpiozero parameter as given in the gpiozero API.
Further time_ms is replaced by on_time(sec). Timing is delegated to gpiozero, e.g. on(on_time=5.0) is realized as blinking(on_time=5.0,off_time=0,n=1).
Remoteio does not support timing itself. This is important for realizing properties like x.value=... or y=x.value without risking timeouts of getter and setter functions.
on(on_time=5.0) is interrutable e.g. by blink(). Therefore when it is wished that on_time is fully executed and you want to append e.g. a blink() to that pin, then remember
that blink() starts immediately,when called. Therefore you better wait 5 seconds by a sleep or a timer. The on_time parameter for on(...) makes sense when you want to give a signal
to different pins, where you don't want to wait until preceeding pins have switched off or when you want to guarantee a good timing for an impulse.
The properties of the following devices as well as their functions and when_... and wait_for clauses are just realized:
Remote_LED,Remote_PWMLED,Remote_RGBLED,Remote_Buzzer,Remote_TonalBuzzer, Remote_Motor,Remote_PhaseEnableMotor,Remote_Servo,Remote_AngularServo,Remote_Button,
Remote_MCP3208, Remote_LineSensor, Remote_MotionSensor,Remote_LightSensor, Remote_DistanceSensor,Remote_RotaryEncoder,Remote_LedBoard,Remote_LedBarGraph.
For Remote_LEDBoard and Remote_LEDBarGraph the Compositum pattern (tree and leaves) is not realized.
Remote_RotaryEncoder is endowed with an interesting mathematical feature (shortest way) for counting of the steps of the Remote_RotaryEncoder.
From a technical point of view the usage of properties is dominant. Remoteio offers functions in order to destinate whether an attribute of a remote device is a function or
an only readable or a writeable property. There are other interesting helper-functions too. Remoteio_server treats all devices in the same way without special knowledge of
the devices. Remoteio_client acts as an abstract kernel too, the details are in remote_devices. All devices are treated by the same proceeding. 
Pins are expected to be written as GPIO-pin numbers. Remoteio offers the function map_bg that translates board numbering in Gpio numbering. The examples in controller.py are 
strongly recommended.



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
from remoteio import RemoteServer, Remote_LED, map_bg

if __name__ == "__main__":
    server_ip = "192.168.1.38"
    server_port = 1234

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = Remote_LED(remote_server,ident,map_bg(7, 'b'))    # ident is a freely chooseable string.

    #you can say Remote_LED, remote_PWMLED, Remote_xxx,
    #where xxx is the name of a supported gpiozero device

    remote_pin.on(on_time=2) # (Optional) Time in seconds until switch off
    remote_pin.blink() # Blink LED
    remote_pin.pulse() # Pulse LED
    remote_pin.off()
    remote_server.close()

    for more concrete examples study controller.py
```

### Use Board numbering
```
remote_pin = remote_LED(remote_server,ident,map_bg(7, 'b')) # Use physical board numbering
```
### Use GPIO numbering (default)
```
remote_pin = remote_LED(remote_server,ident,4) # Use GPIO numbering (e.g. GPIO4)
```



