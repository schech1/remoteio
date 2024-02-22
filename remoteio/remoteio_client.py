import socket
import time

class RemoteServer:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

    def pin(self, pin_number, numbering='b'):
        return RemotePin(self.client_socket, pin_number, numbering)

    def close(self):
        self.client_socket.close()

class RemotePin:
    def __init__(self, client_socket, pin_number, numbering):
        self.client_socket = client_socket
        self.pin_number = pin_number
        self.numbering = numbering
        self.time_ms = 0

    def time(self, time_ms=0):
        self.time_ms = time_ms
        return self

    def on(self):
        self.send_command("on")
        return self

    def off(self):
        self.send_command("off")
        return self

    def send_command(self, status):
        command = f"{self.numbering} {self.pin_number} {status} {int(self.time_ms)}"
        self.client_socket.sendall(command.encode())


# Example usage:
if __name__ == "__main__":
    server_ip = "192.168.1.38"
    server_port = 8509

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = remote_server.pin(7, 'b') # Use BOARD numbering
    # remote_pin = remote_server.pin(4, 'g') # Use GPIO numbering
    remote_pin.time(2000) # Time in ms until switch off
    remote_pin.on()
   # remote_pin.off()
    remote_server.close()
