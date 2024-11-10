#!/usr/bin/env python3
import socket
from multiprocessing import Process, Queue, Event, Lock,Pipe, current_process,parent_process                       
import time
import logging
from remoteio import PORT, evalAllowed
import threading 
from gpiozero import * 
from colorzero import Color,Red,Green,Blue
from gpiozero.tones import Tone
import warnings   

logging.basicConfig(level=logging.DEBUG,
                      format="%(asctime)s [%(levelname)-8s] [%(module)s:%(funcName)s]: %(message)s",
                      datefmt="%d.%m.%Y %H:%M:%S")
#logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}][{funcName:8},{lineno}]{message}")
logger = logging.getLogger(name="remoteio")
logger.setLevel(logging.DEBUG)
#####################################################

def LEDBoardValue(**kwargs):
   return tuple(kwargs.values())


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
########################################################
# timeout functions
def led_off(led:LED):
    led.off()  

def timeOut(obj_type, command):
    logger.info(f"({obj_type},{command}) timed out")
#######################################################################
########################################################################    
########################################################################   
def create_PinDevice(Dict:dict):
    warnings.simplefilter('ignore')
    led=None

    try:
        
        #### Dict1 only with parameters of interest for _create
        Dict1=Dict.copy()
        obj_type=Dict1.pop('obj_type')
        command=Dict1.pop('command')
        if command!='_create':
            raise LedGenError()

        numbering=Dict1.pop('numbering')
        pins=Dict1.pop('pins')
        if 'time_ms' in Dict1.keys():
            time_ms=Dict1.pop('time_ms')
        else:
            time_ms=0 

        
        ### initializing
        Klasse=eval(obj_type)
        match obj_type[0:3]:
            case 'MCP':
                '''
                clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8
                '''               
                Dict1['select_pin'] = pins[0]              
                led=Klasse(**Dict1)
            case _:
                led=Klasse(*pins,**Dict1)
        
        logger.info(f"{Dict} generated")
    except Exception as e:
        logger.info(str(e))
        logger.info(f"{Dict}  not generated")
        led=None
    finally:
        return led

  

########################################################################################################################
#############################################################
#############################################################
def handle_PinDevice(qu:Queue,ev,mode:str,lo,child_conn):
    '''
     realized as multiprocessing.Process 

    '''
    Dict=qu.get()[0]
    obj_type=Dict['obj_type']
    pins=Dict['pins']
    with lo:
        led=create_PinDevice(Dict) 
    if led==None:
        child_conn.send(f"?? {pins}")
    else:
        child_conn.send(f"! {pins}")

    ### continue with client data ###
    ### queue is empty here       ###
    try:
        while True: 
            ende=False 
            while qu.empty():
                # Soft reset and hard reset (e.g. by kill) are treated in the same manner.
                # 
                # Normally as long as any child process exists the parent process is alive.
                # But not when the parent process is killed or terminated.
                if ev.is_set() or not parent_process().is_alive():
                    ende=True
                    break
                time.sleep(0.005) # for that RPI not gets hot
            if ende==True:
                break

            if mode=='wait':
                # perform next task in queue
                Dict = qu.get()[0] 
            else:
                # perform last task in queue
                canc='cancelled before start'
                while not qu.empty():
                    Dict = qu.get()[0]
                    if not qu.empty():
                        logger.info(f"{Dict} {canc}") 

            #### Dict1 only with parameters of interest for led functions
            Dict1=Dict.copy()
            obj_type=Dict1.pop('obj_type')
            command=Dict1.pop('command')
            numbering=Dict1.pop('numbering')
            pins=Dict1.pop('pins')
            if 'time_ms' in Dict1.keys():
                time_ms=Dict1.pop('time_ms')
            else:
                time_ms=0
            time_sec=float(time_ms)/1000 
            try: 
                match command:
                    case 'set':
                        data='?S'
                        for key,item in Dict1.items():
                            setattr(led, key, item)
                            child_conn.send('!S')
                    case 'get':
                        try:
                            data ='!G{'
                            for x in Dict['property']:
                                func=getattr(led,x)
                                if (type(func)) not in evalAllowed:
                                    data+=f"'{x}' : '{str(func)}',"
                                else:
                                    data+=f"'{x}' : {func},"
                            if data!="!G{":
                                data=data[0:-1]
                            data+='}'
                            child_conn.send(data)
                        except:
                            data='?G'
                            raise ValueError("failure in get task")
                    case 'close':
                        data='?F'
                        ev.set()
                        child_conn.send('!F')
                        
                    case _:
                        data='?E'
                        func=getattr(led,command)
                        if Dict1=={}:
                            func()
                        else:
                            if 'args' not in Dict1.keys():
                                func(**Dict1)
                            else:
                                args=Dict1.pop('args')
                                if Dict1=={}:
                                    func(*args)
                                else:
                                    func(*args,**Dict1)
                    
                        child_conn.send('!E')

                if command in ('get','set'):
                    logger.debug(f"{Dict}")
                else:
                    logger.info(f"{Dict}") 

            except Exception as e:
                logger.info(str(e))
                logger.info(f"{e.__class__}: {str(e)}")
                logger.info(f"handle_PinDevice: {pins} ({numbering}) {command}: command error or property not supported")
                child_conn.send(data)
                continue

            canc=''
            if time_sec > 0.:
                if mode=='wait':
                    time.sleep(time_sec)
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
            if canc != '':
                logger.info(f"{Dict} {canc}")   

    except Exception as e:
        logger.error(f"handle_PinDevice: {pins}: {str(e)}")
    finally:
        if not (led is None):
            with lo:
                try:
                    led.close()
                except:
                    logger.error(f"close von {pins} device failed") 
            logger.info(f"handle_PinDevice: Released pin {pins}")
        logger.info(f"Handle_PinDevice of pin {pins} (g) terminated")        
    
################################################################  
def get_pinParams(pinParams:str)->dict:

    Dict={}
    if pinParams!='':
        obj_type,sep,datao=pinParams.partition(' ')
        command,sep, datac=datao.partition(' ')           
        numbering,sep, datan = datac.partition(' ')
        pins,sep, datap= datan.partition(') ')
        pins+=')'
        if not numbering =='g':
            raise ValueError('numbering must be (g)')

        Dict['obj_type']=obj_type
        Dict['command']=command
        Dict['numbering']=numbering
        Dict['pins'] = eval(pins)
        
        # named parameter from client
        if datap !='': 
            x=datap.split(';')
            for y in x:
                ## first = sign considered
                a,sep,b=y.partition('=')              
                Dict[a]=eval(b)
                    
        return Dict
################################################################################

def dispatchPinDevice(conn,addr,client_port,mode,lo,led_dict,paramString):
    
    Dict=get_pinParams(paramString)
    obj_type=Dict['obj_type']
    command=Dict['command']
    pins=Dict['pins']
    # generates PinDevice as a process in multiprocessing context
    if not pins in led_dict.keys():
        ## verification that pins are not used
        for p in pins:
            for key in led_dict.keys():
                if p in key:
                    raise ValueError(f"dispatchPinDevice: {obj_type} {command} {pins} wrong use of pins")
        if command=='_create':                       
            #starting handle_led-process 
            pin_qu=Queue(maxsize=1024)
            # delegate creation of Pin-Device
            pin_qu.put([Dict]) 
            pin_ev=Event()  
            pin_conn, child_conn = Pipe(duplex=True)                    
            pin_proc=Process(target=handle_PinDevice, args=(pin_qu,pin_ev,mode,lo,child_conn)) 
            x=''
            for p in pins:
                x+=str(p) + '_'
            x=x[:-1]
            pin_proc.name=f"p_{x}_{addr[0]}_{client_port}"
            pin_proc.start()
                ### communication between parent process and child process
            
            # Receive message from the child process whether pins are owned by pin_proc
            # Receive challenged info from the child process 
            t=threading.Timer(2.0,timeOut,(obj_type,command))
            t.start()            
            while not pin_conn.poll():
                if t.is_alive():
                    pass
                else:
                    raise ValueError('pipe connection timed out by device creation')
            else:
                if t.is_alive():
                    t.cancel()
                    message = pin_conn.recv()
                    if message[0:1]=='!':
                        led_dict[pins]=[pin_qu,pin_ev,pin_conn,pin_proc]
                        conn.sendall('!C'.encode()) 
                    else:
                        ### queue is empty !!
                        pin_proc.kill()
                        conn.sendall(f"?? {pins} Led creation failure".encode())    
           
        else:
            conn.sendall(f"?I".encode())
            logger.info(f"dispatchPIN: {obj_type} {command} {pins} ignored")
            
        return

    ### pins in Led_dict.keys() ####
    if command=='_create':
        conn.sendall(f"?I".encode())
        logger.info(f"dispatchPIN: {pins} {command} ignored")
        return


    # Execute gpio action 
    while led_dict[pins][0].full():
        pass
    else:                
        led_dict[pins][0].put([Dict]) 
        ### Command-handling ##
        
        # Receive challenged info from the child process 
        t=threading.Timer(2.0,timeOut,(obj_type,command))
        t.start()            
        while not led_dict[pins][2].poll():
            if t.is_alive():
                pass
            else:
                message=f"?? pipe connection timed out {pins} {command}"
                conn.sendall(f"{message}".encode())
                 # kill concerned pin_process
                led_dict[pins][3].kill()
                led_dict.pop(pins)
                break
        else:
            if t.is_alive():
                t.cancel()
                message = led_dict[pins][2].recv()
                conn.sendall(f"{message}".encode())
                
         

    if command == 'close':
        #soft kill of handle_PinDevice
        #remove pin entry from led_dict
        if pins in led_dict.keys():
            led_dict[pins][1].set
            led_dict.pop(pins)
            return    

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
            while data1.count('\n') >= 1:
                datax,sep,data1=data1.partition('\n')  

                # positioning parameters
                obj_type,sep, dummy = datax.partition(' ')  
                dispatchPinDevice(conn,addr,client_port,mode,lo,led_dict,datax)

    except ValueError as e:
        logger.error('handle_client: ' + str(e.__class__) + str(e)) 
        error=True
    except Exception as e:
        logger.error('handle_client: '+ str(e.__class__) + str(e))
        error=True
    finally:
        if error:
           for pi in led_dict.keys():
            # clearing of all pin-queues
            clear_queue(led_dict[pi][0]) 
        # Cleanup actions on disconnect
        if conn:
            conn.close()
            logger.info(f"Disconnected from client (" + str(addr)+ '), client_port = ' + str(client_port))
        for pi,[qu,ev,co,proc] in led_dict.items():
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


