#!/usr/bin/env python3
import socket

   
from remoteio import PORT
from remoteio import PIN_MAP_gb




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
    
    def execute(self):
        # data transfer
        data=''
        data += f"{self.numbering} {self.pin_number} {self.state} {self.time_ms} {self.arg1} {self.arg2} "
        self.client_socket.sendall(data.encode())

     
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
    
    def value(self, time_ms:int=0, arg1:float=1.0,arg2:float=0.0):
        self.state='value'
        self.time_ms=time_ms
        self.arg1=arg1
        self.arg2=arg2
        self.execute() 

    def off(self):
        self.state='off'
        self.time_ms=0
        self.arg1=0.0
        self.arg2=0.0
        self.execute()

    


 


# Example usage:
if __name__ == "__main__":
    import logging
    import time
    remote_pi=None
    remote_pi1=None
    
    try: 
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(name="remoteio")
        raspi1='raspy5' 
        # erstellt virtuelle Pins auf 2 verschiedenen Raspberry Pis
        # 

        #remote_pi=RemoteServer(raspi1,8509)
        #remote_pi1=RemoteServer(raspi1,8510)

        # 'g ': BCM -B e z e i c h n u n g ( G P I O 2 1 )
        #remote_pin=remote_pi.pin(21,'g')
        #remote_pin1=remote_pi1.pin(20,'g')
        #remote_pin2=remote_pi1.pin(36,'b') 

        
            
        #remote_pi=RemoteServer(raspi1,8509)
        #remote_pin=remote_pi.pin(21,'g')
        #remote_pin1=remote_pi1.pin(20,'g')
        #remote_pin2=remote_pi1pin(36,'b') 

        remote_pi=RemoteServer(raspi1,8509)
        remote_pi1=RemoteServer(raspi1,8510)
        remote_pin=remote_pi.pin(21,'g')
        remote_pin1=remote_pi1.pin(20,'g')
        remote_pin2=remote_pi1.pin(36,'b') 

        for z in range(0,3):
            remote_pin.on(time_ms=4000)
            remote_pin.pulse(time_ms=4000,arg1=0.4)
            remote_pin.blink(time_ms=4000,arg1=01.0,arg2=0.5)
            remote_pin1.on(time_ms=4000)
            remote_pin1.pulse(time_ms=4000,arg1=0.4)
            remote_pin1.blink(time_ms=4000,arg1=01.0,arg2=0.5)
            remote_pin2.on(time_ms=4000)
            remote_pin2.pulse(time_ms=4000,arg1=0.4)
            remote_pin2.blink(time_ms=4000,arg1=01.0,arg2=0.5)
        
        while True:
            pass
            #remote_pi.close()
            #time.sleep(1.0)
            #remote_pi.close()
            #time.sleep(15.0)
        
        
        
    except Exception as e:
        logger.error(e)
    finally:
        pass
        #if remote_pi:
        #    remote_pi.close()
        #if remote_pi1:
        #    remote_pi1.close()
