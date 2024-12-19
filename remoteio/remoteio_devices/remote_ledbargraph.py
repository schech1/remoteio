#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_LEDBarGraph(RemoteDigitalDevice):
    '''
    class Remote_LEDBarGraph(
        remote_server:RemoteServer,
        *args,
        **kwargs
    ) 
    class LEDBarGraph(
        *pins: Any,
        pwm: bool = False,
        active_high: bool = True,
        initial_value: float = 0,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            kwargs['args']=args
        super().__init__(remote_server,'LEDBarGraph', **kwargs)

        self.functions=           ['close', 'ensure_pin_factory', 'off', 'on', 'toggle']
        self.readOnlyProperties = ['active_high', 'all', 'closed', 'leds', 'namedtuple', 'values']
        self.writeableProperties= ['lit_count', 'pin_factory', 'source', 'source_delay', 'value'] 

    
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def off(self,*args,**kwargs):
        if 'args' not in kwargs.keys():
            kwargs['args']=args
            args=()
        if args!=():
            raise ValueError("could not transfer args to kwargs")
        self.func_exec(getFunctionName(),**kwargs)
    def on(self,*args,**kwargs):
        if 'args' not in kwargs.keys():
            kwargs['args']=args
            args=()
        if args!=():
            raise ValueError("could not transfer args to kwargs")
        self.func_exec(getFunctionName(),**kwargs) 
    
    def toggle(self,*args,**kwargs):
        if 'args' not in kwargs.keys():
            kwargs['args']=args
            args=()
        if args!=():
            raise ValueError("could not transfer args to kwargs")
        self.func_exec(getFunctionName(),**kwargs)
    ## open, close are treated in super_class   

    ##########################################################
    ##########################################################
    #### properties only as getter 
    ##########################################################
    ##########################################################
    @property
    def active_high(self):
        return self.getProperty(getFunctionName())
    @property
    def all(self):
        return self.getProperty(getFunctionName())
    @property
    def closed(self):
        return self.getProperty(getFunctionName())  
    @property
    def leds(self):
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
    def lit_count(self):
        return self.getProperty(getFunctionName())    
    @lit_count.setter
    def lit_count(self,wert):
        self.func_exec('set',lit_count=wert) 
    ###########################################################
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert)
    ###########################################################                    
    @property
    def source_delay(self):
        return self.getProperty(getFunctionName())    
    @source_delay.setter
    def source_delay(self,wert):
        self.func_exec('set',source_delay=wert)  
    ###########################################################

    ## source, value are treated in superclass  
                                 
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
    #l=LEDBoard(16,20,21)
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
        from remoteio.remoteio_devices.remote_mcp3208 import Remote_MCP3208
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)
                                  
        rl = Remote_LEDBarGraph(rs,16,20,21)
        #remote_mcp=Remote_MCP3208(rs,0,0)
        #print(remote_mcp.value)
        #rl.source=remote_mcp   # ok
        #pause()
    
        rl.value=1/2
        sleep(5)
        rl.value=-1/2
        sleep(5)
        rl.value=-2/2
        sleep(5)
        rl.value=1
        sleep(5)
        rl.off()
        #pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")