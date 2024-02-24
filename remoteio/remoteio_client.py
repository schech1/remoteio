import socket

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

    def __create_command(self, command:str, time_ms:int=0):
        cmd = f"{command} {time_ms}"
        return cmd
    
    def __send_command(self, command):
        command = f"{self.numbering} {self.pin_number} {command}"
        self.client_socket.sendall(command.encode())
    
    def on(self, time_ms:int=0):
        cmd = self.__create_command("on", time_ms)
        self.__send_command(cmd)
        return self
    
    def blink(self):
        cmd = self.__create_command("blink")
        self.__send_command(cmd)
        return self
    
    def pulse(self):
        cmd = self.__create_command("pulse")
        self.__send_command(cmd)
        return self

    def off(self):
        cmd = self.__create_command("off")
        self.__send_command(cmd)
        return self




# Example usage:
if __name__ == "__main__":
    server_ip = "192.168.0.90"
    server_port = 8509

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = remote_server.pin(8, 'b')
    remote_pin.on(time_ms=2000) # Time in ms until switch off
    remote_pin.blink()
    remote_pin.on()  # Turn on the pin with the applied settings
    remote_pin.off()  # Turn off the pin
    remote_server.close()
 
