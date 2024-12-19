#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_LEDBoard(RemoteDigitalDevice):
    '''
    class Remote_LEDBoard(
        remote_server:RemoteServer,
        *args,
        **kwargs
    ) 
    class LEDBoard(
        ...,
        pwm: bool = False,
        active_high: bool = True,
        initial_value: bool = False,
        _order: Any | None = None,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            kwargs['args']=args
        super().__init__(remote_server, 'LEDBoard', **kwargs)

        self.functions=           ['blink', 'close', 'ensure_pin_factory', 'off', 'on', 'pulse', 'toggle']     
        self.readOnlyProperties = ['active_high', 'all', 'closed', 'is_active', 'is_lit', 'leds', 'namedtuple', 'values']
        self.writeableProperties= ['pin_factory', 'source', 'source_delay', 'value'] 

    
    def blink(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
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
    def pulse(self,**kwargs):
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
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def is_lit(self):
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
    ############################################### 
    def LEDBoardValue(self,**kwargs):
        return tuple(kwargs.values())
    @property
    def value(self):
        # This is the call to the original set method 
        x = RemoteDigitalDevice.value.fget(self) 
        return eval('self.' + str(x)) 
    @value.setter
    def value(self,wert):
        # This is the call to the original set method 
        RemoteDigitalDevice.value.fset(self, wert)     
    ################################################
    ## source is treated in superclass   
    ## value property of superclass is here overwritten                            

if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
    #l=LEDBoard(20,21)
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

    

        # _order in combination with named leds defines how the property value has to be interpreted.
        # here value=(led1.value,led2.value,led3.value)
        #rl=Remote_LEDBoard(rs,led2=16,led1=20,led3=21,pwm=True,_order=('led1','led2','led3'))
        #rl.value=(1,0,1) # pin20,pin16,pin21
        #logger.info(RemoteDigitalDevice.value.fget(rl))
        #pause()

        rl=Remote_LEDBoard(rs,16,20,21,pwm=True)
        rl.value=(1,0,1) # pin 16,20,21
        logger.info(RemoteDigitalDevice.value.fget(rl))  # anonymeous alphabetic order
        logger.info(rl.value)
        print(rl.is_active)
        rl.blink()
        sleep(10)
        rl.off()
        print(rl.active_high)
        rl.on(1,-1)
        print(rl.is_active)
        sleep(10)
        rl.off(-1)
        sleep(10)
        rl.toggle(0,1)
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")