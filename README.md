# remoteio
A Raspberry Pi GPIO remote control based on gpiozero


## Installation
Use this all-in-one command to install remoteio as deamon on port `8509`.
If remoteio is already installed, this command will update all files.
```
bash -c "$(wget -qLO - https://github.com/schech1/remoteio/raw/master/install.sh)"

```

## Client usage

```
server_ip = "192.168.1.38"
server_port = 8509
remote_server = RemoteServer(server_ip, server_port)
```

### Use Board numbering
```
remote_pin = remote_server.pin(7, 'b') # Use physical board numbering
```
### Use GPIO numbering
```
remote_pin = remote_server.pin(7, 'g') # Use GPIO numbering (e.g. GPIO7)
```

```
# Time in ms until switch off
remote_pin.time(2000) 

# Turn on the pin with the applied settings
remote_pin.on()   

# Turn off the pin
remote_pin.off()  

remote_server.close()

```
