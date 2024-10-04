
import socket
import threading

PORT=8509   

pin_map_gb={
    0:27,
    1:28,
    2:3,
    3:5,
    4:7,
    5:29,
    6:31,
    7:26,
    8:24,
    9:21,
    10:19,
    11:23,
    12:32,
    13:33,
    14:8,
    15:10,
    16:36,
    17:11,
    18:12,
    19:35,
    20:38,
    21:40,
    22:15,
    23:16,
    24:18,
    25:22,
    26:37,
    27:13
}



class RemoteServer:  

    def __init__(self, server_ip, server_port=PORT):   
        global my_server                                       
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self._pin_list=[]

    def map_g_to_b(self,pin_number,numbering):
        if numbering=='g':
            return pin_map_gb[pin_number], 'b'
            
        if numbering == 'b':
            if pin_number in pin_map_gb.values():
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
        remote_pin=remote_pi.pin(21,'g')
        remote_pin1=remote_pi.pin(20,'g')
        remote_pin2=remote_pi.pin(16,'g')


        
        while True:
            remote_pin.on()
            remote_pin1.pulse()
            remote_pin2.blink()
            time.sleep(20.0)
        #remote_pin1.pulse()
        #remote_pin2.blink()

            
            
            #remote_pin1.off()
            #remote_pin2.off()

       
        while True:
            pass
    except Exception as e:
        logger.info(str(e))
    finally:
        if remote_pi:
            remote_pi.close()
