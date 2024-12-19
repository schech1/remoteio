#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_RGBLED(RemoteDigitalDevice):

    '''
    class Remote_RGBLED(
            remote_server:RemoteServer,
            *args,
            **kwargs
        ) 
    class RGBLED(
        red: Any | None = None,
        green: Any | None = None,
        blue: Any | None = None,
        *,
        active_high: bool = True,
        initial_value: Any = (0, 0, 0),
        pwm: bool = True,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs    
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==3:
                kwargs['args']=args
            else:
                raise ValueError(f"RGBLED has 3 positional parameter")

           
        super().__init__(remote_server, 'RGBLED', **kwargs)
        

        self.functions=  ['blink', 'close', 'ensure_pin_factory', 'off', 'on', 'pulse', 'toggle']
        self.readOnlyProperties= ['closed', 'is_active', 'is_lit', 'values']
        self.writeableProperties= ['blue', 'color', 'green', 'pin_factory', 'red', 'source', 'source_delay', 'value']

        
    def blink(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def off(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def on(self,**kwargs):
        if 'on_time' in kwargs.keys():
            self.blink(on_time=kwargs['on_time'],off_time=0,n=1)
        else:
            self.func_exec(getFunctionName(),**kwargs) 
    def pulse(self,**kwargs):
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
    def is_lit(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################
    @property
    def blue(self):
        return self.getProperty(getFunctionName())    
    @blue.setter
    def blue(self,wert):
        self.func_exec('set',blue=wert) 
    @property   
    def color(self):
        return self.getProperty(getFunctionName())    
    @color.setter
    def color(self,wert):
        self.func_exec('set',color=wert)
    @property
    def green(self):
        return self.getProperty(getFunctionName())    
    @green.setter
    def green(self,wert):
        self.func_exec('set',green=wert)
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert) 
    @property
    def red(self):
        return self.getProperty(getFunctionName())    
    @red.setter
    def red(self,wert):
        self.func_exec('set',red=wert) 
    @property
    def source_delay(self):
        return self.getProperty(getFunctionName())    
    @source_delay.setter
    def source_delay(self,wert):
        self.func_exec('set',source_delay=wert)  
    ## source, value are treated in superclass                               
                                  
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
    #l=RGBLED(16,20,21)
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
        
        #rl=Remote_RGBLED(rs,green=20,blue=16,red=21,pwm=True)  
        rl=Remote_RGBLED(rs,21,20,16,pwm=True)    #red,green,blue
        rl.blink()
        sleep(5)
        rl.pulse()
        sleep(5)
        rl.on(on_time=5.0)
        #pause()
        sleep(5)
        rl.off()
        sleep(5)
        rl.toggle()
        sleep(0.5)
        rl.value=(1.0,0,0)  # red, green,blue
        print(rl.value)
        rl.color="Color('yellow')"
        print(rl.value)
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")