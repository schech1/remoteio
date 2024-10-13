

import socket
from multiprocessing import Process, Queue, Event, Lock
import time
import logging
from remoteio import PORT 
import threading     

logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")

class QueueFullError(Exception):
    def __init__(self,string):
        self.__str__= string
        
class LedGenError(Exception):
    def __init__(self,string):
        self.__str__= string
        

#multiprocessing queue has no clear function
def clear_queue(qu):
    while not qu.empty():
        qu.get()

# target task function
def led_off(led):
    led.off()

def handle_led(pin,qu,ev,mode):
    import warnings
    warnings.simplefilter('ignore')
    from gpiozero import PWMLED

    led=None

    try:
        while True: 
            ende=False  
            while qu.empty():
                if ev.is_set():
                    ende=True
                    break
            if ende==True:
                break

            if mode=='wait':
                # perform next task in queue
                numbering, pin, command, time_ms, arg1, arg2 = qu.get() 
            else:
                # perform last task in queue
                canc='cancelled before start'
                while not qu.empty():
                    numbering, pin, command, time_ms, arg1, arg2 = qu.get()
                    if not qu.empty():
                        logger.info(f"Pin: {pin}({numbering}), State: {command}, " +
                                    f"Time: {time_ms}, Arg1: {arg1}. Arg2: {arg2} {canc}") 

            # the precedent led-process to the same led is perhaps alive. Waiting until it is destroyed  
         
            while led==None:
                try:
                    time.sleep(0.01)
                    led = PWMLED("BOARD"+pin, pin_factory=None)
                    logger.info('led for ' + pin + '(b) generated')
                    break
                except Exception as e:
                    pass
            if (led==None):
                raise LedGenError("Creation of PWMLED has failed")
            
            

            time_sec = float(time_ms) / 1000.0
            try:   
                match command:
                    case 'value':
                        led.value=float(arg1)                        
                    case 'blink':
                        led.blink(float(arg1),float(arg2))
                    case _:
                        func=getattr(led,command)
                        func()
            except:
                logger.info('command error: ' + command)
                continue

            canc=''
            if time_sec > 0.:
                if mode=='wait':
                    time.sleep(time_sec)
                    if qu.empty:
                        led.off()

                else:
                    t=threading.Timer(time_sec,led_off,[led])
                    t.start()
                    while t.is_alive():
                        if qu.empty():
                            pass                        
                        else:
                            t.cancel()
                            canc='cancelled during execution'
                            break
            logger.info(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}, Arg1: {arg1}. Arg2: {arg2} {canc}")    
   
    
    except LedGenError as e:
        logger.error(f"{pin}: str(e)")
    except Exception as e:
        if led is None:
            logger.error(f"{pin}: str(e)")
        else:
            logger.error(f"{pin}: str(e)")
            logger.error(f"Pin: {pin}({numbering}), State: {command}, Time: {time_ms}, Arg1: {arg1}. Arg2: {arg2}") 
    finally:
        if not (led is None):
            led.off()
            led.close() 
            logger.info(f"Released pin {pin}")
        logger.info(f"Handle_led of {pin} (b) terminated")        
    
########################################################################################################################
#     
# Handle client requests
def handle_client(conn,addr,client_port,mode):

    led_dict={}
    error=False
    data1=''
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            data1+=data
            while data1.count(' ') >= 6:               
                numbering,sep, datan = data1.partition(' ')
                pin,sep, datap= datan.partition(' ')
                command,sep, datac= datap.partition(' ')
                time_ms,sep, datat = datac.partition(' ')
                arg1, sep,dataa = datat.partition(' ')
                arg2, sep,data1 = dataa.partition(' ')               
                if not numbering =='b':
                    raise ValueError('numbering must be (b)')

                on_queue=False
                # Create or retrieve LED instance for the specified pin number
                if (pin not in led_dict.keys()):
                    pin_ev=Event()
                    pin_qu=Queue(maxsize=1024)                        
                    pin_proc=Process(target=handle_led, args=(pin,pin_qu,pin_ev,mode)) 
                    led_dict[pin]=[pin_qu,pin_ev,pin_proc]
                    led_dict[pin][0].put([numbering,pin,command,time_ms,arg1,arg2])
                    on_queue=True
                    pin_proc.start()
                
                # Execute gpio action 
                while led_dict[pin][0].full():
                    pass
                
                if on_queue==False:
                    led_dict[pin][0].put([numbering,pin,command,time_ms,arg1,arg2])                
            

    except ValueError as e:
        logger.error(e) 
        error=True
    except Exception as e:
        logger.error(e)
        error=True
    finally:
        if error:
           for pi in led_dict.keys():
            # clearing of all pin-queues
            clear_queue(pi)
            # forced led off
            led_dict[pi][0].put([numbering,pin,'off','0','0.','0.'])  
        # Cleanup actions on disconnect
        if conn:
            conn.close()
            logger.info(f"Disconnected from client (" + str(addr)+ '), client_port = ' + str(client_port))
        for pi,[qu,ev,proc] in led_dict.items():
            ev.set()
        

def run_server(port=PORT,mode='wait'):
    if (mode !='wait' and mode!='nowait'):
        raise ValueError('mode must be wait or nowait')
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))         
        server_socket.listen(5)

        logger.info(f"remoteio listening on port {port}...")

        while True:
            conn, addr = server_socket.accept()
            logger.info(f"Connection from {addr}")
            client_handler=Process(target=handle_client, args=(conn,addr,port,mode))
            client_handler.start()
    

if __name__ == "__main__":
    import sys
    try: 

        run_server(mode='wait')

        #server_8509=Process(target=run_server, args=(8509,'nowait'))
        #server_8509.start()
        #server_8510=Process(target=run_server, args=(8510,'wait'))
        #server_8510.start()
            
    except Exception as e:
        logger.error(e)
        sys.exit()


