from remoteio import RemoteServer

if __name__ == "__main__":
    server_ip = "192.168.1.38"
    server_port = 1234

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = remote_server.pin(7, 'b')
    remote_pin.time(2000)
    remote_pin.on()
    remote_server.close()