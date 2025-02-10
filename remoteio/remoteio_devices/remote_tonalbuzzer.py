#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_TonalBuzzer(RemoteDigitalDevice):
    '''
    class TonalBuzzer(
    pin: Any | None = None,
    *,
    initial_value: Any | None = None,
    mid_tone: Tone = Tone("A4"),
    octaves: int = 1,
    pin_factory: Any | None = None
)
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"TonalBuzzer has 1 positional parameter")
        super().__init__(remote_server, 'TonalBuzzer', **kwargs)
        

        self.functions=  ['close', 'ensure_pin_factory', 'play', 'stop']
        self.readOnlyProperties= ['all', 'closed', 'is_active', 'max_tone', 'mid_tone', 'min_tone', 'namedtuple', 'octaves', 'values']
        self.writeableProperties=['pin_factory', 'source', 'source_delay', 'tone', 'value']

        
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def play(self,**kwargs):
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
    def max_tone(self):
        return self.getProperty(getFunctionName())
    @property
    def mid_tone(self):
        return self.getProperty(getFunctionName())
    @property
    def min_tone(self):
        return self.getProperty(getFunctionName())
    @property
    def namedtuple(self):
        return self.getProperty(getFunctionName())
    @property
    def octaves(self):
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
    @property
    def tone(self):
        return self.getProperty(getFunctionName())    
    @tone.setter
    def tone(self,wert):
        self.func_exec('set',tone=wert)   
    ## source, value are treated in superclass                               
                                  
if __name__=='__main__':
    
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
    #l=TonalBuzzer(16)
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
        from remoteio.remoteio_helper import map_bg
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)

        rl=Remote_TonalBuzzer(rs,pin=map_bg(40,'b'))
        #rl=Remote_TonalBuzzer(rs,map_bg(40,'b'))
        print(rl.all)
        rl.play(tone="Tone('A4')")
        sleep(4)
        rl.stop()
        sleep(10)
        rl.tone=220.0
        print(rl.tone)
        sleep(4)
        rl.stop()
        sleep(4)
        print(rl.tone)
        sleep(5)
        rl.tone=220.0
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")  