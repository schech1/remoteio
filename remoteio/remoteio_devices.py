#!/usr/bin/env python3
from multiprocessing import Lock
from remoteio import RemoteDigitalDevice,getFunctionName,shortestWay
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
        super().__init__(remote_server, 'LED', *args,**kwargs)

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

#    server_ip = "raspy5"
#    server_port = 8509
    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_LED(rs,21)
#    rl1=Remote_LED(rs,20)
#    print(rl.is_active)
#    rl1.source=rl
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
        super().__init__(remote_server, 'PWMLED', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
    
    #l=PWMLED(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
       #   
    # Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_PWMLED(rs,21)
    #rl1=Remote_PWMLED(rs,20)
    #rl1.source=rl
    #rl.blink()
    #sleep(5)
    #rl.pulse(time_ms=5000)
    #sleep(6)
    #rl.on()
    #sleep(5)
    #rl.off()
    #sleep(5)
    #rl.toggle()
    #pause()
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
        super().__init__(remote_server, 'RGBLED', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
    
    #l=RGBLED(16,20,21)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    #   
    # Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_RGBLED(rs,16,20,21)
    
    #rl.blink()
    #sleep(5)
    #rl.pulse()
    #sleep(6)
    #rl.on()
    #sleep(5)
    #rl.off()
    #sleep(5)
    #rl.toggle()
    #sleep(0.5)
    #rl.value=(1.0,0.5,0.1)
    #pause()
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
        super().__init__(remote_server, 'Buzzer', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
    
    #l=Buzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    #   
    # Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_Buzzer(rs,40,'b')
    # 
    #rl.beep()
    #sleep(15)
    #rl.blink()
    #sleep(5)
    #rl.on()
    #sleep(5)
    #rl.off()
    #sleep(5)
    #rl.toggle()
    #pause()
##################################################################
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
        super().__init__(remote_server, 'TonalBuzzer', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
#    
    #l=TonalBuzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

   
    #Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_TonalBuzzer(rs,40,'b')
    #print(rl.all)
    #rl.play(tone="Tone('A4')")
    #sleep(4)
    #rl.stop()
    #sleep(10)
    #rl.tone=220.0
    #sleep(4)
    #rl.stop()
    #sleep(4)
    #print(rl.tone)
    #sleep(5)
    #pause()   
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
        args1=list(args)
        if len(args1)>=3:
            # pin1,pin2,pin3?,...
            if type(args1[2])==int:
                # enable is given
                en=args1.pop(2)
                args=tuple(args1)
                kwargs['enable']=en

        super().__init__(remote_server, 'Motor', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
    
    #l=Motor(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
    #Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_Motor(rs,16,20)
    #print(rl.all)
    #rl.forward()
    #sleep(4)
    #rl.stop()
    #print(rl.is_active)
    #rl.reverse()
    #sleep(4)
    #rl.backward()
    #print(rl.is_active)
    #sleep(4)
    #rl.stop()
    #sleep(5)
    #pause() 
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

    def __init__(self, remote_server,*args,**kwargs):
        super().__init__(remote_server, 'PhaseEnableMotor', *args,**kwargs)
        

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
#    server_ip = "raspy5"
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
        super().__init__(remote_server, 'Servo', *args,**kwargs)
        

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
#    server_ip = "raspy5"
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
        super().__init__(remote_server, 'AngularServo', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
    
    #l=AngularServo(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
    #Create instance of remote Raspberry Pi
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
        super().__init__(remote_server, 'Button', *args,**kwargs)
        

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
#    server_ip = "raspy5"
#    server_port = 8509
#    
    #l=Button(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
#   
#    #Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_Button(rs,5,hold_repeat=False)
#    rl.hold_time=1.0
#   logger.info(rl.hold_time)
#    rl.hold_repeat=True
#    logger.info(rl.hold_repeat)
#    pause()
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
        super().__init__(remote_server, 'MCP3208', *args,**kwargs)

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
    #l=MCP3208(0,0)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

#    server_ip = "raspy5"
#    server_port = 8509
#    
    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_MCP3208(rs,8,channel=0)   # GPIO Pin 8 is the select pin, rs and pin are positional arguments
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
        super().__init__(remote_server, 'LineSensor', *args,**kwargs)

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

#    server_ip = "raspy5"
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
        super().__init__(remote_server, 'MotionSensor', *args,**kwargs)

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

#
#    server_ip = "raspy5"
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
        super().__init__(remote_server, 'LightSensor', *args,**kwargs)

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
#
#    server_ip = "raspy5"
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
        super().__init__(remote_server, 'DistanceSensor', *args,**kwargs)

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

#    server_ip = "raspy5"
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
        self.rSW=None
        ## args evaluation: looking for SW-Pin ##
        args1=list(args)
        if len(args1)>=3:
            # pin1,pin2,pin3?,...
            if type(args1[2])==int:
                # SW is given
                SW=args1.pop(2)
                self.rSW=Remote_Button(remote_server,SW,pull_up=False)
                args=tuple(args1)

        super().__init__(remote_server, 'RotaryEncoder', *args,**kwargs)

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
        self.rSW.when_pressed=self.reset_counter

        

##########################################################
## special treatment for RotaryEncoder
##########################################################  
    def reset_counter(self,x):
        with self._rotary_lock:
            self.counter=0
        logger.info(f"reset_counter: {x}")


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
    ####################################
    # 
    #l=RotaryEncoder(26,22)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    #####################################

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
#    server_ip = "raspy5"
#    server_port = 8509
#    
#   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    
#    rl=Remote_RotaryEncoder(rs,17,18,27, wrap=True)   # CLK, DT, SW
#
#
#
#   #or
#    #rl=Remote_RotaryEncoder(rs,17,18, wrap=True)   # CLK, DT
#    #rb=Remote_Button(rs,27,pull_up=False)          # SW pullup=False important
#    #rb.when_pressed = rl.reset_counter  # method, because dependent from object
#                                        # well interpreted
#                    
#    rp=Remote_PWMLED(rs,21)
#    print(rl.is_active)
#    rl.when_rotated=wrfunc               # function
#    rl.when_rotated_clockwise=wrcfunc    # function
#    rl.when_rotated_counter_clockwise=wrccfunc # method
#    rl._source_delay=0.02                 # generator_function of rl made slower
#    rp.source=rl
#    print(rl.rSW.when_pressed)            # builtin when SW pin is in RotaryEncoder definition 
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
        super().__init__(remote_server, 'LEDBoard', *args,**kwargs)

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

    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
    #l=LEDBoard(20,21)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
#
#    server_ip = "raspy5"
#    server_port = 8509
#    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_LEDBoard(rs,16,20,21)
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
#    rl.toggle(0,1,2)
#    pause()
####################################################################
###############################################################################
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
        super().__init__(remote_server, 'LEDBarGraph', *args,**kwargs)

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
    @property
    def source_delay(self):
        return self.getProperty(getFunctionName())    
    @source_delay.setter
    def source_delay(self,wert):
        self.func_exec('set',source_delay=wert)  

    ## source, value are treated in superclass                               
                                  
#if __name__=='__main__':
    #l=LEDBarGraph(16,20,21)
    #print(getFunctions(l)) 
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(LEDBarGraph(l))
 
#    server_ip = "raspy5"
#    server_port = 8509
    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_LEDBarGraph(rs,16,20,21)
#    remote_mcp=Remote_MCP3208(rs,8,channel=0) # select_pin = 8
#
#    #rl.source=remote_mcp   # ok
#   
#    rl.value=2/3
#    sleep(5)
#    rl.value=-1/3
#    sleep(5)
#    rl.value=-2/3
#    sleep(5)
#    rl.value=1
#    sleep(5)
#    rl.off()
#    pause()