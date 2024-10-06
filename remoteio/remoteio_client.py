
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
    
    def execute(self):
        # data transfer
        data=''
        data += f"{self.numbering} {self.pin_number} {self.state} {self.time_ms} "
        self.client_socket.sendall(data.encode())

     
    def on(self, time_ms:int=0):
        self.state='on'
        self.time_ms=time_ms
        self.execute()
    
    def blink(self, time_ms:int=0):
        self.state='blink'
        self.time_ms=time_ms
        self.execute()
       
    def pulse(self, time_ms:int=0):
        self.state='pulse'
        self.time_ms=time_ms
        self.execute() 

    def off(self):
        self.state='off'
        self.time_ms=0
        self.execute()

    def close(self):
        self.state='close'
        self.time_ms=0
        self.execute()
    


 


# Example usage:
if __name__ == "__main__":
    import logging
    import time
    
    try:  
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(name="remoteio")
        raspi1='raspy5' 
        # erstellt virtuelle Pins auf 2 verschiedenen Raspberry Pis
        remote_pi=None
        remote_pi=RemoteServer(raspi1)


        # 'g ': BCM -B e z e i c h n u n g ( G P I O 2 1 )
        remote_pin=remote_pi.pin(40,'b')
        remote_pin1=remote_pi.pin(20,'g')
        remote_pin2=remote_pi.pin(16,'g')


        
        remote_pin.on(time_ms=10000)
        #remote_pin1.pulse()
        #remote_pin2.blink()

        
                    
        #remote_pin.off()
        #remote_pin1.off()
        #remote_pin2.off()

            

            

        #remote_pin.close()
        #remote_pin1.close()
        #remote_pin2.close()
        #remote_pin1.pulse()
        #remote_pin2.blink()

            
            
            #remote_pin1.off()
            #remote_pin2.off()

       
        while True:
            pass
    except Exception as e:
        logger.error(e)
    finally:
        if remote_pi:
            remote_pi.close()
