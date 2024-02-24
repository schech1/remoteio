from remoteio import RemoteServer

if __name__ == "__main__":
    server_ip = "192.168.1.38"
    server_port = 1234

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = remote_server.pin(8, 'b')
    remote_pin.on(time_ms=2000) # Time until switch off
    remote_pin.blink() # Blink LED
    remote_pin.off()
    remote_server.close()