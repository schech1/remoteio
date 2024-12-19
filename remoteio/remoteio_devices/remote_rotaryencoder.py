#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_devices.remote_button import Remote_Button
from remoteio.remoteio_helper import getFunctionName, shortestWay

from multiprocessing import Lock

from time import sleep
import logging
logger = logging.getLogger(__name__)


class Remote_RotaryEncoder(RemoteDigitalDevice):
    
    '''
    class Remote_RotaryEncoder(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class RotaryEncoder(
        a: int,
        b: int,
        *,
        bounce_time: Any | None = None,
        max_steps: int = 16,
        threshold_steps: Any = (0, 0),
        wrap: bool = False,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    '''

    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            if len(args)==2:
                kwargs['args']=args
            else:
                raise ValueError(f"RotaryEncoder has 2 positional parameter: a,b (named CLK,DT on the hardware-device)")

        super().__init__(remote_server,'RotaryEncoder', **kwargs)

        self.functions=             ['close', 'ensure_pin_factory', 'wait_for_active', 'wait_for_inactive', 'wait_for_rotate',
                                    'wait_for_rotate_clockwise', 'wait_for_rotate_counter_clockwise']  
        self.readOnlyProperties =   ['active_time', 'all', 'closed', 'inactive_time', 'is_active', 'max_steps', 'namedtuple', 
                                    'threshold_steps','values', 'wrap']
        self.writeableProperties=   ['TRANSITIONS', 'pin_factory', 'steps', 'value', 'when_activated', 'when_deactivated', 
                                    'when_rotated', 'when_rotated_clockwise', 'when_rotated_counter_clockwise']
      
        self.whenDict={# when_function, when_thread, _when_thread_function,when_gen}
            'when_activated':                   [None,None,self._when_thread_function,self.gen_when],
            'when_deactivated':                 [None,None,self._when_thread_function,self.gen_when],
            'when_rotated':                     [None,None,self._when_thread_function,self.gen_when],
            'when_rotated_clockwise':           [None,None,self._when_thread_function,self.gen_when],
            'when_rotated_counter_clockwise':   [None,None,self._when_thread_function,self.gen_when]}
        
        self.gen_wait_delay=0.01
        self.gen_when_delay=0.01
 
        ## for Rotary Encoder
        self._rotary_lock=Lock()
        self._steps_saved_wr_c_cc= 0 
        self.counter=0
        self.SW=None

##########################################################
## special treatment for RotaryEncoder
##########################################################  
    def activateSW(self,pinNr,pull_up=True)->int:
        try:
            ret=1
            if self.SW!=None:
                raise ValueError("SW")
            # SW is given
            self.SW=Remote_Button(self.remote_server, pin=pinNr,pull_up=pull_up)
            ret=0
        except Exception as e:
            logger.error(f"{e.__class__}: {str(e)}")
            ret=1
        finally:
            return ret


    def reset_counter(self,x):
        with self._rotary_lock:
            self.counter=0


    def last_step(self,when_wait_text):
        with self._rotary_lock:
            Dict=self.func_exec('get',property=('steps','max_steps'))
            mem=Dict['steps']
            max=Dict['max_steps']
            incr_decr=shortestWay(self._steps_saved_wr_c_cc,mem,max)

            match when_wait_text:
                case 'wait_for_rotate':
                    if incr_decr != 0:
                        return True
                case 'wait_for_rotate_clockwise':
                    if incr_decr > 0:
                        return True
                case 'wait_for_rotate_counter_clockwise':
                    if incr_decr < 0:
                        return True            
                case 'when_rotated':
                    if incr_decr != 0:
                        return True
                case 'when_rotated_clockwise':
                    if incr_decr > 0:
                        self._steps_saved_wr_c_cc=mem
                        self.counter+= incr_decr
                        return True
                case 'when_rotated_counter_clockwise':
                    if incr_decr < 0:
                        self._steps_saved_wr_c_cc=mem
                        self.counter+= incr_decr
                        return True    
            return False
        

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
    def wait_for_rotate(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs) 
    def wait_for_rotate_clockwise(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)   
    def wait_for_rotate_counter_clockwise(self,**my_kwargs):
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
                    case 'wait_for_rotate':
                        yield self.last_step('wait_for_rotate')
                    case 'wait_for_rotate_clockwise':
                        yield  self.last_step('wait_for_rotate_clockwise')
                    case 'wait_for_rotate_counter_clockwise':
                        yield self.last_step('wait_for_rotate_counter_clockwise')
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
    def all(self):
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
    def max_steps(self):
        return self.getProperty(getFunctionName())
    @property
    def namedtuple(self):
        return self.getProperty(getFunctionName())
    @property
    def threshold_steps(self):
        return self.getProperty(getFunctionName())
    @property
    def wrap(self):
        return self.getProperty(getFunctionName())
    
    ##the generator values situated on the remote server is not 
    # of interest, value by super class

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################
    @property
    def TRANSITIONS(self):
        return self.getProperty(getFunctionName())    
    @TRANSITIONS.setter
    def TRANSITIONS(self,wert):
        self.func_exec('set',TRANSITIONS=wert)
    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())    
    @pin_factory.setter
    def pin_factory(self,wert):
        self.func_exec('set',pin_factory=wert)    
    @property
    def steps(self):
        return self.getProperty(getFunctionName())    
    @steps.setter
    def steps(self,wert):
        self.func_exec('set',steps=wert)  
    
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
    def when_rotated(self):
        return self.whenDict[getFunctionName()][0]
    @when_rotated.setter
    def when_rotated(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    @property
    def when_rotated_clockwise(self):
        return self.whenDict[getFunctionName()][0]
    @when_rotated_clockwise.setter
    def when_rotated_clockwise(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    @property
    def when_rotated_counter_clockwise(self):
        return self.whenDict[getFunctionName()][0]
    @when_rotated_counter_clockwise.setter
    def when_rotated_counter_clockwise(self, wert):
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
                match text:
                    case 'when_activated':
                        yield self.is_active==True
                    case 'when_deactivated':
                        yield self.is_active==False
                    case 'when_rotated':
                        yield self.last_step('when_rotated')
                    case 'when_rotated_clockwise':
                        yield  self.last_step('when_rotated_clockwise')
                    case 'when_rotated_counter_clockwise':
                        yield self.last_step('when_rotated_counter_clockwise')
            except Exception:
                break 
                                
                                  
if __name__=='__main__':
    #from remoteio.remoteio_helper import getFunctions,getReadOnlyProperties,getWriteableProperties    
    #l=RotaryEncoder(22,26)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

    try:
        from signal import pause
        from time import sleep
        from remoteio.remoteio_devices.remote_pwmled import Remote_PWMLED
        from remoteio.remoteio_helper import  map_bg

        import logging
        logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        from remoteio.remoteio_client import RemoteServer
        server_ip = "192.168.178.136"
        server_port = 8509
        # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)

        def wrfunc(x):
            #print(f"wr {rl.steps}")
            pass
        def wrcfunc(x):
            print(f"wrc steps: {rl.steps}")
            print(f"wrc counter: {rl.counter}")
        def wrccfunc(x):
            print(f"wrcc steps: {rl.steps}")
            print(f"wrcc counter: {rl.counter}")
            pass
        
        server_ip = "192.168.178.136"
        server_port = 8509
        
    # Create instance of remote Raspberry Pi
        rs = RemoteServer(server_ip, server_port)
        
        pin=map_bg(29,'b')  # GpioPin 5
        rl=Remote_RotaryEncoder(rs,a=19,b=26, wrap=True)           # CLK, DT
        rl.activateSW(pin,pull_up=True)                            # push button of the rotary encoder, default pull_up=True
        #or
        #rl.SW=Remote_Button(rs,pin,pull_up=True)                  # SW pullup=True expected by the rotary encoder used here

        rl.SW.when_pressed = rl.reset_counter           # this is a method not function, because dependent from rotary encoder object
                                                        # nevertheless well interpreted by gpiozero differently to the API of gpiozero
                                                        # where they ask for a function not for a method
        print(rl.SW.getClientIdent())                 
        rp=Remote_PWMLED(rs,21)
        print(rl.is_active)
        rl.when_rotated=wrfunc               # function
        rl.when_rotated_clockwise=wrcfunc    # function
        rl.when_rotated_counter_clockwise=wrccfunc # method
        rl._source_delay=0.02                 # generator_function of rl made slower
        rp.source=rl
        print(rl.SW.when_pressed)            # builtin when SW pin is in RotaryEncoder definition 
        print(rl.when_rotated)
        print(rl.when_rotated_clockwise)
        #print(rb.when_pressed)
        print(rl.when_rotated_counter_clockwise)
        print(rp.source)
        rl.wait_for_rotate()
        print('A: ')
        rl.wait_for_rotate_clockwise()
        print('B: ')
        rl.wait_for_rotate_counter_clockwise()
        print('C: ')
        
        pause()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")