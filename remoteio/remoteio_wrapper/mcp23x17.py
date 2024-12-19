#!/usr/bin/env python3
################################################################################
# class MCP23x17 und Mixins
# Chip MCP23017 I2C-Bus
################################################################################

from multiprocessing import current_process
import spidev
from smbus2 import SMBus
from threading import Thread

from remoteio.remoteio_helper import i2cDetect,getBit,setBit,resetBit

from time import sleep
import logging
logger=logging.getLogger(__name__)

IODIRA=0x00
IODIRB=0x01
IPOLA=0x02
IPOLB=0x03
GPINTENA=0x04
GPINTENB=0x05
DEFVALA=0x06
DEFVALB=0x07
INTCONA=0x08
INTCONB=0x09
IOCON=0x0A          # there exists only one IOCON register with 8 bits 
#IOCON=0x0B         # it can be addressed by 0x0A and 0xoB
GPPUA=0x0C
GPPUB=0x0D
INTFA=0x0E
INTFB=0x0F
INTCAPA=0x10
INTCAPB=0x11
GPIOA=0x12
GPIOB=0x13
OLATA=0x14
OLATB=0x15

#############################################################################################
# class Mixin23017
#############################################################################################
class Mixin23017:
    '''
    Parameters:
        busId:int=1
        address:int=0x20
    '''
    def __init__(self,busId:int=1,address:int=0x20):
        self._lock=Lock()
        self.address=address  # I2C address
        self.busId = busId
        self.i2c = SMBus(self.busId)
        while self._i2cDetect() == None:
            sleep(0.005)   
    
    def _i2cDetect(self):       
        try:
            x=i2cDetect()      # remoteio_helper.py
            if not (self.address in x):
                pass 
            return self.address
        except:
            raise IOError("I2C-Bus-Device "+ hex(self.address) + " antwortet nicht!")  

    def close(self):
        self.i2c.close() 

    def getRegister(self,register:int)->int:
        daten=self.i2c.read_byte_data(self.address,register)
        return daten
    def setRegister(self,register,daten):
        with self._lock:
            daten=daten&0xFF
            self.i2c.write_byte_data(self.address,register,daten)
    def getRegisterBit(self,register,bitNr):
        daten=self.i2c.read_byte_data(self.address,register)
        return getBit(bitNr,daten)
    def setRegisterBit(self,register,bitNr,flag): 
        with self._lock:
            oldData=self.getRegister(register)
            daten=None
            match flag:
                case 1:
                    daten= setBit(bitNr,oldData)
                case 0:
                    daten=resetBit(bitNr,oldData)
                case _:
                    return    
            self.i2c.write_byte_data(self.address,register,daten)         


#############################################################################################
# class Mixin23S17
#############################################################################################
class Mixin23S17:
    '''
    Parameters:
        port:int=0
        device:int=0
        address:int=0x00
    '''
    


    #    Bit field flags as documented in the technical data sheet at
    #    http://ww1.microchip.com/downloads/en/DeviceDoc/21952b.pdf
    IOCON_UNUSED = 0x01
    IOCON_INTPOL = 0x02
    IOCON_ODR = 0x04
    IOCON_HAEN = 0x08
    IOCON_DISSLW = 0x10
    IOCON_SEQOP = 0x20
    IOCON_MIRROR = 0x40
    IOCON_BANK_MODE = 0x80

    IOCON_INIT = 0x28  # IOCON_SEQOP and IOCON_HAEN from above


    MCP23S17_CMD_READ  = 0x41
    MCP23S17_CMD_WRITE = 0x40

    def __init__(self, port=0, device=0, address=0x00): 
        self._lock=Lock()
        self.address = address
        self._port = port
        self._device = device
        self._spimode = 0b00
        self._spi = spidev.SpiDev()
        self._spi.open(self._port, self._device)
        self._spi.max_speed_hz=1000000
        self._spi.mode=self._spimode
        self._spi.xfer2([0])  # dummy write, to force CLK to correct level
        self.setRegisterBit(IOCON,3,1)    # enable address pins for use of multiple chips on SPI-Bus
                                                    # with the same CS-pin
        
        
    def setRegister(self, register, daten):
        command = Mixin23S17.MCP23S17_CMD_WRITE | (self.address<< 1)
        with self._lock:
            daten=daten&0xFF
            self._spi.xfer2([command, register, daten])

    def getRegister(self, register):
        command = Mixin23S17.MCP23S17_CMD_READ | (self.address << 1)
        data = self._spi.xfer2([command, register, 0])
        return data[2] & 0xFF

    def setRegisterBit(self,register,bitNr,flag): 
        with self._lock:
            oldData=self.getRegister(register)
            daten=None
            match flag:
                case 1:
                    daten= setBit(bitNr,oldData)
                case 0:
                    daten=resetBit(bitNr,oldData)
                case _:
                    return    
            command = Mixin23S17.MCP23S17_CMD_WRITE | (self.address << 1)
            daten=daten&0xFF
            self._spi.xfer2([command, register, daten])        

    def getRegisterBit(self,register,bitNr):
            daten=self.getRegister(register)
            return getBit(bitNr,daten)
##########################################################################
class MCP23x17:
    '''
    constructor initializes all register to zero

    This is comparable to the abstract part in the abstract factory design
    for being used independently of whether it is an I2C-device or an
    SPI-device

    Parameters:
        None
    '''

    def __init__(self):        
        self.buttonList=[None for i in range(16)]
        self.ledList=[None for i in range(16)]

        ## all pins are output pins by this reset
        self.reset()
        
     
        
    def reset(self):
        for register in (0,1):
            self.setRegister(register,0x00)
        for register in (2,21):
            self.setRegister(register,0x00)
    


    # only effects output pins
    def set_value(self,pinNr,val):
        if self.ledList[pinNr] != None:
            self.ledList[pinNr].value=val

    def on(self,pinNr,**kwargs):
        self.ledList[pinNr].on(**kwargs)
    def off(self,pinNr,**kwargs):
        self.ledList[pinNr].off(**kwargs)
    def toggle(self,pinNr,**kwargs):
        self.ledList[pinNr].toggle(**kwargs)
    def blink(self,pinNr,**kwargs):
        self.ledList[pinNr].blink(**kwargs)    

    ## needed for remote RMCPButton ###
    def create_MCPLED(self,pinNr):
        self.ledList[pinNr]=MCPLED(self,pinNr)
    ## needed for remote RMCPButton ###
    def create_MCPButton(self,pinNr,bounce_time):
        self.buttonList[pinNr]=MCPButton(self,pinNr,bounce_time)

    def set_hold_time(self,pinNr:int,hold_time:int):
        self.buttonList[pinNr]._hold_time = hold_time

    def set_hold_repeat(self,pinNr:int,hold_repeat:bool):
        self.buttonList[pinNr]._hold_repeat = hold_repeat

    ##################################
    @property
    def is_held(self):
        liste=[None for i in range(16)]
        for i in range(16):
            if self.buttonList[i]!=None:
                liste[i]=self.buttonList[i].is_held
        return liste

    @property
    def held_time(self):
        liste=[None for i in range(16)]
        for i in range(16):
            if self.buttonList[i]!=None:
                liste[i]=self.buttonList[i].held_time
        return liste

    @property
    def hold_time(self):
        liste=[None for i in range(16)]
        for i in range(16):
            if self.buttonList[i]!=None:
                liste[i]=self.buttonList[i].hold_time
        return liste
    @property
    def hold_repeat(self):
        liste=[None for i in range(16)]
        for i in range(16):
            if self.buttonList[i]!=None:
                liste[i]=self.buttonList[i].hold_repeat
        return liste
    ###################################    
    @property
    def iodir(self):
        a=self.getRegister(IODIRA)
        b=self.getRegister(IODIRB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @iodir.setter
    def iodir(self,daten):
        self.setRegister(IODIRA,daten & 0xFF)   
        self.setRegister(IODIRB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def ipol(self):
        a=self.getRegister(IPOLA)
        b=self.getRegister(IPOLB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @ipol.setter
    def ipol(self,daten):
        self.setRegister(IPOLA,daten & 0xFF)   
        self.setRegister(IPOLB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def gpinten(self):
        a=self.getRegister(GPINTENA)
        b=self.getRegister(GPINTENB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @gpinten.setter
    def gpinten(self,daten):
        self.setRegister(GPINTENA,daten & 0xFF)   
        self.setRegister(GPINTENB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def defval(self):
        a=self.getRegister(DEFVALA)
        b=self.getRegister(DEFVALB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @defval.setter
    def defval(self,daten):
        self.setRegister(DEFVALA,daten & 0xFF)   
        self.setRegister(DEFVALB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def intcon(self):
        a=self.getRegister(INTCONA)
        b=self.getRegister(INTCONB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @intcon.setter
    def intcon(self,daten):
        self.setRegister(INTCONA,daten & 0xFF)   
        self.setRegister(INTCONB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def iocon(self):
        a=self.getRegister(IOCON)
        return a&0x00FF
    @iocon.setter
    def iocon(self,daten):
        self.setRegister(IOCON,daten & 0xFF)   
    ##################################
    @property
    def gppu(self):
        a=self.getRegister(GPPUA)
        b=self.getRegister(GPPUB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @gppu.setter
    def gppu(self,daten):
        self.setRegister(GPPUA,daten & 0xFF)   
        self.setRegister(GPPUB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def intf(self):
        a=self.getRegister(INTFA)
        b=self.getRegister(INTFB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @intf.setter
    def intf(self,daten):
        self.setRegister(INTFA,daten & 0xFF)   
        self.setRegister(INTFB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def intcap(self):
        a=self.getRegister(INTCAPA)
        b=self.getRegister(INTCAPB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @intcap.setter
    def intcap(self,daten):
        self.setRegister(INTCAPA,daten & 0xFF)   
        self.setRegister(INTCAPB,(daten>>8) & 0xFF) 
    ##################################
    @property
    def gpio(self):
        a=self.getRegister(GPIOA)
        b=self.getRegister(GPIOB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @gpio.setter
    def gpio(self,daten):
        self.setRegister(GPIOA,daten & 0xFF)   
        self.setRegister(GPIOB,(daten>>8) & 0xFF) 

    ##################################
    @property
    def olat(self):
        a=self.getRegister(OLATA)
        b=self.getRegister(OLATB)
        return ((b<<8)&0xFF00)| (a&0x00FF)
    @olat.setter
    def olat(self,daten):
        self.setRegister(OLATA,daten & 0xFF)   
        self.setRegister(OLATB,(daten>>8) & 0xFF) 

####################################################################
    @property
    def value(self):
        daten=self.gpio
        for button in self.buttonList:
            if button!=None:
                x=button.value
                if x == 0:
                    daten=resetBit(button._pinNr,daten)
                if x == 1:
                    daten=setBit(button._pinNr,daten)
        return daten
    @value.setter
    def value(self,daten):
        self.olat=daten    
#####################################################################
#####################################################################
class MCP23017(MCP23x17,Mixin23017):
    '''
    parameter of the constructor are used for Mixin23017
    only the close-function is specific

    Parameters:
        busId:int=1
        address:int=0x20

    '''

    def __init__(self,busId:int=1,address:int=0x20):
        Mixin23017.__init__(self,busId,address)
        MCP23x17.__init__(self)
        
    def close(self):
        for button in self.buttonList:
            if button!=None:
                # soft termination of threads
                button._when_pressed=None
                if button._when_pressed_Thread!=None:
                    button._when_pressed_Thread.join()
                    button._when_pressed_Thread=None
                button._when_held=None
                if button._when_held_Thread!=None:
                    button._when_held_Thread.join()
                    button._when_held_Thread=None
                button._stop_held=True
                if button._is_held_Thread!=None:
                    button._is_held_Thread.join()
                    button._is_held_Thread=None
                button._when_released=None
                if button._when_released_Thread!=None:
                    button._when_released_Thread.join()
                    button._when_released_Thread=None

        for led in self.ledList:
            if led!=None:
                #soft kill of thread
                led._source=None                
                if led._sourceThread!=None:
                    led._sourceEvent.set()
                    led._sourceThread.join()
                    led._sourceEvent.clear()
                    led._sourceThread = None
                ## terminate _blinkProcess by
                led.value=0
        self.buttonList=[]
        self.ledList=[]
        self.reset()
        sleep(0.001)
        self.i2c.close()



        
class MCP23S17(MCP23x17,Mixin23S17):
    '''
    parameter of the constructor are used for Mixin23S17
    only the close-function is specific

    Parameters:
        port=0 
        device=0 
        address=0x00
    '''

    def __init__(self, port=0, device=0, address=0x00): 
        Mixin23S17.__init__(self, port, device, address)
        MCP23x17.__init__(self)
        
    def close(self):
        for button in self.buttonList:
            if button!=None:
                # soft termination of threads
                button._when_pressed=None
                if button._when_pressed_Thread!=None:
                    button._when_pressed_Thread.join()
                    button._when_pressed_Thread=None
                button._when_held=None
                if button._when_held_Thread!=None:
                    button._when_held_Thread.join()
                    button._when_held_Thread=None
                button._stop_held=True
                if button._is_held_Thread!=None:
                    button._is_held_Thread.join()
                    button._is_held_Thread=None
                button._when_released=None
                if button._when_released_Thread!=None:
                    button._when_released_Thread.join()
                    button._when_released_Thread=None

        for led in self.ledList:
            if led!=None:
                #soft kill of thread
                led._source=None                
                if led._sourceThread!=None:
                    led._sourceEvent.set()
                    led._sourceThread.join()
                    led._sourceEvent.clear()
                    led._sourceThread = None
                ## terminate _blinkProcess by
                led.value=0
        self.buttonList=[]
        self.ledList=[]
        self.reset()
        sleep(0.001)
        self._spi.close()

            
###############################################################################
################################################################################
# class MCPLED for remoteio
# Chip MCP23017 I2C-Bus
################################################################################

from smbus import SMBus
from time import sleep
from threading import Thread
from multiprocessing import Lock,Event,Process
from typing import Generator
from inspect import isgeneratorfunction, signature, isfunction,ismethod

class MCPLED:
    '''
    like a gpiozero-LED

    acts only with the interface MCP23x17,
    
    Parameters:
        mcp:MCP23017|MCP23S17
        pinNr:int=None

    '''
    def __init__(self,mcp:MCP23017|MCP23S17, pinNr:int=None):  
        self._mcp=mcp
        self._pinNr=pinNr   # variable
        if self._mcp.buttonList[self._pinNr]!= None or \
            self._mcp.ledList[self._pinNr]!= None:
            raise ValueError(f"Pin {self._pinNr} of MCP23x17 {self._mcp} is busy")
            
        self._mcp.ledList[self._pinNr]=self
        self.gppu=0         # property
        self.iodir=0        # property
        self._source_delay=0.005
        self._source=None
        self._sourceEvent=Event()
        self._blinkEvent=Event()
        self._sourceThread=None
        self._blinkProcess=None
        self._blinkPID=None

####################################################################
## property source
####################################################################
    @property
    def source(self):
       ## time needed for aborting source_function-thread
        #sleep(0.002)
        return self._source
    @source.setter
    def source(self, quelle):
        if self._sourceThread !=None:
            #soft kill of thread
            self._sourceEvent.set()
            self._sourceThread.join()
            self._source=None
            self._sourceThread = None
        if quelle==None:   
            return
        self._sourceThread=Thread(target=self.source_function, args=(quelle,self._sourceEvent),)
        self._sourceThread.start() 
        self._source=quelle
        

    def source_function(self,quelle,ev):
        ## infinite generator expected
        try:
            old_value=None    
            xxx=None           
            if isinstance(quelle,Generator):
                    xxx=quelle
            if isgeneratorfunction(quelle):
                        xxx=quelle()
            if xxx==None:
                xxx=quelle.values
                    
            for wert in xxx:
                if wert!=old_value:
                    self.value=wert
                    old_value=wert
                if ev.is_set():
                    break
                    
        except Exception as e:
            logger.error(str(e))
        finally:
            ev.clear()
            logger.info("source_Thread terminated")

    @property
    def values(self):
        #########################################
        #   infinite generator for button as source
        #########################################
        while True:
            try:
                sleep(self._source_delay)
                yield self.value
            except:
                break
    @property
    def value(self):
        try:
            register=GPIOA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @value.setter
    def value(self,wert):
        try:
            if self.iodir==1:
                return
            if wert not in range(2):
                return
            if current_process()!=self._blinkProcess:
                self._killBlink()
            if self.value==wert:
                return
            register=OLATA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass

    @property
    def gppu(self):
        try:
            register=GPPUA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @gppu.setter
    def gppu(self,wert):
        try:
            if wert not in range(2):
                return
            register=GPPUA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass

    @property
    def iodir(self):
        try:
            register=IODIRA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @iodir.setter
    def iodir(self,wert):
        try:
            if wert not in range(2):
                return
            register=IODIRA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass

    @property
    def ipol(self):
        try:
            register=IPOLA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @ipol.setter
    def ipol(self,wert):
        try:
            if wert not in range(2):
                return
            register=IPOLA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass
    #####################################
    @property
    def is_active(self):
        return self.value==1
    ######################################
####################################################################################

    def off(self):
        self.value=0

    def toggle(self):
        if self.value==0:
            self.value=1
        else:
            self.value=0

    def on(self,on_time=None):
        if on_time==None:
            self.value=1
            return
        if on_time>0:
            self.blink(on_time,off_time=0,n=1)   

    def einBlink(self,on_time,off_time):
        if on_time>0:
                    self.value=1
                    sleep(on_time)
                    self.value=0
        if off_time>0:
            self.value=0
            sleep(off_time)

    def blinkTask(self,on_time=1,off_time=1,n=None):
        if n==None:
            while True:
                self.einBlink(on_time,off_time)
        if n>0:
            while n>0:
                self.einBlink(on_time,off_time)
                n=n-1

    def _killBlink(self):
        import os
        import signal
        if self._blinkPID!=None:
            os.kill(self._blinkPID, signal.SIGTERM) #or signal.SIGKILL 
            self._blinkProcess=None
            self._blinkPID=None

    def blink(self,on_time=1,off_time=1,n=None,background=True):
        self._killBlink()
        if background==False:
            self.blinkTask(on_time,off_time,n)
        else:
            self._blinkProcess=Process(target=self.blinkTask,args=(on_time,off_time,n),)
            self._blinkProcess.start()
            self._blinkPID=self._blinkProcess.pid
            

                


        
################################################################################
# class MCPButton for remoteio
# Chip MCP23017 I2C-Bus
################################################################################
from smbus import SMBus
from time import sleep
from threading import Thread,Timer
from multiprocessing import Lock
from inspect import signature 
class MCPButton:
    '''
    a button with a bounce-time parameter like a gpiozero-button,

    acts only with the interface MCP23x17
    
    Parameters:
        mcp:MCP23017|MCP23S17
        pinNr:int=None
        bounce_time:float=None
    )
    '''
    def __init__(self,mcp:MCP23017|MCP23S17,pinNr:int=None,bounce_time:float=None):  
        self._mcp=mcp
        self._pinNr=pinNr    # variable
        self._bounce_time=bounce_time
        if self._mcp.buttonList[self._pinNr]!= None or \
            self._mcp.ledList[self._pinNr]!= None:
            raise ValueError(f"Pin {self._pinNr} of MCP23x17 {self._mcp} is busy")  

        self._mcp.buttonList[self._pinNr]=self
        self.iodir=1    # property
        self.gppu=1     # property
        self.ipol=1     # property
        self._source_delay=0.01
        self.gen_when_delay=0.01
        self.gen_wait_delay=0.01
        self._hold_time=0
        self._held_time=0
        self._hold_repeat=0
        self._is_held=False
        self._stop_held=False
        self._when_held=None
        self._when_pressed=None
        self._when_released=None
        self._is_held_Thread=None
        self._when_held_Thread=None
        self._when_pressed_Thread=None
        self._when_released_Thread=None
        self._value=self._mcp.getRegisterBit(GPIOA+self._pinNr//8,self._pinNr%8)
        self._valueTimer=None
        self._valueLock=Lock()
        ## start of thread
        self._is_held_Thread=Thread(target=self.is_held_function, args=(),)
        self._is_held_Thread.start()
        
        


    ## generators
    def gen_when(self):
        #########################################
        # infinite generator for when... function
        #########################################
        while True:
            try:
                sleep(self.gen_when_delay)
                yield self.value
            except:
                break

    def gen_wait(self):
        #########################################
        # infinite generator for wait... function
        #########################################
        while True:
            try:
                sleep(self.gen_wait_delay)
                yield self.value
            except:
                break

    @property
    def values(self):
        #########################################
        #   infinite generator for button as source
        #########################################
        while True:
            try:
                sleep(self._source_delay)
                yield self.value
            except:
                break
    
    def _valueDummy(self):
        pass

    @property
    def value(self):
        try:
            with self._valueLock:
                # read new data
                register=GPIOA + self._pinNr//8
                daten=self._mcp.getRegisterBit(register,self._pinNr%8) 
                if self._bounce_time==None:
                    self._value=daten
                    return self._value
                 
                if daten != self._value:
                    if self._valueTimer!=None and self._valueTimer.is_alive():
                        return self._value
                    else:
                        if self._valueTimer==None:
                            self._valueTimer=Timer(self._bounce_time,self._valueDummy,())
                            self._valueTimer.start()
                        else:
                            self._value=daten
                            self._valueTimer=None
                return self._value                 
                
        except:
            return None

    @property
    def gppu(self):
        try:
            register=GPPUA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @gppu.setter
    def gppu(self,wert):
        try:
            if wert not in range(2):
                return
            register=GPPUA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass

    @property
    def iodir(self):
        try:
            register=IODIRA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @iodir.setter
    def iodir(self,wert):
        try:
            if wert not in range(2):
                return
            register=IODIRA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass

    @property
    def ipol(self):
        try:
            register=IPOLA + self._pinNr//8
            daten=self._mcp.getRegisterBit(register,self._pinNr%8)
            return daten
        except:
            return None
    @ipol.setter
    def ipol(self,wert):
        try:
            if wert not in range(2):
                return
            register=IPOLA + self._pinNr//8
            self._mcp.setRegisterBit(register,self._pinNr%8,wert)
        except:
            pass
    #####################################
    @property
    def is_active(self):
        return self.value==1
    @property
    def is_pressed(self):
        return self.value==1
    @property
    def is_released(self):
        return self.value==0

    @property
    def is_held(self):
        return self._is_held
    @property
    def held_time(self):
        return self._held_time
    @property
    def hold_repeat(self):
        return self._hold_repeat
    @hold_repeat.setter
    def hold_repeat(self,wert):
        self._hold_repeat=wert
    @property
    def hold_time(self):
        return self._hold_time
    @hold_time.setter
    def hold_time(self,wert):
        self._hold_time=wert
    #####################################
    @property
    def when_held(self):
        return self._when_held
    @when_held.setter
    def when_held(self,func):        
        #soft kill of threads
        self._when_held=None
        if self._when_held_Thread != None:
            self._when_held_Thread.join()
            self._when_held_Thread = None 
        if func==None:  
            self._when_held=None
            self._when_held_Thread = None 
            return

        self._when_held_Thread=Thread(target=self.when_held_function, args=(func,),)
        self._when_held_Thread.start() 
    #####################################
    @property
    def when_pressed(self):
        return self._when_pressed
    @when_pressed.setter
    def when_pressed(self,func):
        #soft kill of thread
        self._when_pressed=None
        if self._when_pressed_Thread != None:
            self._when_pressed_Thread.join()
            self._when_pressed_Thread = None 
        if func==None:  
            self._when_pressed=None
            self._when_pressed_Thread = None 
            return
        self._when_pressed_Thread=Thread(target=self.when_pressed_function, args=(func,),)
        self._when_pressed_Thread.start() 
        
    #####################################
   #####################################
    @property
    def when_released(self):
        return self._when_released
    @when_released.setter
    def when_released(self,func):
        #soft kill of thread
        self._when_released=None
        if self._when_released_Thread != None:
            self._when_released_Thread.join()
            self._when_released_Thread = None 
        if func==None:  
            self._when_released=None
            self._when_released_Thread = None 
            return
        self._when_released_Thread=Thread(target=self.when_released_function, args=(func,),)
        self._when_released_Thread.start() 
    ######################################

    def wait_for_release(self,timeout=None):
        import time
        start=None
        if timeout!=None and timeout>0:
            start = time.perf_counter()
        while self.value==1:
            if start!=None:
                end=time.perf_counter()
                if end - start > timeout:
                    return
            sleep(self.gen_wait_delay)
            pass
        else:
            return
    def wait_for_press(self,timeout=None):
        import time
        start=None
        if timeout!=None and timeout>0:
            start = time.perf_counter()
        while self.value==0:
            if start!=None:
                end=time.perf_counter()
                if end - start > timeout:
                    return
            sleep(self.gen_wait_delay)
            pass
        else:
            return
#######################################################################

    def when_released_function(self,func):
        try:
            self._when_released=func
            while True:
                if self._when_released!=None:
                    old_value = None
                    for val in self.gen_when():
                        if old_value==None: 
                            old_value=val
                            continue
                        if val!= old_value:
                            old_value=val
                            if val==0:
                                if self._when_released!=None:
                                    wh=0
                                    sig = signature(func)
                                    for name, param in sig.parameters.items():
                                        if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                            wh=+1
                                            break 
                                    if wh == 0:
                                        func()
                                    else:
                                        func(self)
                                else:
                                    break
                        if self._when_released==None:
                            break
                else:
                    break
        except Exception as e:
            logger.error(f"{e.__class__}: {str(e)}")
        finally:
            self._when_released=None
            logger.info("when_released_Thread terminated")


    def when_pressed_function(self,func):
        try:
            self._when_pressed=func
            while True:
                if self._when_pressed!=None:
                    old_value = None
                    for val in self.gen_when():
                        if old_value==None: 
                            old_value=val
                            continue
                        if val!= old_value:
                            old_value=val
                            if val==1:
                                if self._when_pressed!=None:
                                    wh=0
                                    sig = signature(func)
                                    for name, param in sig.parameters.items():
                                        if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                            wh=+1
                                            break 
                                    if wh == 0:
                                        func()
                                    else:
                                        func(self)
                                else:
                                    break
                        if self._when_pressed==None:
                            break
                else:
                    break
        except Exception as e:
            logger.error(f"{e.__class__}: {str(e)}")
        finally:
            self._when_pressed=None
            logger.info("when_pressed_Thread terminated")

    def when_held_function(self,func):
        try:
            self._when_held=func
            while True:
                if self._when_held!=None:
                    while not self._is_held:
                        sleep(0.001)
                        if self._when_held==None:
                            break
                    if self._when_held==None:
                        break
                    func = self._when_held
                    if func !=None:   
                        wh=0
                        sig = signature(func)
                        for name, param in sig.parameters.items():
                            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                wh=+1
                                break
                        while self._hold_repeat:
                            if self._when_held==None:
                                break
                            if wh==0:
                                func()
                            else:
                                func(self)
                            sleep(self.hold_time)
                            
                        else:
                            if self._when_held==None:
                                break
                            if wh==0:
                                func()
                            else:
                                func(self)
                            while self.value!=0:
                                if self._when_held==None:
                                    break
                                sleep(self.gen_wait_delay)

                    sleep(self.gen_when_delay*2)
                else:
                    break
        except Exception as e:
            logger.error(f"{e.__class__}: {str(e)}")
        finally:
            self._when_held=None
            logger.info("when_held_Thread terminated")

    def is_held_function(self):
        import time
        try:
            while True:
                if self._stop_held==False:
                    self._held_time=0
                    self._is_held=False
                    while self._hold_time == 0 or \
                            self.iodir==0 or \
                            self.value==0:
                        sleep(0.005)
                        if self._stop_held==True:
                            break
                    if self._stop_held==True:
                        break
                    # Startet den hochauflösenden Timer
                    start = time.perf_counter()
                    while self.value==1:
                        end=time.perf_counter()
                        self._held_time=end - start
                        if self._held_time>=self._hold_time:
                            self._is_held=True
                        sleep(0.005)
                        if self._stop_held==True:
                            break
                else:
                    break
        except Exception as e:
            logger.error(f"{e.__class__}: {str(e)}")
        finally:
            self._is_held=False
            logger.info("is_held_Thread terminated")

if __name__=='__main__':
    from multiprocessing import active_children 
    import sys
    from signal import pause

    import logging
    # instantiate logger
    logging.basicConfig(level=logging.INFO,style="{",format="{asctime} {name} {lineno}: [{levelname:8}]{message}")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # logger.info('start')
    try:
        from gpiozero import LED
        l=LED(21)
        def xwr(x):
            logger.info(f"{x}: wr")
        def xwp(x):
            logger.info(f"{x}: wp")
        def xwh(x):
            logger.info(f"{x}: wh")
        
        mcp=MCP23S17()
        b=MCPButton(mcp,2,bounce_time=0.2)
        #while True:
        #    print(hex(mcp.value))
        #    print(hex(b.value))
        #    sleep(0.5)
    
        led=MCPLED(mcp,0)
        for register in range(0,22):
            logger.info(f"{hex(register)}: {hex(mcp.getRegister(register))}")
    
        
        led.source=b
       
       
        b.hold_time=0.5
        #b.hold_repeat=True
        b.when_pressed=xwp
        b.when_released=xwr
        b.when_held=xwh
        b.wait_for_press(timeout=1.0)
        print('A')
        sleep(10)
        b.wait_for_release(timeout=1.0)
        print('B')
        #b._stop_held=True
        #mcp.close()
        b.hold_repeat=False
        #led.source=b
        led.blink(0.5,1)
        #b.when_released=None
        sleep(1)
        #led.source=b
        sleep(15)
        mcp.close()
        #sleep(1)
        #print(current_process())
        #print(led._blinkProcess)
        #    led.source=b.values
        #    led.value=1
        #    sleep(3)
        #    led.toggle()
        #    sleep(3)
        #    led.toggle()
        #    sleep(3)
        #    led.blink()
        #    b.hold_repeat=False
        #    
        #
        
        pause()
    
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")
    finally:
        #get all active child processes
        active = active_children()
        logger.info(f'Active Children: {len(active)}')
        #terminate all active children
        for child in active:
            child.terminate()
        # block until all children have closed
        for child in active:
            child.join()
        # report active children
        active = active_children()
        logger.info(f'Active Children: {len(active)}')
        logger.info('MainThread terminated')
        sys.exit()