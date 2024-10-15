#!/usr/bin/env python3
import socket
from time import sleep 
   
from remoteio import PORT
from remoteio import PIN_MAP_gb

import logging
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")



class RemoteServer:  

    def __init__(self, server_ip, server_port=PORT):                                 
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self._pin_list=[]

    def map_g_to_b(self,pin_number,numbering):
        if numbering=='g':
            if pin_number in PIN_MAP_gb.keys():
                return PIN_MAP_gb[pin_number], 'b'
            else:
                raise ValueError('((g), ' + str(pin_number) + ') false')    
        if numbering == 'b':
            if pin_number in PIN_MAP_gb.values():
                return pin_number,numbering
            else:
                raise ValueError('((b), ' + str(pin_number) + ') false')
            
    def pin(self, pin_number, numbering='b'):
        pin_number_new,numbering_new = self.map_g_to_b(pin_number,numbering)
        for p in self._pin_list:
            if p.pin_number==pin_number_new and p.numbering==numbering_new:
                raise ValueError('(('+ str(numbering) + '), ' + str(pin_number) + ') already created as ' + 
                                 '((' + str(numbering_new) + '), ' + str(pin_number_new)+')')
            
        p = RemotePin(self.client_socket, pin_number_new, numbering_new)
        self._pin_list.append(p)
        return p

    def close(self): 
        sleep(1.0)   
        self.client_socket.close()

class RemotePin:
    
    def __init__(self, client_socket, pin_number, numbering):
        self.client_socket = client_socket
        self.pin_number = pin_number
        self.numbering = numbering
        self.state='off'
        self.time_ms = 0
        self.arg1=0.0
        self.arg2=0.0
        self.create()
    
    def execute(self):
        # data transfer
        data=''
        data += f"{self.numbering} {self.pin_number} {self.state} {self.time_ms} {self.arg1} {self.arg2} "
        self.client_socket.sendall(data.encode())
        ret=self.client_socket.recv(1024).decode()
        if not ret:
            raise RuntimeError('Server has terminated connection')
        if ret[0:1] =='?':
            if ret != f"? command ignored: {self.state}":
             raise RuntimeError(ret)


     
    def create(self):
        self.state='create'
        self.time_ms=0
        self.arg1=0.
        self.arg2=0.
        self.execute()

    def on(self, time_ms:int=0,arg1:float=0.0,arg2:float=0.0):
            self.state='on'
            self.time_ms=time_ms
            self.arg1=arg1
            self.arg2=arg2
            self.execute()
        
    def blink(self,time_ms:int=0,arg1:float=1.0,arg2:float=1.0):
        self.state='blink'
        self.time_ms=time_ms
        self.arg1=arg1
        self.arg2=arg2
        self.execute()
       
    def pulse(self, time_ms:int=0, arg1:float=0.0,arg2:float=0.0):
        self.state='pulse'
        self.time_ms=time_ms
        self.arg1=arg1
        self.arg2=arg2
        self.execute() 
    
    def value(self, time_ms:int=0, arg1:float=1.0):
        self.state='value'
        self.time_ms=time_ms
        self.arg1=arg1
        self.arg2=0.0
        self.execute() 

    def off(self,time_ms:int=0):
        self.state='off'
        self.time_ms=time_ms
        self.arg1=0.0
        self.arg2=0.0
        self.execute()

    def close(self):
        self.state='close'
        self.time_ms=0
        self.arg1=0.0
        self.arg2=0.0
        self.execute()

    


 


# Example usage:


if __name__ == "__main__":
    from time import sleep
    time = 2000
    server_ip = "raspy5"
    server_port = 8509
  
    
    # Create instance of remote Raspberry Pi
    #remote_server = RemoteServer(server_ip, server_port)
    
    #remote_pin = remote_server.pin(21, 'g')
    #remote_pin1 = remote_server.pin(38, 'b')

    z=0
    while z<10:   
        # Create instance of remote Raspberry Pi
        remote_server = RemoteServer(server_ip, server_port)
        remote_pin1 = remote_server.pin(38, 'b')
        remote_pin = remote_server.pin(21, 'g')
        #remote_pin1 = remote_server.pin(38, 'b') 
        # Demo features
        remote_pin.on(time_ms=4000) 
        remote_pin1.on(time_ms=4000) 
        sleep(4)
        #remote_pin.close()
        #remote_pin1.close()
        #sleep(4)
        remote_pin.off(time_ms=4000) 
        remote_pin1.off(time_ms=4000) 
        sleep(4)        

        remote_pin.blink(time_ms=4000)
        remote_pin1.blink(time_ms=4000)
        sleep(4)
        remote_pin.off (time_ms=4000)
        remote_pin1.off (time_ms=4000)
        sleep(4)

        remote_pin.pulse (time_ms=4000)
        remote_pin1.pulse (time_ms=4000)
        sleep(4)
        remote_pin.off (time_ms=4000)
        remote_pin1.off (time_ms=4000)
        sleep(4)
        remote_pin.blink(time_ms=4000,arg1=0.1,arg2=0.2)
        remote_pin1.blink(time_ms=4000,arg1=0.1,arg2=0.2)
        sleep(4)
        remote_pin.off (time_ms=4000)
        remote_pin1.off (time_ms=4000)
        sleep(4)
        remote_pin.value(time_ms=4000,arg1=0.1)
        remote_pin1.value(time_ms=4000,arg1=0.1)
        sleep(4)
        remote_pin.off (time_ms=4000)
        remote_pin1.off (time_ms=4000)
        sleep(4)
        remote_server.close()  
        z=z+1
    while True:
       pass
            

