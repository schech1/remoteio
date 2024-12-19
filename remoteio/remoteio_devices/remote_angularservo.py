#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName


from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_AngularServo(RemoteDigitalDevice):
    
    '''
    class Remote_AngularServo(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class AngularServo(
        pin: Any | None = None,
        *,
        initial_angle: float = 0,
        min_angle: int = -90,
        max_angle: int = 90,
        min_pulse_width: float = 1 / 1000,
        max_pulse_width: float = 2 / 1000,
        frame_width: float = 20 / 1000,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"AngularServo has 1 positional parameter")
        super().__init__(remote_server, 'AngularServo', **kwargs)
        

        self.functions=  ['close', 'detach', 'ensure_pin_factory', 'max', 'mid', 'min']
        self.readOnlyProperties= ['all', 'closed', 'frame_width', 'is_active', 'max_angle', 'max_pulse_width', 'min_angle', 
                                  'min_pulse_width', 'namedtuple', 'values']
        self.writeableProperties=['angle', 'pin_factory', 'pulse_width', 'source', 'source_delay', 'value']
        
    def detach(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def max(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def mid(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def min(self,**kwargs):
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
    def frame_width(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def max_angle(self):
        return self.getProperty(getFunctionName())
    @property
    def max_pulse_width(self):
        return self.getProperty(getFunctionName())
    @property
    def min_angle(self):
        return self.getProperty(getFunctionName())
    @property
    def min_pulse_width(self):
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
    def angle(self):
        return self.getProperty(getFunctionName())    
    @angle.setter
    def angle(self,wert):
        self.func_exec('set',angle=wert) 
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert) 
    @property
    def pulse_width(self):
        return self.getProperty(getFunctionName())    
    @pulse_width.setter
    def pulse_width(self,wert):
        self.func_exec('set',pulse_width=wert) 
    @property
    def source_delay(self):
        return self.getProperty(getFunctionName())    
    @source_delay.setter
    def source_delay(self,wert):
        self.func_exec('set',source_delay=wert)
    ## source, value are treated in superclass                               
                                  
if __name__=='__main__':

    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties 
    #l=AngularServo(16)
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
    
        rl=Remote_AngularServo(rs,21)
        print(rl.all)
        rl.max()
        sleep(4)
        rl.mid()
        print(rl.pulse_width)
        print(rl.max_pulse_width)
    
        sleep(4)
        rl.min()
        print(rl.is_active)
        sleep(4)
        rl.angle=rl.max_angle
        sleep(5)
        pause() 
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")