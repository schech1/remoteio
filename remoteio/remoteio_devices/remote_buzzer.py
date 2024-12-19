#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_Buzzer(RemoteDigitalDevice):
    '''
    class Remote_RGBLED(
            remote_server:RemoteServer,
            *args,
            **kwargs
        ) 
    class Buzzer(
    pin: Any | None = None,
    *,
    active_high: bool = True,
    initial_value: bool = False,
    pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs 
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"Buzzer has 1 positional parameter")

        super().__init__(remote_server, 'Buzzer', **kwargs)
        

        self.functions=  ['beep', 'blink', 'close', 'ensure_pin_factory', 'off', 'on', 'toggle']
        self.readOnlyProperties= ['closed', 'is_active', 'pin', 'values']
        self.writeableProperties=['active_high', 'pin_factory', 'source', 'source_delay', 'value']

        
    def beep(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def blink(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def off(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def on(self,**kwargs):
        if 'on_time' in kwargs.keys():
            self.beep(on_time=kwargs['on_time'],off_time=0,n=1)
        else:
            self.func_exec(getFunctionName(),**kwargs)
    def toggle(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    ## open, close are treated in super_class   

    ##########################################################
    ##########################################################
    #### properties only as getter 
    ##########################################################
    ##########################################################
    @property
    def closed(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def pin(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################

    @property
    def active_high(self):
        return self.getProperty(getFunctionName())    
    @active_high.setter
    def active_high(self,wert):
        self.func_exec('set',active_high=wert) 
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
    #l=Buzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    # 
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
    
        rl=Remote_Buzzer(rs,21)
        rl.beep()
        sleep(8)
        rl.blink()
        sleep(5)
        rl.on(on_time=5)
        sleep(5)
        rl.off()
        sleep(5)
        rl.toggle()
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")