from remoteio import RemoteServer
from time import sleep

if __name__ == "__main__":
    time = 2000
    server_ip = "192.168.1.38"
    server_port = 1234

    # Create instance of remote Raspberry Pi
    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = remote_server.pin(8, 'b')

    # Demo features
    remote_pin.on(time_ms=time) # Time until switch off
    sleep(time/1000)
    remote_pin.blink()
    sleep(1)
    remote_pin.pulse()
    sleep(1)
    remote_pin.blink(arg1=0.1,arg2=0.2)
    sleep(1)
    remote_pin.value(arg1=0.5)
    sleep(1)
    remote_pin.off()
    remote_server.close()
