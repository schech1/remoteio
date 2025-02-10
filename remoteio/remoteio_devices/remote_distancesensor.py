#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_DistanceSensor(RemoteDigitalDevice):
    '''
    class Remote_DistanceSensor(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class DistanceSensor(
        echo: Any | None = None,
        trigger: Any | None = None,
        *,
        queue_len: int = 9,
        max_distance: int = 1,
        threshold_distance: float = 0.3,
        partial: bool = False,
        pin_factory: Any | None = None
    )    
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==2:
                kwargs['args']=args
            else:
                raise ValueError(f"DistanceSensor has 2 positional parameter: echo, trigger")
        super().__init__(remote_server, 'DistanceSensor', **kwargs)

        self.functions= ['close', 'ensure_pin_factory', 'wait_for_active', 'wait_for_in_range', 'wait_for_inactive', 'wait_for_out_of_range']
        self.readOnlyProperties = ['active_time', 'closed', 'distance', 'echo', 'in_range', 'inactive_time', 'is_active', 
                                   'partial', 'pin', 'pull_up', 'queue_len', 'trigger', 'value', 'values']
        self.writeableProperties= ['ECHO_LOCK', 'max_distance', 'pin_factory', 'threshold', 'threshold_distance', 'when_activated', 
                                   'when_deactivated','when_in_range', 'when_out_of_range'] 
      
        self.whenDict={# when_function, when_thread, _when_thread_function,when_gen}
            'when_activated':       [None,None,self._when_thread_function,self.gen_when],
            'when_deactivated':     [None,None,self._when_thread_function,self.gen_when],
            'when_in_range':        [None,None,self._when_thread_function,self.gen_when],
            'when_out_of_range':    [None,None,self._when_thread_function,self.gen_when]}
        
        self.gen_wait_delay=0.01
        self.gen_when_delay=0.01
 
        
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    ## open, close are treated in super_class   

    ###############################################################
    ## wait_for... functions
    ################################################################  
    def wait_for_active(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
    def wait_for_in_range(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
    def wait_for_inactive(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)           
    def wait_for_out_of_range(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
   
    
    #############################################################
    ### The following generator is used in the super class.
    ### The _wait_task asks, whether the yields give True as response 
    #############################################################
    def gen_wait(self,wait_text):
        """
        generator function 
        An infinite iterator of values read from :attr:`...`
        """
        while True:
            try:
                sleep(self.gen_wait_delay) 
                match wait_text:
                    case 'wait_for_active':            
                        yield self.is_active
                    case 'wait_for_inactive':            
                        yield not self.is_active
                    case 'wait_for_in_range':            
                        yield not self.is_active
                    case 'wait_for_out_of_range':            
                        yield self.is_active
            except Exception:
                break

    ##########################################################
    ##########################################################
    #### properties only as getter 
    ##########################################################
    ##########################################################
    @property
    def active_time(self):
        return self.getProperty(getFunctionName())
    @property
    def closed(self):
        return self.getProperty(getFunctionName())
    @property
    def distance(self):
        return self.getProperty(getFunctionName())
    @property
    def echo(self):
        return self.getProperty(getFunctionName())
    @property
    def in_range(self):
        return self.getProperty(getFunctionName())
    @property
    def inactive_time(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def partial(self):
        return self.getProperty(getFunctionName())
    @property
    def pin(self):
        return self.getProperty(getFunctionName())
    @property
    def pull_up(self):
        return self.getProperty(getFunctionName())
    @property
    def queue_len(self):
        return self.getProperty(getFunctionName())
    @property
    def trigger(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest, value by super class

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################
    @property
    def ECHO_LOCK(self):
        return self.getProperty(getFunctionName())    
    @ECHO_LOCK.setter
    def ECHO_LOCK(self,wert):
        self.func_exec('set',ECHO_LOCK=wert)
    @property
    def max_distance(self):
        return self.getProperty(getFunctionName())    
    @max_distance.setter
    def max_distance(self,wert):
        self.func_exec('set',max_distance=wert)  
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert)    
    @property
    def threshold(self):
        return self.getProperty(getFunctionName())    
    @threshold.setter
    def threshold(self,wert):
        self.func_exec('set',threshold=wert)  
    @property
    def threshold_distance(self):
        return self.getProperty(getFunctionName())    
    @threshold_distance.setter
    def threshold_distance(self,wert):
        self.func_exec('set',threshold_distance=wert)  
    
    ## value is treated in the superclass   

    ###########################################################
    @property
    def when_activated(self):
        return self.whenDict[getFunctionName()][0]
    @when_activated.setter
    def when_activated(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    ###########################################################
    @property
    def when_deactivated(self):
        return self.whenDict[getFunctionName()][0]
    @when_deactivated.setter
    def when_deactivated(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    ###########################################################
    @property
    def when_in_range(self):
        return self.whenDict[getFunctionName()][0]
    @when_in_range.setter
    def when_in_range(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    
    #############################################################
    @property
    def when_out_of_range(self):
        return self.whenDict[getFunctionName()][0]
    @when_out_of_range.setter
    def when_out_of_range(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)  
    #############################################################
    ### The following generator is used in the super class.
    ### The _when_thread_function asks, whether the yields give True as response 
    #############################################################                            
    def gen_when(self,text,thread_dict):
        """
        A generator function
        An infinite iterator of values read from :attr:`value`, 'is_held'.
        """
        while not thread_dict[text][0]==None:
            try:
                sleep(self.gen_when_delay)
                if text=='when_activated':
                    yield self.is_active==True
                if text=='when_deactivated':
                    yield self.is_active==False
                if text=='when_out_of_range':
                    yield self.is_active==True
                if text=='when_in_range':
                    yield self.is_active==False
            except Exception:
                break 
                                
                                  
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties    
    #l=DistanceSensor(22,26)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

    try:
        from signal import pause
        from time import sleep
        from remoteio.remoteio_devices.remote_pwmled import Remote_PWMLED

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        from remoteio.remoteio_client import RemoteServer
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)

        def wmfunc(x):
            print(f"wm {x}")
        def wnmfunc(x):
            print(f"wnm {x}")#

        rl=Remote_DistanceSensor(rs,26,22)   
        rp=Remote_PWMLED(rs,21)
        print(rl.is_active)
        rp.source=rl
        rl.wait_for_in_range()

        print('A: '+ str(rl.is_active))
        rl.wait_for_out_of_range()
        print('B: '+str(rl.is_active))
        rl.when_in_range=wmfunc
        rl.when_out_of_range=wnmfunc
        
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")