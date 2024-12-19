#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_Button(RemoteDigitalDevice):
    
    '''
    class Remote_Button(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class Button(
        pin: Any | None = None,
        *,
        pull_up: bool = True,
        active_state: Any | None = None,
        bounce_time: Any | None = None,
        hold_time: int = 1,
        hold_repeat: bool = False,
        pin_factory: Any | None = None
    )    
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"Button has 1 positional parameter")
        super().__init__(remote_server, 'Button',**kwargs)
        

        self.functions=  ['close', 'ensure_pin_factory', 'wait_for_active', 'wait_for_inactive', 'wait_for_press', 'wait_for_release']
        self.readOnlyProperties= ['active_time', 'closed', 'held_time', 'inactive_time', 'is_active', 'is_held', 'is_pressed', 'pin', 
                                  'pressed_time', 'pull_up', 'value', 'values']
        self.writeableProperties= ['hold_repeat', 'hold_time', 'pin_factory', 'when_activated', 'when_deactivated', 'when_held', 
                                   'when_pressed', 'when_released']
        
        self.whenDict={# when_function, when_thread, _when_thread_function,when_gen}
            'when_activated':   [None,None,self._when_thread_function,self.gen_when],
            'when_deactivated': [None,None,self._when_thread_function,self.gen_when],
            'when_pressed':     [None,None,self._when_thread_function,self.gen_when],
            'when_released':    [None,None,self._when_thread_function,self.gen_when],
            'when_held':        [None,None,self._when_wh_function,self.gen_when]} 
        
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
    def wait_for_press(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
    def wait_for_release(self,**my_kwargs):
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
                    case 'wait_for_press':            
                        yield self.is_pressed
                    case 'wait_for_release':            
                        yield not self.is_pressed
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
    def held_time(self):
        return self.getProperty(getFunctionName())   
    @property
    def inactive_time(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def is_held(self):
        return self.getProperty(getFunctionName())
    @property
    def is_pressed(self):
        return self.getProperty(getFunctionName())
    @property
    def pin(self):
        return self.getProperty(getFunctionName())
    @property
    def pressed_time(self):
        return self.getProperty(getFunctionName())
    @property
    def pullup(self):
        return self.getProperty(getFunctionName())
    
    ##the generator 'values' situated on the remote server is not 
    # of interest, value is treated in superclass

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################   

    #############################################################    
    @property
    def hold_repeat(self):
        return self.getProperty(getFunctionName()) 
    @hold_repeat.setter
    def hold_repeat(self,wert):    
        self.func_exec('set',hold_repeat=wert)
    #############################################################    
    @property
    def hold_time(self):
        return self.getProperty(getFunctionName())   
    @hold_time.setter
    def hold_time(self,wert): 
        self.func_exec('set',hold_time=wert)
    ###################################################################
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert) 
    ## value is treated in superclass   
     
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
    ############################################################# 
    ###########################################################
    @property
    def when_pressed(self):
        return self.whenDict[getFunctionName()][0]
    @when_pressed.setter
    def when_pressed(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    @property
    def when_released(self):
        return self.whenDict[getFunctionName()][0]
    @when_released.setter
    def when_released(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    @property
    def when_held(self):
        return self.whenDict[getFunctionName()][0]
    @when_held.setter
    def when_held(self, wert):
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
        while not thread_dict[text][0]==None: #important as thread interrupt condition
            try:
                sleep(self.gen_when_delay)
                if text=='when_activated':
                    yield self.is_active==True
                if text=='when_deactivated':
                    yield self.is_active==False
                if text=='when_pressed':
                    yield self.value ==1
                if text=='when_released':
                    yield self.value == 0
                if text=='when_held':
                    yield self.is_held  
            except Exception:
                break
            
             
                               
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties
    #l=Button(16)
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

        def wpfunc(x):
                logger.info(f"wp {x}")
        def wrfunc(x):
            logger.info(f"wr {x}")
        def whfunc(x):
            logger.info(f"wh {x}")

        rl=Remote_Button(rs,5,hold_repeat=False,pull_up=True)
        rl.hold_time=1.0
        logger.info(rl.hold_time)
        rl.hold_repeat=True
        logger.info(rl.hold_repeat)
        #pause()
        sleep(1.0)
        x=rl.hold_repeat
        logger.info(x)
        rl.when_pressed=wpfunc
        rl.when_released=wrfunc
        rl.when_held=whfunc
        rl.wait_for_press()
        print('A')
        rl.wait_for_release()
        print('B')
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")