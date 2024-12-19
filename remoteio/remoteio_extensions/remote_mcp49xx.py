#!/usr/bin/env python3
from remoteio.remoteio_client import RemoteServer
from remoteio.remoteio_client import RemoteDigitalDevice
from remoteio.remoteio_helper import getFunctionName

from time import sleep
import logging
logger = logging.getLogger(__name__)

#####################################################################
# class Remote_MCP4801
#####################################################################
class Remote_MCP4801(RemoteDigitalDevice):
    '''
    class Remote_MCP4801(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4801(      
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self, remote_server:RemoteServer,*args,**kwargs):
        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4801', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)   
    @value.setter
    def value(self,wert):
        assert wert in range(2**8), "value: only 0,...,255 allowed" 
        self.func_exec('set',value=wert) 

    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################
#if __name__ =='__main__':
#    from signal import pause
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rmcp=Remote_MCP4801(rs,device=1,max_speed_hz=250000)  
#    rmcp.gain=1  
#
#    #Connect a led with the output of MCP4801
#    while True:
#        for i in range(0,256):
#            rmcp.value=i
#        for i in range(255,0,-1):
#            rmcp.value=i
#
#    rmcp.value=1
#    print(rmcp.value)
#    rmcp.gain=2
#    rmcp.value=1
#    pause()
#####################################################################
# class Remote_MCP4811
#####################################################################
class Remote_MCP4811(RemoteDigitalDevice):
    '''
    class Remote_MCP4811(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4811(      
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4811', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    @value.setter
    def value(self,wert):
        assert wert in range(2**10), "value: only 0,...,1023 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################

if __name__ =='__main__':
    from signal import pause
    server_ip = "192.168.178.136"
    server_port = 8509
    # Create instance of remote Raspberry Pi
    rs = RemoteServer(server_ip, server_port)
    rmcp=Remote_MCP4811(rs,device=1,max_speed_hz=250000)  
    rmcp.gain=1 ##

    #Connect a led with the output of MCP4811
    #while True:
    #    for i in range(600,1024):
    #        rmcp.value=i
    #    for i in range(1023,599,-1):
    #        rmcp.value=i
    #pause() 
    rmcp.value=1023
    print(rmcp.value)
    sleep(5)
    rmcp.close()
    sleep(5)
    rmcp.open()
    rmcp.gain=1
    rmcp.value=1023
    #rmcp.gain=2
    #rmcp.value=1
    #print(rmcp.value)
    pause()
#####################################################################
# class Remote_MCP4821
#####################################################################
class Remote_MCP4821(RemoteDigitalDevice):
    '''
    class Remote_MCP4821(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4821(      
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4821', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    @value.setter
    def value(self,wert):
        assert wert in range(2**12), "value: only 0,...,4095 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################
    
#if __name__ =='__main__':
#    from signal import pause
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rmcp=Remote_MCP4821(rs,device=1,max_speed_hz=250000)  
#    rmcp.gain=1 
#
#    #Connect a led with the output of MCP4821
#    while True:
#        for i in range(600,4096):
#            rmcp.value=i
#        for i in range(4095,599,-1):
#            rmcp.value=i
#  
#    rmcp.value=1
#    print(rmcp.value)
#    rmcp.gain=2
#    rmcp.value=1
#    print(rmcp.value)
#    
#####################################################################
# class Remote_MCP4802
#####################################################################
class Remote_MCP4802(RemoteDigitalDevice):
    '''
    class Remote_MCP4802(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4802(      
        channel:int
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4802', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    ###############################################        
    @property
    def value(self):
        return self.getProperty(getFunctionName())  
    @value.setter
    def value(self,wert):
        assert wert in range(2**8), "value: only 0,...,255 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################

#if __name__ =='__main__':
#    from signal import pause
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rmcp=Remote_MCP4802(rs,0,device=1,max_speed_hz=250000)  # channel needed
#    rmcp.gain=1 
##
#    #Connect a led with the output of MCP4801
#    while True:
#        for i in range(0,256):
#            rmcp.value=i
#        for i in range(255,0,-1):
#            rmcp.value=i
#    rmcp.value=1
#    print(rmcp.value)

#    rmcp.gain=2
#    rmcp.value=1
#    print(rmcp.value)

#    rmcp=Remote_MCP4802(rs,1)  # channel needed
#    rmcp.gain=1  
#    rmcp.value=1
#    print(rmcp.value)

#    rmcp.gain=2
#    rmcp.value=1
#    print(rmcp.value)

#####################################################################
# class Remote_MCP4812
#####################################################################
class Remote_MCP4812(RemoteDigitalDevice):
    '''
    class Remote_MCP4812(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4812(      
        channel:int
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4812', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    @value.setter
    def value(self,wert):
        assert wert in range(2**10), "value: only 0,...,1023 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################
    
#if __name__ =='__main__':
#    from signal import pause
#    server_ip = "192.168.178.136"
#    server_port = 8509
#   # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rmcp=Remote_MCP4812(rs,1,device=1,max_speed_hz=250000)  # channel needed
#    rmcp.gain=1
#
#    #Connect a led with the output of MCP4812
#    while True:
#        for i in range(600,1024):
#            rmcp.value=i
#        for i in range(1023,599,-1):
#            rmcp.value=i
# 
#    rmcp.value=1023
#    pause()
#    print(rmcp.value)

#    rmcp.gain=2
#    rmcp.value=1
#    print(rmcp.value)

#    rmcp1=Remote_MCP4812(rs,0,device=1,max_speed_hz=250000)  # channel needed
#    rmcp1.gain=1  
#    rmcp1.value=1
#    print(rmcp1.value)

#    rmcp1.gain=2
#    rmcp1.value=1
#    print(rmcp1.value)

#    pause()
#####################################################################
# class Remote_MCP4822
#####################################################################
class Remote_MCP4822(RemoteDigitalDevice):
    '''
    class Remote_MCP4822(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4822(      
        channel:int
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4822', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)   
    @value.setter
    def value(self,wert):
        assert wert in range(2**12), "value: only 0,...,4093 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################
    
#if __name__ =='__main__':
#    from remoteio import Remote_PWMLED
#    from signal import pause
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rmcp=Remote_MCP4822(rs,0,device=1,max_speed_hz=250000)  # channel needed
#    rmcp.gain=1 
#
#    #Connect a led with the output of MCP4822
#    while True:
#        for i in range(600,4096):
#            rmcp.value=i
#        for i in range(4095,599,-1):
#            rmcp.value=i
# 
#    rmcp.value=1
#    print(rmcp.value)

#    rmcp.gain=1
#    rmcp.value=4095
#    print(rmcp.value)

#    rmcp1=Remote_MCP4822(rs,1,bus=0,device=1)  # channel needed
#    rmcp1.gain=1  
#    rmcp1.value=1
#    print(rmcp1.value)

#    rmcp1.gain=1
#    rmcp1.value=4095
#    print(rmcp1.value)

#    sleep(5)
#    rmcp.close()
#    rmcp1.value=2500
#    sleep(5)
#    rmcp.open()
#    rmcp.value=4095
#    rmcp1.close()
#    sleep(5)
#    rmcp1.open()
#    rmcp1.value=4095
#    sleep(5)
#    rmcp.close()
#    rmcp1.close()

#####################################################################
# class Remote_MCP4902
#####################################################################
class Remote_MCP4902(RemoteDigitalDevice):
    '''
    class Remote_MCP4902(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4902(      
        channel:int
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4902', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    @value.setter
    def value(self,wert):
        assert wert in range(2**8), "value: only 0,...,255 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################

##################################################
#   Remote_MCP4912
##################################################
class Remote_MCP4912(RemoteDigitalDevice):
    '''
    class Remote_MCP4912(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4912(      
        channel:int
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4912', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    @value.setter
    def value(self,wert):
        assert wert in range(2**10), "value: only 0,...,1023 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    #################################################
        
##################################################
#   Remote_MCP4922
##################################################
class Remote_MCP4922(RemoteDigitalDevice):
    '''
    class Remote_MCP4922(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class MCP4922(      
        channel:int
        bus:int=0,
        device:int=0   
    )
    initializes the corresponding device on the remote server by args and kwargs
    '''
    def __init__(self,remote_server:RemoteServer,*args,**kwargs):

        if args!=():
            kwargs['args']=args  
        super().__init__(remote_server,'MCP4922', **kwargs)

        self._source_delay=0.01

    ###############################################    
    @property
    def value(self):
        # This is the call to the original get method 
        return RemoteDigitalDevice.value.fget(self)  
    @value.setter
    def value(self,wert):
        assert wert in range(2**8), "value: only 0,...,4095 allowed" 
        self.func_exec('set',value=wert)  
    #################################################
    @property
    def gain(self):
        return self.getProperty(getFunctionName())    
    @gain.setter
    def gain(self,wert):
        assert wert in (1,2), "gain must be 1,2"
        self.func_exec('set',gain=wert)   
    #################################################
    @property
    def resolution(self):
        return self.getProperty(getFunctionName()) 
    ################################################# 


#if __name__ =='__main__':
#    from time import sleep
#    from signal import pause
#    server_ip = "192.168.178.136"
#    server_port = 8509
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rmcp=Remote_MCP4912(rs,0,device=1)  # channel needed
#    rmcp.gain=1 
#
#    #Connect a led with the output of MCP4912
#    #while True:
#    #    for i in range(500,1024):
#    #        rmcp.value=i
#    #    for i in range(1023,500,-1):
#    #        rmcp.value=i
# 
#    rmcp.value=1
#    print(rmcp.value)
#    rmcp.gain=1
#    rmcp.value=1023
#    print(rmcp.value)
#    rmcp1=Remote_MCP4912(rs,1,bus=0,device=1)  # channel needed
#    rmcp1.gain=1  
#    rmcp1.value=1
#
#
#    rmcp1.gain=1
#    rmcp1.value=1023
#    print(rmcp1.value)
# 
#    sleep(5)
#    rmcp.close()
#    rmcp1.value=500
#    sleep(5)
#    rmcp.open()
#    rmcp.value=1023
#    rmcp1.close()
#    sleep(5)
#    rmcp1.open()
#    rmcp1.value=1023
#    sleep(5)
#    rmcp.close()
#    rmcp1.close()
#    pause()