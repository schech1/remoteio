#!/usr/bin/env python3
import socket
from multiprocessing import Process, Queue, Event, Lock,Pipe, current_process,parent_process                       
import time
import logging
from remoteio import PORT, evalAllowed
from remoteio.remoteio_wrapper import *
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
def rdevice_off(rdevice:LED):
    rdevice.off()  

def timeOut(ident,obj_type, command):
    logger.info(f"({ident},{obj_type},{command}) timed out")

########################################################################    
########################################################################   
def create_Device(Dict:dict):
    warnings.simplefilter('ignore')
    rdevice=None

    try:
        
        #### Dict1 only with parameters of interest for _create
        Dict1=Dict.copy()
        ident=Dict1.pop('ident')
        obj_type=Dict1.pop('obj_type')
        Klasse=eval(obj_type)
        
        command=Dict1.pop('command')
        if command!='_create':
            raise LedGenError()
        if 'args' in Dict1.keys():
            args=Dict1.pop('args')
            ### initializing        
            rdevice=Klasse(*args,**Dict1)
        else:
            rdevice=Klasse(**Dict1)
        logger.info(f"{Dict} generated")

    except Exception as e:
        logger.info(str(e))
        logger.info(f"{Dict}  not generated")
        rdevice=None
    finally:
        return rdevice

  

########################################################################################################################
#############################################################
#############################################################
def handle_Device(qu:Queue,ev,lo,child_conn):
    '''
     realized as multiprocessing.Process 

    '''
    Dict=qu.get()[0]
    obj_type=Dict['obj_type']
    ident=Dict['ident']
    with lo:
        rdevice=create_Device(Dict) 
    if rdevice==None:
        child_conn.send(f"?? {ident}")
    else:
        child_conn.send(f"! {ident}")

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

            
            # perform next task in queue
            Dict = qu.get()[0] 

            #### Dict1 only with parameters of interest for rdevice functions
            Dict1=Dict.copy()
            obj_type=Dict1.pop('obj_type')
            command=Dict1.pop('command')
            ident=Dict1.pop('ident')

            try: 
                match command:
                    case 'set':
                        data='?S'
                        for key,item in Dict1.items():
                            setattr(rdevice, key, item)
                            child_conn.send('!S')
                    case 'get':
                        try:
                            data ='!G{'
                            for x in Dict['property']:
                                func=getattr(rdevice,x)
                                if (type(func)) not in evalAllowed:
                                    data+=f"'{x}' : \"{str(func)}\","
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
                        func=getattr(rdevice,command)
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
                logger.info(f"handle_Device: ({ident} ,{obj_type}) {command}: command error or property not supported")
                child_conn.send(data)
                continue

    except Exception as e:
        logger.error(f"handle_Device: {ident}: {str(e)}")
    finally:
        if not (rdevice is None):
            with lo:
                try:
                    rdevice.close()
                except:
                    logger.error(f"close von {ident} rdevice failed") 
            logger.info(f"handle_Device: Released rdevice {ident}")
        logger.info(f"Handle_Device of rdevice {ident} terminated")        
    
################################################################  
def get_rdeviceParams(rdeviceParams:str)->dict:

    Dict={}
    if rdeviceParams!='':
        ident,sep,datai=rdeviceParams.partition(' ')
        obj_type,sep,datao=datai.partition(' ') 
        command,sep, datac=datao.partition(' ')  
        Dict['ident']=ident         
        Dict['obj_type']=obj_type
        Dict['command']=command
        
        # named parameter from client
        if datac !='': 
            x=datac.split(';')
            for y in x:
                ## first = sign considered
                a,sep,b=y.partition('=')              
                Dict[a]=eval(b)    
        return Dict
################################################################################

def dispatchDevice(conn,addr,client_port,lo,rdevice_dict,paramString):
    
    Dict=get_rdeviceParams(paramString)
    ident=Dict['ident']
    obj_type=Dict['obj_type']
    command=Dict['command']

    # generates Device as a process in multiprocessing context
    if not ident in rdevice_dict.keys():
        ## verification that ident is not used 
        for key in rdevice_dict.keys():
                if ident == key:
                    raise ValueError(f"dispatchDevice: {ident} {obj_type} {command}  wrong use of ident")
        if command=='_create':                       
            #starting handle_rdevice-process 
            ident_qu=Queue(maxsize=1024)
            # delegate creation of Pin-Device
            ident_qu.put([Dict]) 
            ident_ev=Event()  
            ident_conn, child_conn = Pipe(duplex=True)                    
            ident_proc=Process(target=handle_Device, args=(ident_qu,ident_ev,lo,child_conn)) 
            ident_proc.name=f"proc_{ident}_{addr[0]}_{client_port}"
            ident_proc.start()
                ### communication between parent process and child process
            
            # Receive message from the child process whether ident is owned by ident_proc
            # Receive challenged info from the child process 
            t=threading.Timer(2.0,timeOut,(ident,obj_type,command))
            t.start()            
            while not ident_conn.poll():
                if t.is_alive():
                    pass
                else:
                    raise ValueError('pipe connection timed out by rdevice creation')
            else:
                if t.is_alive():
                    t.cancel()
                    message = ident_conn.recv()
                    if message[0:1]=='!':
                        rdevice_dict[ident]=[ident_qu,ident_ev,ident_conn,ident_proc]
                        conn.sendall('!C'.encode()) 
                    else:
                        ### queue is empty !!
                        ident_proc.kill()
                        conn.sendall(f"?? {ident} Led creation failure".encode())    
           
        else:
            conn.sendall(f"?I".encode())
            logger.info(f"dispatchDevice: {obj_type} {command} {ident} ignored")
            
        return

    ### ident in Led_dict.keys() ####
    if command=='_create':
        conn.sendall(f"?I".encode())
        logger.info(f"dispatchDevice: {ident} {command} ignored")
        return


    # Execute gpio action 
    while rdevice_dict[ident][0].full():
        pass
    else:                
        rdevice_dict[ident][0].put([Dict]) 
        ### Command-handling ##
        
        # Receive challenged info from the child process 
        t=threading.Timer(2.0,timeOut,(ident,obj_type,command))
        t.start()            
        while not rdevice_dict[ident][2].poll():
            if t.is_alive():
                pass
            else:
                message=f"?? pipe connection timed out {ident} {command}"
                conn.sendall(f"{message}".encode())
                 # kill concerned rdevice_process
                rdevice_dict[ident][3].kill()
                rdevice_dict.pop(ident)
                break
        else:
            if t.is_alive():
                t.cancel()
                message = rdevice_dict[ident][2].recv()
                conn.sendall(f"{message}".encode())
                
         

    if command == 'close':
        #soft kill of handle_Device
        #remove rdevice entry from rdevice_dict
        if ident in rdevice_dict.keys():
            rdevice_dict[ident][1].set
            rdevice_dict.pop(ident)
            return    

########################################################################################################################
#     
# Handle client requests
def handle_client(conn,addr,client_port,lo):
    '''
     realized as multiprocessing.Process  
    '''
    rdevice_dict={}
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
                ident,sep,dummy=datax.partition('\n')   
                dispatchDevice(conn,addr,client_port,lo,rdevice_dict,datax)

    except ValueError as e:
        logger.error('handle_client: ' + str(e.__class__) + str(e)) 
        error=True
    except Exception as e:
        logger.error('handle_client: '+ str(e.__class__) + str(e))
        error=True
    finally:
        if error:
           for ident in rdevice_dict.keys():
            # clearing of all rdevice-queues
            clear_queue(rdevice_dict[ident][0]) 
        # Cleanup actions on disconnect
        if conn:
            conn.close()
            logger.info(f"Disconnected from client (" + str(addr)+ '), client_port = ' + str(client_port))
        for ident,[qu,ev,co,proc] in rdevice_dict.items():
            ev.set()

#################################################################### 

def run_server(port=PORT):
    lo=Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))         
        server_socket.listen(5)

        logger.info(f"remoteio listening on port {port}...")

        while True:
            conn, addr = server_socket.accept()
            logger.info(f"Connection from {addr}")
            client_handler=Process(target=handle_client, args=(conn,addr,port,lo))
            client_handler.name='client_handler_' + str(addr[0])
            client_handler.start()

            
##########################################################################
##########################################################################
##########################################################################    

if __name__ == "__main__":
    import sys
    import multiprocessing as mp

    try: 

        run_server()

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

