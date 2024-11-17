#!/usr/bin/env python3
from multiprocessing import Lock
from remoteio import RemoteDigitalDevice,RemoteSupervisor
from remoteio import RemoteServer
from remoteio import getFunctionName,shortestWay,map_bg,getName
from remoteio import getFunctions,getReadOnlyProperties,getWriteableProperties
from gpiozero import *
from signal import pause
from time import sleep
import logging
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")
logger.setLevel(logging.INFO)

class Remote_LED(RemoteDigitalDevice):
    '''
    class Remote_LED(
    pin: Any | None = None,
    *,
    active_high: bool = True,
    initial_value: bool = False,
    pin_factory: Any | None = None
)'''

    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"LED has 1 positional parameter")
        super().__init__(remote_server, 'LED',**kwargs)

        self.functions=    ['blink', 'close', 'ensure_pin_factory', 'off', 'on', 'toggle']         
        self.readOnlyProperties = ['closed', 'is_active', 'is_lit', 'pin', 'values']
        self.writeableProperties=['active_high', 'pin_factory', 'source', 'source_delay', 'value']
        
      
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
    @property
    def pin(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################
    @property
    def active_high(self):
        return self.getProperty(getFunctionName())    
    @active_high.setter
    def active_high(self,wert):
        self.func_exec('set',active_high=wert)
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

    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
    #l=LED(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#
#    rl=Remote_LED(rs,pin=21)
#    rl.on(on_time=5.0)
#    sleep(5.0)       # simulate timing for server on client, when you work furtheron with the led                
#    rl1=Remote_LED(rs,20)
#    
#    rl2=Remote_LED(rs,16) 
#    print(rl.is_active)
#    rl1.source=rl
#    rl2.source=rl1
#    rl.blink()
#    sleep(5)
#    print(rl.active_high)
#    rl.on()
#    print(rl.is_active)
#    sleep(5)
#    rl.off()
#    sleep(5)
#    rl.toggle()
#    pause()
##################################################################
##################################################################
class Remote_PWMLED(RemoteDigitalDevice):
    '''
    class PWMLED(
        pin: Any | None = None,
        *,
        active_high: bool = True,
        initial_value: int = 0,
        frequency: int = 100,
        pin_factory: Any | None = None
    )
    '''

    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"PWMLED has 1 positional parameter")
        super().__init__(remote_server, 'PWMLED', **kwargs)
        

        self.functions=  ['blink', 'close', 'ensure_pin_factory', 'off', 'on', 'pulse', 'toggle']
        self.readOnlyProperties= ['closed', 'is_active', 'is_lit', 'pin', 'values']
        self.writeableProperties= ['active_high', 'frequency', 'pin_factory', 'source', 'source_delay', 'value']

        
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
    @property
    def pin(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################
    @property
    def active_high(self):
        return self.getProperty(getFunctionName())    
    @active_high.setter
    def active_high(self,wert):
        self.func_exec('set',active_high=wert)
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
    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=PWMLED(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
       #   
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_PWMLED(rs,21)
#    rl1=Remote_PWMLED(rs,pin=20)
#    rl._source_delay=0.01
#    rl1.source=rl
#    #rl.blink()
#    #sleep(5)
#    rl.pulse(fade_in_time=2.5,fade_out_time=2.5,n=1)   # pulse one time in 5 seconds
#    sleep(5)                                           # wait until pulsing has finished
#    rl.on()
#    sleep(5)
#    rl.off()
#    sleep(5)
#    rl.toggle()
#    pause()
##################################################################
##################################################################
class Remote_RGBLED(RemoteDigitalDevice):

    '''
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
    '''

    def __init__(self, remote_server,*args,**kwargs):
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
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=RGBLED(16,20,21)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
       
    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    #rl=Remote_RGBLED(rs,green=20,blue=16,red=21,pwm=True)  
#    rl=Remote_RGBLED(rs,21,20,16,pwm=True)    #red,green,blue
#    rl.blink()
#    sleep(5)
#    rl.pulse()
#    sleep(5)
#    rl.on(on_time=5.0)
#    #pause()
#    sleep(5)
#    rl.off()
#    sleep(5)
#    rl.toggle()
#    sleep(0.5)
#    rl.value=(1.0,0,0)  # red, green,blue
#    pause()
##################################################################
##################################################################
class Remote_Buzzer(RemoteDigitalDevice):

    '''
    class Buzzer(
    pin: Any | None = None,
    *,
    active_high: bool = True,
    initial_value: bool = False,
    pin_factory: Any | None = None
    )
    '''

    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"Buzzer has 1 positional parameter")

        super().__init__(remote_server, 'Buzzer', **kwargs)
        

        self.functions=  ['beep', 'blink', 'close', 'ensure_pin_factory', 'off', 'on', 'toggle']
        self.readOnlyProperties= ['closed', 'is_active', 'pin', 'values']
        self.writeableProperties=['active_high', 'pin_factory', 'source', 'source_delay', 'value']

        
    def beep(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def blink(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def off(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def on(self,**kwargs):
        if 'on_time' in kwargs.keys():
            self.beep(on_time=kwargs['on_time'],off_time=0,n=1)
        else:
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
    def pin(self):
        return self.getProperty(getFunctionName())
    ##the generator values situated on the remote server is not 
    # of interest

    ##########################################################
    ##########################################################
    #### properties with getter and setter
    ##########################################################
    ##########################################################

    @property
    def active_high(self):
        return self.getProperty(getFunctionName())    
    @active_high.setter
    def active_high(self,wert):
        self.func_exec('set',active_high=wert) 
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
    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=Buzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    #   
    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_Buzzer(rs,map_bg(40,'b'))
#     
#    rl.beep()
#    sleep(8)
#    rl.blink()
#    sleep(5)
#    rl.on(on_time=5)
#    sleep(5)
#    rl.off()
#    sleep(5)
#    rl.toggle()
#    pause()
#################################################################
##################################################################
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

    def __init__(self, remote_server,*args,**kwargs):
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
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=TonalBuzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

   
#    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_TonalBuzzer(rs,pin=map_bg(40,'b'))
#    rl=Remote_TonalBuzzer(rs,map_bg(40,'b'))
#    print(rl.all)
#    rl.play(tone="Tone('A4')")
#    sleep(4)
#    rl.stop()
#    sleep(10)
#    rl.tone=220.0
#    print(rl.tone)
#    sleep(4)
#    rl.stop()
#    sleep(4)
#    print(rl.tone)
#    sleep(5)
#    pause()   
##################################################################
##################################################################
class Remote_Motor(RemoteDigitalDevice):

    '''
    class Motor(
    forward: int,
    backward: int,
    *,
    enable: Any | None = None,
    pwm: bool = True,
    pin_factory: Any | None = None
)

    '''

    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==2:
                kwargs['args']=args
            else:
                raise ValueError(f"Motor has 2 positional parameter")

        super().__init__(remote_server, 'Motor', **kwargs)
        

        self.functions=  ['backward', 'close', 'ensure_pin_factory', 'forward', 'reverse', 'stop']
        self.readOnlyProperties= ['all', 'closed', 'is_active', 'namedtuple', 'values']
        self.writeableProperties=['pin_factory', 'source', 'source_delay', 'value']

        
    def backward(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def forward(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def reverse(self,**kwargs):
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
    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=Motor(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_Motor(rs,16,20)
#    print(rl.all)
#    rl.forward()
#    sleep(4)
#    rl.stop()
#    print(rl.is_active)
#    rl.reverse()
#    sleep(4)
#    rl.backward()
#    print(rl.is_active)
#    sleep(4)
#    rl.stop()
#    sleep(5)
#    pause() 
##################################################################
##################################################################
class Remote_PhaseEnableMotor(RemoteDigitalDevice):

    '''
   class PhaseEnableMotor(
    phase: int,
    enable: int,
    *,
    pwm: bool = True,
    pin_factory: Any | None = None
)
    '''

    def __init__(self, remote_server, *args,**kwargs):
        if args!=():
            if len(args)==2:
                kwargs['args']=args
            else:
                raise ValueError(f"PhaseEnableMotor has 2 positional parameter")
        super().__init__(remote_server, 'PhaseEnableMotor', **kwargs)
        

        self.functions=  ['backward', 'close', 'ensure_pin_factory', 'forward', 'reverse', 'stop']
        self.readOnlyProperties= ['all', 'closed', 'is_active', 'namedtuple', 'values']
        self.writeableProperties=['pin_factory', 'source', 'source_delay', 'value']
        
    def backward(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def ensure_pin_factory(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs) 
    def forward(self,**kwargs):
        self.func_exec(getFunctionName(),**kwargs)
    def reverse(self,**kwargs):
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
    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=PhaseEnableMotor(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_PhaseEnableMotor(rs,16,20)
#    print(rl.all)
#    rl.forward()
#    sleep(4)
#    rl.stop()
#    print(rl.forward)
#    print(rl.backward)
#    rl.reverse()
#    rl.value=-0.5
#    sleep(4)
#    rl.backward()
#    print(rl.is_active)
#    sleep(4)
#    rl.stop()
#    sleep(5)
#    pause()
##################################################################
##################################################################
class Remote_Servo(RemoteDigitalDevice):

    '''
   class Servo(
    pin: Any | None = None,
    *,
    initial_value: float = 0,
    min_pulse_width: float = 1 / 1000,
    max_pulse_width: float = 2 / 1000,
    frame_width: float = 20 / 1000,
    pin_factory: Any | None = None
)
    '''

    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"Servo has 1 positional parameter")
        super().__init__(remote_server, 'Servo', **kwargs)
        

        self.functions=  ['close', 'detach', 'ensure_pin_factory', 'max', 'mid', 'min']
        self.readOnlyProperties= ['all', 'closed', 'frame_width', 'is_active', 'max_pulse_width', 'min_pulse_width', 'namedtuple', 'values']
        self.writeableProperties=['pin_factory', 'pulse_width', 'source', 'source_delay', 'value']

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
    def max_pulse_width(self):
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
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
   
    #l=Servo(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

   
    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_Servo(rs,21)
#    print(rl.all)
#    rl.max()
#    sleep(4)
#    rl.mid()
#    print(rl.pulse_width)
#    print(rl.max_pulse_width)
#   
#    sleep(4)
#    rl.min()
#    print(rl.is_active)
##################################################################
##################################################################
class Remote_AngularServo(RemoteDigitalDevice):
    '''
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

    '''

    def __init__(self, remote_server,*args,**kwargs):
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
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=AngularServo(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
#    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_AngularServo(rs,21)
#    print(rl.all)
#    rl.max()
#    sleep(4)
#    rl.mid()
#    print(rl.pulse_width)
#    print(rl.max_pulse_width)
#   
#    sleep(4)
#    rl.min()
#    print(rl.is_active)
#    sleep(4)
#    rl.angle=rl.max_angle
#    sleep(5)
#    pause() 
##################################################################
##################################################################
class Remote_Button(RemoteDigitalDevice):
    
    '''
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
    '''

    def __init__(self, remote_server,*args,**kwargs):
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
        while not thread_dict[text][0]==None:
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
            
             
                               
#if __name__=='__main__':
#    import logging
#    logging.basicConfig(level=logging.INFO,
#                        style="{",
#                        format="{asctime} [{levelname:8}][{funcName}: {linenoS}]{message}"
#                        )
#     
#    logger = logging.getLogger(name="remoteio1")
#
#    def wpfunc(x):
#            logger.info(f"wp {x}")
#    def wrfunc(x):
#        logger.info(f"wr {x}")
#    def whfunc(x):
#        logger.info(f"wh {x}")
#
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=Button(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_Button(rs,5,hold_repeat=False,pull_up=True)
#    rl.hold_time=1.0
#    logger.info(rl.hold_time)
#    rl.hold_repeat=True
#    logger.info(rl.hold_repeat)
#    #pause()
#    sleep(1.0)
#    x=rl.hold_repeat
#    logger.info(x)
#    rl.when_pressed=wpfunc
#    rl.when_released=wrfunc
#    rl.when_held=whfunc
#    rl.wait_for_press()
#    print('A')
#    rl.wait_for_release()
#    print('B')
#    
#    pause()
############################################################################
############################################################################
class Remote_MCP3208(RemoteDigitalDevice):
    '''
    class MCP3208(
    channel: int = 0,
    differential: bool = False,
    max_voltage: float = 3.3,
    **spi_args: Any
    )
    '''
    
    ##################################################################################
    ## we expect remote_server, select_pin as first arguments,because they identify the SPI-device
    ## look the examples. If you want remote_server,channel as first arguments, you can do this, but
    # you need a rearrangment of the arguments between __init__ and super().__init__ because super()
    # expects remote_server,pins as first positional arguments. Examples of rearrangement can be found
    # in the super class, where the numbering parameter ('b' or 'g') is considered
    #################################################################################
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
                                  
#if __name__=='__main__':
#    #l=MCP3208(0,0)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l))
#    #print(getWriteableProperties(l))
#
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_MCP3208(rs,0)   # GPIO Pin 8 is the select pin
#    rp=Remote_PWMLED(rs,21)
#    rp.source=rl
#    while True:
#        sleep(0.1)
#        print(rl.value)
#    pause()
###########################################################
###########################################################
class Remote_LineSensor(RemoteDigitalDevice):
    '''
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
    '''
    
    def __init__(self, remote_server,*args,**kwargs):
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
                                
                                  
#if __name__=='__main__':
    #l=LineSensor(5)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#
#    def wlfunc(x):
#        print(f"wl {x}")
#    def wnlfunc(x):
#        print(f"wnl {x}")
#
#    rl=Remote_LineSensor(rs,5,pull_up=True)   
#    rp=Remote_PWMLED(rs,21)
#    rl.threshold=0.6
#    print(rl.threshold)
#    rp.source=rl
#    rl.wait_for_no_line()
#    print('A')
#    rl.wait_for_line()
#    print('B')
#    rl.when_line=wlfunc
#    rl.when_no_line=wnlfunc
#    
#    pause()
###########################################################
###########################################################
class Remote_MotionSensor(RemoteDigitalDevice):
    '''
   class MotionSensor(
    pin: Any | None = None,
    *,
    pull_up: bool = False,
    active_state: Any | None = None,
    queue_len: int = 1,
    sample_rate: int = 10,
    threshold: float = 0.5,
    partial: bool = False,
    pin_factory: Any | None = None
)
    '''
    
    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"MotionSensor has 1 positional parameter")
        super().__init__(remote_server, 'MotionSensor', **kwargs)

        self.functions= ['close', 'ensure_pin_factory', 'wait_for_active', 'wait_for_inactive', 'wait_for_motion', 'wait_for_no_motion']
        self.readOnlyProperties =['active_time', 'closed', 'inactive_time', 'is_active', 'motion_detected', 
                                  'partial', 'pin', 'pull_up', 'queue_len', 'value', 'values']
        self.writeableProperties=['pin_factory', 'threshold', 'when_activated', 'when_deactivated', 'when_motion', 'when_no_motion']
      
        self.whenDict={# when_function, when_thread, _when_thread_function,when_gen}
            'when_activated':   [None,None,self._when_thread_function,self.gen_when],
            'when_deactivated': [None,None,self._when_thread_function,self.gen_when],
            'when_motion':        [None,None,self._when_thread_function,self.gen_when],
            'when_no_motion':     [None,None,self._when_thread_function,self.gen_when]}
        
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
    def wait_for_motion(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
    def wait_for_no_motion(self,**my_kwargs):
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
                    case 'wait_for_motion':            
                        yield self.is_active
                    case 'wait_for_no_motion':            
                        yield  not self.is_active
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
    def inactive_time(self):
        return self.getProperty(getFunctionName())
    @property
    def is_active(self):
        return self.getProperty(getFunctionName())
    @property
    def motion_detected(self):
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
    def when_motion(self):
        return self.whenDict[getFunctionName()][0]
    @when_motion.setter
    def when_motion(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    @property
    def when_no_motion(self):
        return self.whenDict[getFunctionName()][0]
    @when_no_motion.setter
    def when_no_motion(self, wert):
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
                if text=='when_motion':
                    yield self.is_active==True
                if text=='when_no_motion':
                    yield self.is_active==False
            except Exception:
                break 
                                
                                  
#if __name__=='__main__':
    #l=MotionSensor(5)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))


#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#
#    def wmfunc(x):
#        print(f"wm {x}")
#    def wnmfunc(x):
#        print(f"wnm {x}")
#
#    rl=Remote_MotionSensor(rs,5,pull_up=True)   
#    rp=Remote_PWMLED(rs,21)
#    print(rl.is_active)
#    rp.source=rl
#    rl.wait_for_no_motion()
#    print('A')
#    rl.wait_for_motion()
#    print('B')
#    rl.when_motion=wmfunc
#    rl.when_no_motion=wnmfunc
#    
#    pause()
###########################################################
###########################################################
class Remote_LightSensor(RemoteDigitalDevice):

    '''
    class LightSensor(
    pin: Any | None = None,
    *,
    queue_len: int = 5,
    charge_time_limit: float = 0.01,
    threshold: float = 0.1,
    partial: bool = False,
    pin_factory: Any | None = None
)
    '''
    
    def __init__(self, remote_server,*args,**kwargs):
        if args!=():
            if len(args)==1:
                kwargs['args']=args
            else:
                raise ValueError(f"LightSensor has 1 positional parameter")
        super().__init__(remote_server, 'LightSensor', **kwargs)

        self.functions= ['close', 'ensure_pin_factory', 'wait_for_active', 'wait_for_dark', 'wait_for_inactive', 'wait_for_light']   
        self.readOnlyProperties = ['active_time', 'charge_time_limit', 'closed', 'inactive_time', 'is_active', 'light_detected',
                            'partial', 'pin', 'pull_up', 'queue_len', 'value', 'values']
        self.writeableProperties= ['pin_factory', 'threshold', 'when_activated', 'when_dark', 'when_deactivated', 'when_light']
      
        self.whenDict={# when_function, when_thread, _when_thread_function,when_gen}
            'when_activated':   [None,None,self._when_thread_function,self.gen_when],
            'when_deactivated': [None,None,self._when_thread_function,self.gen_when],
            'when_light':        [None,None,self._when_thread_function,self.gen_when],
            'when_dark':     [None,None,self._when_thread_function,self.gen_when]}
        
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
    def wait_for_dark(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)
    def wait_for_inactive(self,**my_kwargs):
        return self._wait_task(getFunctionName(),self.gen_wait,**my_kwargs)           
    def wait_for_light(self,**my_kwargs):
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
                    case 'wait_for_light':            
                        yield self.is_active
                    case 'wait_for_dark':            
                        yield  not self.is_active
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
    def charge_time_limit(self):
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
    def light_detected(self):
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
    def when_dark(self):
        return self.whenDict[getFunctionName()][0]
    @when_dark.setter
    def when_dark(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    ###########################################################
    @property
    def when_deactivated(self):
        return self.whenDict[getFunctionName()][0]
    @when_deactivated.setter
    def when_deactivated(self, wert):
        self._when_task(getFunctionName(),wert,self.whenDict)
    #############################################################
    @property
    def when_light(self):
        return self.whenDict[getFunctionName()][0]
    @when_light.setter
    def when_light(self, wert):
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
                if text=='when_light':
                    yield self.is_active==True
                if text=='when_dark':
                    yield self.is_active==False
            except Exception:
                break 
                                
                                  
#if __name__=='__main__':
#
#    ####################################
#    #l=LightSensor(5)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l))
#    #print(getWriteableProperties(l))
#    #####################################

#   server_ip = "192.168.178.136"
#    server_port = 8509
    
   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#
#    def wmfunc(x):
#        print(f"wm {x}")
#    def wnmfunc(x):
#        print(f"wnm {x}")
#
#    rl=Remote_LightSensor(rs,5)   
#    rp=Remote_PWMLED(rs,21)
#    print(rl.is_active)
#    rp.source=rl
#    rl.wait_for_dark()
#    print('A')
#    rl.when_dark=wnmfunc
#    rl.wait_for_light()
#    print('B')
#    rl.when_light=wmfunc
#    rl.when_dark=wnmfunc
#    
#    pause()
########################################
###########################################################
class Remote_DistanceSensor(RemoteDigitalDevice):
    '''
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

    '''
    
    def __init__(self, remote_server,*args,**kwargs):
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
                                
                                  
#if __name__=='__main__':

    ####################################
    # 
    #l=DistanceSensor(22,26)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    #####################################

#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#
#    def wmfunc(x):
#        print(f"wm {x}")
#    def wnmfunc(x):
#        print(f"wnm {x}")#
#
#    rl=Remote_DistanceSensor(rs,26,22)   
#    rp=Remote_PWMLED(rs,21)
#    print(rl.is_active)
#    rp.source=rl
#    rl.wait_for_in_range()
#
#    print('A: '+ str(rl.is_active))
#    rl.wait_for_out_of_range()
#    print('B: '+str(rl.is_active))
#    rl.when_in_range=wmfunc
#    rl.when_out_of_range=wnmfunc
#    
#    pause()
###################
###########################################################
class Remote_RotaryEncoder(RemoteDigitalDevice):
    '''
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
    '''
    from multiprocessing import Lock
    import logging
    
    def __init__(self, remote_server,*args,**kwargs):
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
                                
                                  
#if __name__=='__main__':
#    from remoteio import RemoteServer
#    ####################################
#    # 
#    #l=RotaryEncoder(26,22)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l))
#    #print(getWriteableProperties(l))
#    #####################################
#
#    def wrfunc(x):
#        #print(f"wr {rl.steps}")
#        pass
#    def wrcfunc(x):
#        print(f"wrc steps: {rl.steps}")
#        print(f"wrc counter: {rl.counter}")
#    def wrccfunc(x):
#        print(f"wrcc steps: {rl.steps}")
#        print(f"wrcc counter: {rl.counter}")
#        pass
#    
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    pin=map_bg(29,'b')  # GpioPin 5
#    rl=Remote_RotaryEncoder(rs,a=19,b=26, wrap=True)           # CLK, DT
#    rl.activateSW(pin,pull_up=True)                            # push button of the rotary encoder, default pull_up=True
#    #or
#    #rl.SW=Remote_Button(rs,pin,pull_up=True)                  # SW pullup=True expected by the rotary encoder used here
#
#    rl.SW.when_pressed = rl.reset_counter           # method not function, because dependent from object
#                                                    # well interpreted by gpiozero
#    print(rl.SW.clientIdent())                 
#    rp=Remote_PWMLED(rs,21)
#    print(rl.is_active)
#    rl.when_rotated=wrfunc               # function
#    rl.when_rotated_clockwise=wrcfunc    # function
#    rl.when_rotated_counter_clockwise=wrccfunc # method
#    rl._source_delay=0.02                 # generator_function of rl made slower
#    rp.source=rl
#    print(rl.SW.when_pressed)            # builtin when SW pin is in RotaryEncoder definition 
#    print(rl.when_rotated)
#    print(rl.when_rotated_clockwise)
#    #print(rb.when_pressed)
#    print(rl.when_rotated_counter_clockwise)
#    print(rp.source)
#    rl.wait_for_rotate()
#    print('A: ')
#    rl.wait_for_rotate_clockwise()
#    print('B: ')
#    rl.wait_for_rotate_counter_clockwise()
#    print('C: ')
#    
#    pause()
###############################################################################
###############################################################################
class Remote_LEDBoard(RemoteDigitalDevice):
    '''
    class LEDBoard(
    ...,
    pwm: bool = False,
    active_high: bool = True,
    initial_value: bool = False,
    _order: Any | None = None,
    pin_factory: Any | None = None
    )
    '''

    def __init__(self, remote_server,*args,**kwargs):
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
                                  
#if __name__=='__main__':
#    server_ip = "192.168.178.136"
#    server_port = 8509
    
    #l=LEDBoard(20,21)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
    

    # _order in combination with named leds defines how the property value has to be interpreted.
    # here value=(led1.value,led2.value,led3.value)
    #rl=Remote_LEDBoard(rs,led2=16,led1=20,led3=21,pwm=True,_order=('led1','led2','led3'))
    #rl.value=(1,0,1) # pin20,pin16,pin21
    #logger.info(RemoteDigitalDevice.value.fget(rl))
    #pause()

#    rl=Remote_LEDBoard(rs,16,20,21,pwm=True)
#    rl.value=(1,0,1) # pin 16,20,21
#    logger.info(RemoteDigitalDevice.value.fget(rl))  # anonymeous alphabetic order
#
#    print(rl.is_active)
#    rl.blink()
#    sleep(10)
#    rl.off()
#    print(rl.active_high)
#    rl.on(1,-1)
#    print(rl.is_active)
#    sleep(10)
#    rl.off(-1)
#    sleep(10)
#    rl.toggle(0,1)
#    pause()
####################################################################
####################################################################
class Remote_LEDBarGraph(RemoteDigitalDevice):
    '''
    class LEDBarGraph(
    *pins: Any,
    pwm: bool = False,
    active_high: bool = True,
    initial_value: float = 0,
    pin_factory: Any | None = None
    )   
    '''

    def __init__(self, remote_server,*args,**kwargs):
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
                                 
                                  
#if __name__=='__main__':
    #l=LEDBarGraph(16,20,21)
    #print(getFunctions(l)) 
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(LEDBarGraph(l))
 
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl = Remote_LEDBarGraph(rs,16,20,21)
#    remote_mcp=Remote_MCP3208(rs,0,0)
#    print(remote_mcp.value)
#    pause()
#    rl.source=remote_mcp   # ok
#   
#    rl.value=1/2
#    sleep(5)
#    rl.value=-1/2
#    sleep(5)
#    rl.value=-2/2
#    sleep(5)
#    rl.value=1
#    sleep(5)
#    rl.off()
#    #pause()
############################################################################
class Remote_Compositum():
    def __init__(self,*args):
        self._childs=[]
        self._value={}
        self._gpiozero_elements=[]
        self.addComponent(*args)
        self.ident=RemoteSupervisor.genServerIdent()
        self.setClientIdent(self.ident)

    def getClientIdent(self):
        return RemoteSupervisor._ident_dict[self.ident]
    def setClientIdent(self,ident):
        RemoteSupervisor.setClientIdent(self.ident,ident)

    def addComponent(self,*compTuple):
        for comp in compTuple:
            if  hasattr(comp,'on')      and \
                hasattr(comp,'off')     and \
                hasattr(comp,'toggle')  and \
                hasattr(comp,'blink')   and \
                hasattr(comp,'value')   and \
                not comp in self._childs:
                if isinstance(comp,Remote_Compositum):
                    for x in comp._gpiozero_elements:
                        if x in self._gpiozero_elements:
                           raise ValueError(f"{comp.getClientIdent()}: {x.getClientIdent()} is already related to " + 
                                             "{self.getClientIdent()}")
                    self._gpiozero_elements     +=comp._gpiozero_elements     
                else:
                    if not comp in self._gpiozero_elements:
                        self._gpiozero_elements.append(comp)
                    else:
                        raise ValueError(f"{comp.getClientIdent()} is already related to {self.getClientIdent()}")
                self._childs.append(comp)
            else:
                raise ValueError(f"{comp.getClientIdent()} is not a valid Component")
                        
    def popComponent(self,comp):
        if comp in self._childs:
            self.pop(comp)
        
    def getChild(self,index):
        if 0 <= index < len(self._childs):
            return self._childs[index]
        else:
            return None


    def on(self,*args):
        if args==():
            for child in self._childs:
                child.on()
        else:
            for index in args:
                self._childs[index].on()

    def off(self,*args):
        if args==():
            for child in self._childs:
                child.off()
        else:
            for index in args:
                self._childs[index].off()

    
    def toggle(self,*args):
        if args==():
            for child in self._childs:
                child.toggle()
        else:
            for index in args:
                self._childs[index].toggle()

    def blink(self,**args):
        for child in self._childs:
            child.blink(**args)

    def pulse(self,**args):
        for child in self._childs:
            if hasattr(child,'pulse'):
                child.pulse(**args)


    @property
    def value(self):
        self._value={}
        for child in self._childs:
            self._value[child.getClientIdent()] = child.value
        return self._value
    @value.setter
    def value(self,wert):
         for child in self._childs:
            child.value=wert[child.getClientIdent()]

if __name__=='__main__':
    rs=RemoteServer('192.168.178.136',8509)
    
    rl1=Remote_RGBLED(rs,16,18,20,pwm=True)
    rl2=Remote_PWMLED(rs,22)
    rl3=Remote_PWMLED(rs,21)
    rl1.close()
    rc=Remote_Compositum(rl1,rl2)
    rc1=Remote_Compositum(rc,rl3)
    rl1.setClientIdent('rs.rl1')
    rl2.setClientIdent('rs.rl2')
    rl3.setClientIdent('rs.rl3') 
    rc.setClientIdent('__.rc')
    rc1.setClientIdent('__.rc1') 
    print(rl1.getClientIdent())
    print(rl2.getClientIdent())  
    print(rl3.getClientIdent())
    print(rc.getClientIdent())
    print(rc1.getClientIdent())
    print(list(RemoteSupervisor._ident_dict.keys()))
    #print(rc1._childs)
    #print(rc1._gpiozero_elements)
    #print(rc1._gpiozero_elements_dict)
    rl1.on()
    rl2.on()
    rl3.on()
    print(rl1.value)
    print(rl2.value)
    print(rl3.value)
    rc1.off()
    rc1.on(-1)
   
    print(rc1.value)
    sleep(5)
    rc1.off(-2,-1)
    print(rc1.value)
    sleep(5)
    rl1.open()
    rc1.toggle(0,1)
    print(rc1.value)
    sleep(5)
   
    rc1.value={rc.getClientIdent(): {rl1.getClientIdent(): (1,1,0), rl2.getClientIdent(): 1}, rl3.getClientIdent(): 1}
    print(rc1.value)
    sleep(5)
    rc1.pulse()
    pause()

        