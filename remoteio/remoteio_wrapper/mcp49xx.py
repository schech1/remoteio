#!/usr/bin/env python3
########################################################
## MCP49xx
########################################################
import spidev

from time import sleep
import logging
logger=logging.getLogger(__name__)

class MCP49xx:
    '''
    superclass of MCP4801, MCP4811, MCP4821, MCP4802, MCP4812, MCP4822, MCP4902, MCP4912, MCP4922   

    Parameters:
        name:str
        channel:None
        bus:int=0
        device:int=0
    '''
    def __init__(self,name:str,*args,**kwargs):
        
        self.channel=None
        self.bus=0
        self.device=0
        self._resolution=int(name[5])
        self.number_of_channels=(int(name[6]))
        self.mcp_type=int(name[4])

        if args!=():
            match len(args):
                case 1:
                    if 'channel' in kwargs.keys():
                        raise ValueError(f" channel as positional and as non positional parameter")
                    self.channel=args[0]
                case 2:
                    if 'channel' in kwargs.keys():
                        raise ValueError(f" channel as positional and as non positional parameter")
                    if 'bus' in kwargs.keys():
                        raise ValueError(f" bus as positional and as non positional parameter")
                    self.channel=args[0]
                    self.bus=args[1]
                case 3:
                    if 'channel' in kwargs.keys():
                        raise ValueError(f" channel as positional and as non positional parameter")
                    if 'bus' in kwargs.keys():
                        raise ValueError(f" bus as positional and as non positional parameter")
                    if 'device' in kwargs.keys():
                        raise ValueError(f" device as positional and as non positional parameter")
                    self.channel=args[0]
                    self.bus=args[1]
                    self.device=args[2]
        if 'channel' in kwargs.keys():
            self.channnel=kwargs.pop('channel')
        if 'bus' in kwargs.keys():
            self.bus=kwargs.pop('bus')
        if 'device' in kwargs.keys():
            self.device=kwargs.pop('device')
   
        self._gain=1
        self._buf=0
        self._value=None
        self._spi=None
        
        assert self._resolution in (0,1,2), "resolution must be 0,1,2"
        assert self.channel in range(self.number_of_channels), f"channel must be less than {self.number_of_channels}"

        match (self.bus,self.device):
            case (0,0):
                pass
            case (0,1):
                pass
            case (1,0):
                pass
            case (1,1):
                pass
            case (1,2):
                pass
            case _:
                raise ValueError("combination bus,device not allowed")
        
        match self._resolution:
            case 0:
                self._scale= 2**8
            case 1:
                self._scale= 2**10
            case 2:
                self._scale= 2**12

        self._spi=spidev.SpiDev(self.bus,self.device) 
        for key,val in kwargs.items():
            setattr(self._spi,key,val) 
        ## define beginning position
        self.value=0
 
   ####################################       
    @property
    def gain(self):
        return self._gain
    @ gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2" 
        self._gain=wert
    ####################################    
    @property
    def buf(self):
        return self._buf
    @ buf.setter
    def buf(self,wert):
        assert wert in (0,1), "buf must be 0,1"
        self._buf=wert

    #####################################
    @property
    ## last value to MCP49xx
    def value(self):
        return self._value
    @value.setter
    def value(self,wert): 
        ## MCP49x2 channels have external Vref that can vary, therefore: 
        if self.mcp_type==9:
            wert=min(wert,self._scale-2)
        match self._gain:
            case 1: # voltage 0 ... 2.048 Volt
                write_word=0x30<<8 | (self.channel * 0x8000)
            case 2: # voltage 0 ... 4.096 Volt
                write_word=0x10<<8 | (self.channel * 0x8000) | self._buf << 14
        
        wert1=None
        match self._resolution:
            # 8-bit-resolution
            case 0:
                wert1=wert<<4
            # 10-bit-resolution
            case 1:
                wert1=wert<<2
            case _:
                wert1=wert
        wert1=wert1&0x0FFF | write_word
        wert1=wert1.to_bytes(2,'big')
        self._spi.writebytes([wert1[0],wert1[1]])  
        self._value= wert
               
    
    @property
    ## resolution
    def resolution(self):
        return self._resolution
    
    def close(self):
        self.value=0
        self._spi.close()


###################################################################
## MCP4801
####################################################################
class MCP4801(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,0,*args,**kwargs)


#if __name__ == '__main__':
#    from signal import pause
#    m=MCP4801(device=1)
#    m.gain=1
#    m.value=1
#    sleep(2)
#    print(m.value)
#    m.gain=1
#    m.value=2
#    print(m.value)
#    pause()
########################################################################
## MCP4811
########################################################################
class MCP4811(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,0,*args,**kwargs)


#if __name__ == '__main__':
#    from signal import pause
#    m=MCP4811(device=1,max_speed_hz=250000)
#    m.gain=1
#    m.value=1
#    print(m.value)
#    #sleep(5)
#    m.value=1023
#    print(m.value)
#    #m.gain=2
#    #m.value=1023
#    #print(m.value)
#    sleep(5)
#    m.close()
#    pause()
###################################################################
## MCP4821
###################################################################
class MCP4821(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,0,*args,**kwargs)


#if __name__ == '__main__':
#    m=MCP4821(device=1)
#    m.gain=1
#    m.value=1
#    print(m.value)
#    m.gain=1
#    m.value=4095
#    print(m.value)
###################################################################
## MCP4802
####################################################################
class MCP4802(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,*args,**kwargs)


#if __name__ == '__main__':
#    m=MCP4802(0,device=1)
#    m.gain=1
#    m.value=1
#    print(m.value)
#    m1=MCP4802(1,device=1)
#    m1.gain=2
#    m1.value=255
#    print(m1.value)
###################################################################
# MCP4812
####################################################################
class MCP4812(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,*args,**kwargs)


#if __name__ == '__main__':
#    from signal import pause
#    m=MCP4812(0,device=1)
#    m.gain=1
#    m.value=1
#    print(m.value)
#    m1=MCP4812(1,device=1)
#    m1.gain=1
#    m1.value=1023
#    print(m1.value)
#    pause()
###################################################################
## MCP4822
####################################################################
class MCP4822(MCP49xx):
   def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,*args,**kwargs)

#if __name__ == '__main__':
#    from signal import pause
#    m=MCP4822(0,device=1)
#    m.gain=1
#    m1=MCP4822(1,device=1)
#    m1.gain=1
#
#    while True:
#        for i in range(4096):
#            m.value=i
#            m1.value=i
#            print(m.value)
#            print(m1.value)
#
#    
#    sleep(5)
#    m.value=0
#    print(m.value)
#    sleep(5)
#    #m1.value=0
#    pause()
#
###################################################################
## MCP4902
####################################################################
class MCP4902(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,*args,**kwargs)


#if __name__ == '__main__':
#    m=MCP4902(0,device=1)
#    m.gain=1
#    m.value=1
#    print(m.value)
#    m1=MCP4902(1,device=1)
#    m1.gain=2
#    m1.value=255
#    print(m1.value)
###################################################################
## MCP4912
####################################################################
class MCP4912(MCP49xx):
    def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,*args,**kwargs)


#if __name__ == '__main__':
#    from signal import pause
#    m=MCP4912(0,device=1)
#    m.gain=1
#    m.value=1
#    print(m.value)
#    m1=MCP4912(1,device=1)
#    m1.gain=1
#    m1.value=1023
#    print(m1.value)
#    pause()
###################################################################
## MCP4922
####################################################################
class MCP4922(MCP49xx):
   def __init__(self,*args,**kwargs):
        name=__class__.__qualname__
        super().__init__(name,*args,**kwargs)


#if __name__ == '__main__':
#    from signal import pause
#    m=MCP4922(0,device=1)
#    m.gain=1
#    m1=MCP4922(1,device=1)
#    m1.gain=1
#    #m1.gain=1
#
#    
#   
#    for i in range(20):
#        m.value=4095
#        print(m.value)
#    #    m1.value=0
#        sleep(0.5)
#        m.value=0
#    #    m1.value=4095
#        sleep(0.5)
#
#    m.value=4095
#    sleep(5)
#    m.close()
#    sleep(5)
#    #m1.close()
#    print(m.value) # no error message
#    m.value=0      # error message because spi not affected
#    sleep(5)
#    #m1.value=0     # error message
#    pause()
#