#!/usr/bin/env python3
import socket
from time import sleep 
import builtins
from gpiozero import Device 
from threading import Thread,Event,Timer
from multiprocessing import Lock
from remoteio import PORT, PIN_MAP_bg,getFunctionName

from typing import Generator
from inspect import isgeneratorfunction, signature, isfunction,ismethod
import logging
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")
logger.setLevel(logging.INFO)

def timeOut(obj_type, command):
    logger.info(f"({obj_type},{command}) timed out")


class RemoteServer:  
    def __init__(self, server_ip, server_port=PORT):                                 
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self._ident_list=[]
        ### synchronizing of access to tcp/Ip-connection by different threads
        self.conn_lock=Lock()

    def close(self): 
        sleep(1.0)   
        self.client_socket.close()

    

    def identExists(self,ident):
        ret=False
        for id in self._ident_list:
            if id==ident:
                ret=True
        return ret
    
############################################################
############################################################
############################################################
class RemotePinDevice:
    def __init__(self, remote_server, ident, obj_type, **kwargs):
        self.remote_server=remote_server
        self.client_socket=remote_server.client_socket
        self.command='off'
        self.ident=ident
        self.kwargs=kwargs
        self.obj_type=obj_type
        self._value=None
        self._closed=False
        self._source=None
        self._sourceThread=None
        self._sourceEvent=Event()
        self._source_delay=0.005


#############################################################    
#############################################################    
##  general functions
#############################################################
############################################################


    def _create(self):
        self.func_exec('_create',**self.kwargs)
        self._value=self.getProperty('value') 

    def get(self,**my_kwargs):
        for x in my_kwargs.keys():
            if x!='property':
                raise ValueError('only allowed key: property')
        ret=self.func_exec('get',**my_kwargs)
        return ret

    def set(self,**my_kwargs):
        '''
        my_kwargs:
        value=...
        '''
        self.func_exec('set',**my_kwargs)

    def close(self):
        self.command='close'
        if self._closed==True:
            raise ValueError("Device is closed!")
        my_kwargs={}
        self.func_exec('close',**my_kwargs)
        ## delete from _pin_list
        self.remote_server._ident_list.remove(self.ident)
        self._closed=True

    def open(self):
        self.command='open'
        ## is open ##
        if self._closed==False:
            raise ValueError("Device is open!")
        my_kwargs={}
        self.func_exec('_create',**my_kwargs)
        self.remote_server._ident_list.append(self.ident)
        self._closed=False

    def getProperty(self,my_property):
        try:
            return self.get(property=(my_property,))[my_property]
        except:
            return None
        
    def execute(self):
        # data transfer
        data=f"{self.ident} {self.obj_type} "
        data +=  f"{self.command} "
        
        match self.command:
            case 'get': # only verification
                if self.kwargs=={}: 
                    logger.info(f"{self.obj_type} {self.command} refused: no parameter ")
                    return None
                if len(self.kwargs) != 1: 
                    logger.info(f"{self.obj_type} {self.command} refused: exact one parameter allowed")
                    return None
                if 'property' not in self.kwargs.keys():
                    logger.info(f"{self.obj_type} {self.command} refused: expected property=(...)")
                    return None
                ## property=... expects a property as string or a list of properties as strings
                for value in self.kwargs.values():
                    if type(value)==str:
                        value=(value,)
                    if type(value)!=tuple:
                        logger.info(f"{self.obj_type} {self.command} refused: property must be tuple")
                        return None
                    data+=f"{'property'}={value};"
                data=data[0:-1]
                data+='\n'
            case 'set': 
                    if self.kwargs=={}: 
                        logger.info(f"{self.obj_type} {self.command} refused:no parameter")
                        return None
                    for key, value in self.kwargs.items():
                        data+=f"{key}={value};"
                    if self.kwargs!={}:
                        data=data[0:-1]
                        data+='\n'
                                
            case _: 
                for key, value in self.kwargs.items():
                    data+=f"{key}={value};"
                if self.kwargs!={}:
                    data=data[0:-1]
                data+='\n'

        with self.remote_server.conn_lock:
            self.client_socket.sendall(data.encode())
            self.client_socket.settimeout(3.0)
            ret=self.client_socket.recv(1024).decode()
            self.client_socket.settimeout(None)           
            if not ret:
                raise RuntimeError('Server has terminated connection')

            match ret[0:2]:
                case "??": 
                    logger.info(ret)
                    raise RuntimeError(ret)
                case "!G":
                    ### message to get-command from server ###   
                    return eval(ret[2:])
                case _:
                    return None
            
    def func_exec(self,name,**func_kwargs):
        self.command=name
        self.kwargs.clear()

        for key,value in func_kwargs.items():
            self.kwargs[key]=value
        ret=self.execute()
        return ret

####################################################################
## property source
####################################################################
    @property
    def source(self):
       ## time needed for aborting source_function-thread
        #sleep(0.002)
        return self._source
    @source.setter
    def source(self, quelle):
        self.command='source'
        if self._sourceThread !=None:
            #soft kill of thread
            self._sourceEvent.set()
            while self._sourceEvent.is_set():
                pass
            self._source=None
            self._sourceThread = None
        if quelle==None:   
            return
        if not issubclass(type(quelle),RemotePinDevice):
            if not issubclass(type(quelle),Device) and \
                not isinstance(quelle,Generator) and \
                not isgeneratorfunction(quelle):
               raise ValueError(f"Source {quelle} not supported")
            else:
                self._sourceThread=Thread(target=self.source_function, args=(quelle,self._sourceEvent),)
                self._sourceThread.start() 
                self._source=quelle
        else:
            self._sourceThread=Thread(target=self.source_function, args=(quelle.values,self._sourceEvent))
            self._sourceThread.start() 
            self._source=quelle

             
    def source_function(self,quelle,ev):
        ## infinite generator expected
        try:
            old_value=None    
            if issubclass(type(quelle),Device):
                xxx=quelle.values
            else:
                if isinstance(quelle,Generator):
                    xxx=quelle
                else:
                    if isgeneratorfunction(quelle):
                        xxx=quelle()
                    else:
                        raise ValueError(f"Source {quelle} not supported")
            
            for wert in xxx:
                if wert!=old_value:
                    self.value=wert
                    old_value=wert
                if ev.is_set():
                    break
                    
        except Exception as e:
            logger.info(str(e))
        finally:
            ev.clear()
###########################################################
    @property
    def value(self): 
        self._value=self.getProperty('value') 
        return self._value 
    @value.setter
    def value(self, wert):     
        self.func_exec('set',value=wert)
        self._value=wert
#############################################################
    @property
    def values(self):
        """
        An infinite iterator of values read from :attr:`value`.
        """
        while True:
            try:
                sleep(self._source_delay)           
                yield self.value
            except Exception:
                break
##########################################################################
##########################################################################

class RemoteDigitalDevice(RemotePinDevice):
    def __init__(self, remote_server, ident, obj_type, *args,**kwargs):          
        RemotePinDevice.__init__(self,remote_server, ident, obj_type, *args, **kwargs)
        remote_server._ident_list.append(ident)

        ## for some necessary locking
        self._Lock = Lock()
        self._create()
 
#############################################################
### parametrizable methods for when_... properties
#############################################################
    def _when_task(self,when_text,wert,thread_dict):
        if wert==None:
           thread_dict[when_text][0]=None
           return 
        if not (isfunction(wert) or ismethod(wert)):
           raise TypeError(f"{wert.__name__} is not a function and not a method")        
        sig = signature(wert)   
        count_positional=0
        for name, param in sig.parameters.items():
            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                count_positional=+1
        if count_positional>1:
            raise TypeError('more than 1 positional(mandatory) parameters')
        
        if not thread_dict[when_text][1] is None:
            thread_dict[when_text][0]=None
            while thread_dict[when_text][1]!= None and thread_dict[when_text][1].is_alive():
                pass
        thread_dict[when_text][0]=wert
        thread_dict[when_text][1]=Thread(target=thread_dict[when_text][2], args=(when_text,wert,thread_dict),)
        try:
            thread_dict[when_text][1].start() 
        except:
            thread_dict[when_text][0]=None
            logger.info(f"{when_text} = {str(wert)} has failed")

    def _when_thread_function(self,when_text,func,thread_dict):
        try:
            old_value=None
            for value in thread_dict[when_text][3](when_text,thread_dict):
                #starting condition
                if old_value==None:
                    old_value=value
                    continue
                else:
                    #change situation
                    if old_value!=value:
                        if value == True:
                                if not func is None:  
                                    wp=0
                                    sig = signature(func)
                                    for name, param in sig.parameters.items():
                                        if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                            wp=+1
                                            break
                                    if wp==0:
                                        func()
                                    else:
                                        func(self)
                                else:
                                    break
                        else:
                            pass
                        old_value=value
        except Exception as e:
            logger.error(f"{str(e)}")
        finally:
            thread_dict[when_text][0]=None
            thread_dict[when_text][1]=None     
            
##################################################################
## special treatment for when_held
##################################################################
    def _when_wh_function(self,when_text,func,thread_dict):
        try:
            for value in thread_dict[when_text][3](when_text,thread_dict):
                if value==True:
                    if not func is None:
                        wh=0
                        sig = signature(func)
                        for name, param in sig.parameters.items():
                            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                wh=+1
                                break
                        if self.hold_repeat:
                            while not thread_dict[when_text][0] is None:
                                if wh==0:
                                    func()
                                else:
                                    func(self)
                                sleep(self.hold_time)
                            else:
                                break
                        else:
                            if wh==0:
                                func()
                            else:
                                func(self)
                            self.wait_for_release()
                        if thread_dict[when_text][0] == None:
                            break
                    else:
                        thread_dict[when_text][0] = None
                        break
                   
        except Exception as e:
            logger.error(f"{str(e)}")
        finally:
            thread_dict[when_text][0] = None
            thread_dict[when_text][1] = None
#########################################################################
## for parametrizing of wait_for... funtions
#########################################################################
    def _wait_task(self,wait_text,gen_function,**my_kwargs):
        if 'timeout' in my_kwargs.keys():
            if not my_kwargs['timeout'] is None:
                t=Timer(my_kwargs['timeout'],timeOut,(self.obj_type,wait_text))
                t.start()
                while t.is_alive(): 
                    for value in gen_function(wait_text):
                        if value==True:
                            t.cancel()
                            return 0
                        break
                else:
                    return 1   
        for value in gen_function(wait_text):
            if value==True:
                return 0

    
