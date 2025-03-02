#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

class Remote_LineSensor(RemoteDigitalDevice):
    '''
    class Remote_LineSensor(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class LineSensor(
        pin: Any | None = None,
        *,
        pull_up: bool = False,
        active_state: Any | None = None,
        queue_len: int = 5,
        sample_rate: int = 100,
        threshold: float = 0.5,
        partial: bool = False,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"LineSensor has 1 positional parameter")

        super().__init__(remote_server, 'LineSensor',**kwargs)

        self.functions=   ['close', 'ensure_pin_factory', 'wait_for_active', 'wait_for_inactive', 'wait_for_line', 'wait_for_no_line']
        self.readOnlyProperties =['active_time', 'closed', 'inactive_time', 'is_active', 'line_detected', 'partial', 'pin', 
                                  'pull_up', 'queue_len', 'value', 'values']
        self.writeableProperties=['pin_factory', 'threshold', 'when_activated', 'when_deactivated', 'when_line', 'when_no_line']
      
        self.whenDict={# when_function, when_thread, _when_thread_function,when_gen}
            'when_activated':   [None,None,self._when_thread_function,self.gen_when],
            'when_deactivated': [None,None,self._when_thread_function,self.gen_when],
            'when_line':        [None,None,self._when_thread_function,self.gen_when],
            'when_no_line':     [None,None,self._when_thread_function,self.gen_when]}
        
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
    def wait_for_inactive(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)           
    def wait_for_line(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
    def wait_for_no_line(self,**my_kwargs):
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
                    case 'wait_for_line':            
                        yield not self.is_active
                    case 'wait_for_no_line':            
                        yield  self.is_active
            except:
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
    def inactive_time(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def line_detected(self):
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
    @property
    def threshold(self):
        return self.getProperty(getFunctionName())    
    @threshold.setter
    def threshold(self,wert):
        self.func_exec('set',threshold=wert)  
    
    ## value is treated in the superclass   

    ###########################################################
    @property
    def when_activated(self):
        return self.whenDict[getFunctionName()][0]
    @when_activated.setter
    def when_activated(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    @property
    def when_deactivated(self):
        return self.whenDict[getFunctionName()][0]
    @when_deactivated.setter
    def when_deactivated(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    ###########################################################
    @property
    def when_line(self):
        return self.whenDict[getFunctionName()][0]
    @when_line.setter
    def when_line(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    @property
    def when_no_line(self):
        return self.whenDict[getFunctionName()][0]
    @when_no_line.setter
    def when_no_line(self, wert):
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
                if text=='when_line':
                    yield self.is_active==False
                if text=='when_no_line':
                    yield self.is_active==True
            except Exception:
                break 
                                
                                  
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties    
    #l=LineSensor(5)
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


        def wlfunc(x):
            print(f"wl {x}")
        def wnlfunc(x):
            print(f"wnl {x}")

        rl=Remote_LineSensor(rs,5,pull_up=True)   
        rp=Remote_PWMLED(rs,21)
        rl.threshold=0.6
        print(rl.threshold)
        rp.source=rl
        rl.wait_for_no_line()
        print('A')
        rl.wait_for_line()
        print('B')
        rl.when_line=wlfunc
        rl.when_no_line=wnlfunc
        
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")