#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_PhaseEnableMotor(RemoteDigitalDevice):
    '''
    class Remote_Motor(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class PhaseEnableMotor(
    phase: int,
    enable: int,
    *,
    pwm: bool = True,
    pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer, *args,**kwargs):
        if args!=():
            if len(args)==2:
                kwargs['args']=args
            else:
                raise ValueError(f"PhaseEnableMotor has 2 positional parameter")
        super().__init__(remote_server, 'PhaseEnableMotor', **kwargs)
        

        self.functions=  ['backward', 'close', 'ensure_pin_factory', 'forward', 'reverse', 'stop']
        self.readOnlyProperties= ['all', 'closed', 'is_active', 'namedtuple', 'values']
        self.writeableProperties=['pin_factory', 'source', 'source_delay', 'value']
        
    def backward(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def forward(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def reverse(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def stop(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    ## open, close are treated in super_class   

    ##########################################################
    ##########################################################
    #### properties only as getter 
    ##########################################################
    ##########################################################
    @property
    def all(self):
        return self.getProperty(getFunctionName())
    @property
    def closed(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def namedtuple(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################   
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert) 
    @property
    def source_delay(self):
        return self.getProperty(getFunctionName())    
    @source_delay.setter
    def source_delay(self,wert):
        self.func_exec('set',source_delay=wert)
    ## source, value are treated in superclass 
    
                                  
if __name__=='__main__':
    
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
    #l=PhaseEnableMotor(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
    try:
        from signal import pause
        from time import sleep

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        from remoteio.remoteio_client import RemoteServer
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)

        rl=Remote_PhaseEnableMotor(rs,16,20)
        print(rl.all)
        rl.forward()
        sleep(4)
        rl.stop()
        
        rl.reverse()
        rl.backward(speed=0.5)
        print(rl.value)
        sleep(4)
        rl.backward()
        print(rl.value)
        print(rl.is_active)
        sleep(4)
        rl.stop()
        sleep(5)
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")