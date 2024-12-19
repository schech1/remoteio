#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_MCP3208(RemoteDigitalDevice):
    
    '''
    class Remote_MCP3208(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP3208(
        channel: int = 0,
        differential: bool = False,
        max_voltage: float = 3.3,
        **spi_args: Any
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server,*args,**kwargs):
        # by the above definition of MCP3208 only named parameters are allowed
        if args!=():
            kwargs['args']=args
        super().__init__(remote_server, 'MCP3208', **kwargs)

        self.functions=    ['close', 'ensure_pin_factory']
        self.readOnlyProperties = ['bits', 'channel', 'closed', 'differential', 'is_active', 'max_voltage', 
                                   'raw_value', 'value', 'values', 'voltage']
        self.writeableProperties=['pin_factory']
      
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    ## open, close are treated in super_class   

    ##########################################################
    ##########################################################
    #### properties only as getter 
    ##########################################################
    ##########################################################
    @property
    def bits(self):
        return self.getProperty(getFunctionName())
    @property
    def channel(self):
        return self.getProperty(getFunctionName())
    @property    
    def closed(self):
        return self.getProperty(getFunctionName())
    @property
    def differential(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def max_voltage(self):
        return self.getProperty(getFunctionName())
    @property
    def raw_value(self):
        return self.getProperty(getFunctionName())
    @property
    def voltage(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest, value by super class

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
    
    ## value is treated in the superclass                               
                                  
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
#   #l=MCP3208(0,0)
#   #print(getFunctions(l))
#   #print(getReadOnlyProperties(l))
#   #print(getWriteableProperties(l))
#

    from remoteio.remoteio_devices.remote_pwmled import Remote_PWMLED
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

        ## in this example the mcp3208 gets its values from a photoresistor (Ky-018)
        ## rp gets lite when rl.value passes the threshold of 0.7
        ## look the following generator-function gen_ldr
        def gen_ldr():
            global rl
            while True:
                try:
                    sleep(0.1)
                    if rl.value>0.7:
                        yield 1.0
                    else:
                        yield 0.0
                except:
                    break

        rl=Remote_MCP3208(rs,0,port=0,device=1)  # GPIO Pin 7 is the select pin
        rp=Remote_PWMLED(rs,21)
        rp.source=gen_ldr

        while True:
            sleep(0.5)
            print(rl.value)
        
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")