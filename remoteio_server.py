
import socket
from multiprocessing import Process, Queue, Event, Lock,Pipe, current_process,parent_process
                            
import time
import logging
from remoteio import PORT 
import threading 
from gpiozero import PWMLED
import warnings   
 
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")
#####################################################
class QueueFullError(Exception):
    def __init__(self,string):
        self.__str__= string
        
class LedGenError(Exception):
    def __init__(self,string):
        self.__str__= string
#######################################################
#multiprocessing queue has no clear function
def clear_queue(qu:Queue):
    while not qu.empty():
        qu.get()

# target task function
def led_off(led:PWMLED):
    led.off()

def create_led(pin:int)->PWMLED:
    warnings.simplefilter('ignore')
    led=None
    try:
        #time.sleep(0.01)
        led = PWMLED("BOARD"+pin, pin_factory=None)
        logger.info('led for ' + pin + '(b) generated')
    except Exception as e:
        logger.info('led for ' + pin + '(b) not generated')
        led=None
    finally:
        return led
#############################################################
#############################################################
def handle_led(pin:int,qu:Queue,ev,mode:str,lo):
    '''
     realized as multiprocessing.Process 

    '''
    with lo:
        led=create_led(pin)                   
    if led==None:
        qu.put(f"? {pin}")
    else:
        qu.put(f"! {pin}")   
    # wait until handl_client has evaluated the queue-data 
    while qu.qsize()==1:
        pass

    ### continue with client data ###
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
            
            time_sec = float(time_ms) / 1000.0
            try:   
                match command:
                    case 'value':
                        led.value=float(arg1)                        
                    case 'blink':
                        led.blink(float(arg1),float(arg2))
                    case 'close':
                        ev.set()
                    case _:
                        func=getattr(led,command)
                        func()
            except:
                logger.info('handle_client: command error: ' + command)
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
    except Exception as e:
        if led is None:
            logger.error(f"handle_led: {pin}: {str(e)}")
        else:
            logger.error(f"handle_led: {pin}: {str(e)}")
    finally:
        if not (led is None):
            led.off()
            with lo:
                led.close() 
            logger.info(f"handle_led: Released pin {pin}")
        logger.info(f"Handle_led of pin {pin} (b) terminated")        
    
########################################################################################################################
#     
# Handle client requests
def handle_client(conn,addr,client_port,mode,lo):
    '''
     realized as multiprocessing.Process  
    '''
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
                
                # Create or retrieve LED instance for the specified pin number
                if not pin in led_dict.keys():
                    if command=='create':                       
                        #starting handle_led-process 
                        pin_qu=Queue(maxsize=1024) 
                        pin_ev=Event()                      
                        pin_proc=Process(target=handle_led, args=(pin,pin_qu,pin_ev,mode,lo)) 
                        pin_proc.name=f"p_{pin}_{addr[0]}_{client_port}"
                        pin_proc.start()
                        while pin_qu.empty():
                            pass
                        x=pin_qu.get()
                        if x[0:1]=='!':
                            led_dict[pin]=[pin_qu,pin_ev]
                            conn.sendall('!'.encode()) 
                        else:
                            pin_proc.kill()
                            conn.sendall(f"? {pin} Led creation failure".encode())
                        continue
                    else:
                        conn.sendall(f"? command ignored: {command}".encode())
                        logger.info('handle_client: ' + pin  +' ' + command + ' ignored ' )
                        continue

                
                # Execute gpio action 
                while led_dict[pin][0].full():
                    pass
                else:                
                    led_dict[pin][0].put([numbering,pin,command,time_ms,arg1,arg2]) 
                    conn.sendall('! command on execution-queue'.encode())              
                if command == 'close':
                    #remove pin entry from led_dict
                    led_dict.pop(pin)
                    continue    
                

    except ValueError as e:
        logger.error('handle_client: ' + str(e)) 
        error=True
    except Exception as e:
        logger.error('handle_client: ' + str(e))
        error=True
    finally:
        if error:
           for pi in led_dict.keys():
            # clearing of all pin-queues
            clear_queue(led_dict[pi][0])
            # forced led off
            led_dict[pi][0].put([numbering,pin,'off','0','0.','0.'])  
        # Cleanup actions on disconnect
        if conn:
            conn.close()
            logger.info(f"Disconnected from client (" + str(addr)+ '), client_port = ' + str(client_port))
        for pi,[qu,ev] in led_dict.items():
            ev.set()
#################################################################### 

def run_server(port=PORT,mode='wait'):
    if (mode !='wait' and mode!='nowait'):
        raise ValueError('mode must be wait or nowait')
    
    lo=Lock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))         
        server_socket.listen(5)

        logger.info(f"remoteio listening on port {port}...")

        while True:
            conn, addr = server_socket.accept()
            logger.info(f"Connection from {addr}")
            client_handler=Process(target=handle_client, args=(conn,addr,port,mode,lo))
            client_handler.name='client_handler_' + str(addr[0])
            client_handler.start()
            
##########################################################################
##########################################################################
##########################################################################    

if __name__ == "__main__":
    import sys
    import multiprocessing as mp

    try: 

        run_server(mode='wait')

        #server_8509=Process(target=run_server, args=(8509,'nowait'))
        #server_8509.start()
        #server_8510=Process(target=run_server, args=(8510,'wait'))
        #server_8510.start()
    except KeyboardInterrupt as e:  
        logger.error(e)      
    except Exception as e:
        logger.error(e)
    finally:
        for child in mp.active_children():
            child.kill()
        sys.exit()

