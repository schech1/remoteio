#!/usr/bin/env python3
import socket
from time import sleep 
import builtins
from gpiozero import Device 
from threading import Thread,Event,Timer
from multiprocessing import Lock
from remoteio import PORT, PIN_MAP_bg,getFunctionName

from typing import Generator
from inspect import isgeneratorfunction, signature, isfunction,ismethod
import logging
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")
logger.setLevel(logging.INFO)


#def LEDBoardValue(**kwargs):
#  return tuple(kwargs.values)

def timeOut(obj_type, command):
    logger.info(f"({obj_type},{command}) timed out")


class RemoteServer:  
    def __init__(self, server_ip, server_port=PORT):                                 
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self._pin_list=[]
        ### synchronizing of access to tcp/Ip-connection by different threads
        self.conn_lock=Lock()

    def close(self): 
        sleep(1.0)   
        self.client_socket.close()

    def map_b_to_g(self,pin_number,numbering):
        if numbering=='b':
            if pin_number in PIN_MAP_bg.keys():
                return PIN_MAP_bg[pin_number], 'g'
            else:
                raise ValueError('((b), ' + str(pin_number) + ') false')    
        if numbering == 'g':
            if pin_number in PIN_MAP_bg.values():
                return pin_number,numbering
            else:
                raise ValueError('((g), ' + str(pin_number) + ') false')

    def pinExists(self,pin_number,numbering):
        pin_number,numbering=self.map_b_to_g(pin_number,numbering)
        ret=False
        for p in self._pin_list:
            if p==pin_number:
                ret=True

        return ret
    
############################################################
############################################################
############################################################
class RemotePinDevice:
    def __init__(self, remote_server, obj_type, pins, numbering,**kwargs):
        self.remote_server=remote_server
        self.client_socket=remote_server.client_socket
        self.command='off'
        self.numbering=numbering
        self.pins=pins
        self.kwargs=kwargs
        self.obj_type=obj_type
        self._value=None
        self._closed=False
        self._source=None
        self._sourceThread=None
        self._sourceEvent=Event()
        self._source_delay=0.005


#############################################################    
#############################################################    
##  general functions
#############################################################
############################################################


    def _create(self):
        self.func_exec('_create',**self.kwargs)
        self._value=self.getProperty('value') 

    def get(self,**my_kwargs):
        for x in my_kwargs.keys():
            if x!='property':
                raise ValueError('only allowed key: property')
        ret=self.func_exec('get',**my_kwargs)
        return ret

    def set(self,**my_kwargs):
        '''
        my_kwargs:
        value=...
        '''
        self.func_exec('set',**my_kwargs)

    def close(self):
        self.command='close'
        if self._closed==True:
            raise ValueError("Device is closed!")
        my_kwargs={}
        self.func_exec('close',**my_kwargs)
        ## delete from _pin_list
        for p in self.pins:
            if p in self.remote_server._pin_list:
                self.remote_server._pin_list.remove(p)
        self._closed=True

    def open(self):
        self.command='open'
        ## is open ##
        if self._closed==False:
            raise ValueError("Device is open!")
        my_kwargs={}
        self.func_exec('_create',**my_kwargs)
        for p in self.pins:
            if p not in self.remote_server._pin_list:
                self.remote_server._pin_list.append(p)
        self._closed=False

    def getProperty(self,my_property):
        try:
            return self.get(property=(my_property,))[my_property]
        except:
            return None
        
    def execute(self):
        # data transfer
        data=f"{self.obj_type} "
        data +=  f"{self.command} {self.numbering} {self.pins} "
        
        match self.command:
            case 'get': # only verification
                if self.kwargs=={}: 
                    logger.info(f"{self.obj_type} {self.command} refused: no parameter ")
                    return None
                if len(self.kwargs) != 1: 
                    logger.info(f"{self.obj_type} {self.command} refused: exact one parameter allowed")
                    return None
                if 'property' not in self.kwargs.keys():
                    logger.info(f"{self.obj_type} {self.command} refused: expected property=(...)")
                    return None
                ## property=... expects a property as string or a list of properties as strings
                for value in self.kwargs.values():
                    if type(value)==str:
                        value=(value,)
                    if type(value)!=tuple:
                        logger.info(f"{self.obj_type} {self.command} refused: property must be tuple")
                        return None
                    data+=f"{'property'}={value};"
                data=data[0:-1]
                data+='\n'
            case 'set': 
                    if self.kwargs=={}: 
                        logger.info(f"{self.obj_type} {self.command} refused:no parameter")
                        return None
                    for key, value in self.kwargs.items():
                        data+=f"{key}={value};"
                    if self.kwargs!={}:
                        data=data[0:-1]
                        data+='\n'
                                
            case _: 
                for key, value in self.kwargs.items():
                    data+=f"{key}={value};"
                if self.kwargs!={}:
                    data=data[0:-1]
                data+='\n'

        with self.remote_server.conn_lock:
            self.client_socket.sendall(data.encode())
            self.client_socket.settimeout(3.0)
            ret=self.client_socket.recv(1024).decode()
            self.client_socket.settimeout(None)           
            if not ret:
                raise RuntimeError('Server has terminated connection')

            match ret[0:2]:
                case "??": 
                    logger.info(ret)
                    raise RuntimeError(ret)
                case "!G":
                    ### message to get-command from server ###   
                    return eval(ret[2:])
                case _:
                    return None
            
    def func_exec(self,name,**func_kwargs):
        self.command=name
        self.kwargs.clear()

        for key,value in func_kwargs.items():
            self.kwargs[key]=value
        ret=self.execute()
        return ret

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
        self.command='source'
        if self._sourceThread !=None:
            #soft kill of thread
            self._sourceEvent.set()
            while self._sourceEvent.is_set():
                pass
            self._source=None
            self._sourceThread = None
        if quelle==None:   
            return
        if not issubclass(type(quelle),RemotePinDevice):
            if not issubclass(type(quelle),Device) and \
                not isinstance(quelle,Generator) and \
                not isgeneratorfunction(quelle):
               raise ValueError(f"Source {quelle} not supported")
            else:
                self._sourceThread=Thread(target=self.source_function, args=(quelle,self._sourceEvent),)
                self._sourceThread.start() 
                self._source=quelle
        else:
            self._sourceThread=Thread(target=self.source_function, args=(quelle.values,self._sourceEvent))
            self._sourceThread.start() 
            self._source=quelle

             
    def source_function(self,quelle,ev):
        ## infinite generator expected
        try:
            old_value=None    
            if issubclass(type(quelle),Device):
                xxx=quelle.values
            else:
                if isinstance(quelle,Generator):
                    xxx=quelle
                else:
                    if isgeneratorfunction(quelle):
                        xxx=quelle()
                    else:
                        raise ValueError(f"Source {quelle} not supported")
            
            for wert in xxx:
                if wert!=old_value:
                    self.value=wert
                    old_value=wert
                if ev.is_set():
                    break
                    
        except Exception as e:
            logger.info(str(e))
        finally:
            ev.clear()
###########################################################
    @property
    def value(self): 
        self._value=self.getProperty('value') 
        return self._value 
    @value.setter
    def value(self, wert):     
        self.func_exec('set',value=wert)
        self._value=wert
#############################################################
    @property
    def values(self):
        """
        An infinite iterator of values read from :attr:`value`.
        """
        while True:
            try:
                sleep(self._source_delay)           
                yield self.value
            except Exception:
                break
##########################################################################
##########################################################################

class RemoteDigitalDevice(RemotePinDevice):
    def __init__(self, remote_server, obj_type, *args,**kwargs):
        pins,kwargs = self.argsTranslator(*args,**kwargs)
        qs=[]
        kwargs1={}
        for key, value in kwargs.items():
            kwargs1[key]=value
        numbering=kwargs1.pop('numbering') 

        for q in pins:
            pin_number_new,numbering_new = remote_server.map_b_to_g(q,numbering)
            ret=remote_server.pinExists(pin_number_new,numbering_new)
            if ret==True:
                raise ValueError('(('+ str(numbering) + '), ' + str(q) + ') already created as ' + 
                                    '((' + str(numbering_new) + '), ' + str(pin_number_new)+')')
            qs.append(pin_number_new)
        qs1=tuple(qs) 
              
        RemotePinDevice.__init__(self,remote_server, obj_type, qs1, numbering='g', **kwargs1)
        remote_server._pin_list+=pins

        ## for some necessary locking
        self._Lock = Lock()
        self._create()

    def argsTranslator(self,*args,**kwargs):
        if args[-1]=='b' or args[-1]=='g':
                kwargs['numbering']=args[-1]
                args1=args[0:-1]
        else:
            if 'numbering' not in kwargs.keys():
                kwargs['numbering']='g'
            args1=args
        return args1,kwargs    
#############################################################
### parametrizable methods for when_... properties
#############################################################
    def _when_task(self,when_text,wert,thread_dict):
        if wert==None:
           thread_dict[when_text][0]=None
           return 
        if not (isfunction(wert) or ismethod(wert)):
           raise TypeError(f"{wert} is not a function or method")         
        sig = signature(wert)   
        count_positional=0
        for name, param in sig.parameters.items():
            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                count_positional=+1
        if count_positional>1:
            raise TypeError('more than 1 positional(mandatory) parameters')
        
        if not thread_dict[when_text][1] is None:
            thread_dict[when_text][0]=None
            while thread_dict[when_text][1]!= None and thread_dict[when_text][1].is_alive():
                pass
        thread_dict[when_text][0]=wert
        thread_dict[when_text][1]=Thread(target=thread_dict[when_text][2], args=(when_text,wert,thread_dict),)
        try:
            thread_dict[when_text][1].start() 
        except:
            thread_dict[when_text][0]=None
            logger.info(f"{when_text} = {str(wert)} has failed")

    def _when_thread_function(self,when_text,func,thread_dict):
        try:
            old_value=None
            for value in thread_dict[when_text][3](when_text,thread_dict):
                #starting condition
                if old_value==None:
                    old_value=value
                    continue
                else:
                    #change situation
                    if old_value!=value:
                        if value == True:
                                if not func is None:  
                                    wp=0
                                    sig = signature(func)
                                    for name, param in sig.parameters.items():
                                        if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                            wp=+1
                                            break
                                    if wp==0:
                                        func()
                                    else:
                                        func(self)
                                else:
                                    break
                        else:
                            pass
                        old_value=value
        except Exception as e:
            logger.error(f"{str(e)}")
        finally:
            thread_dict[when_text][0]=None
            thread_dict[when_text][1]=None     
            
##################################################################
## special treatment for when_held
##################################################################
    def _when_wh_function(self,when_text,func,thread_dict):
        try:
            for value in thread_dict[when_text][3](when_text,thread_dict):
                if value==True:
                    if not func is None:
                        wh=0
                        sig = signature(func)
                        for name, param in sig.parameters.items():
                            if str(param.kind)=='POSITIONAL_OR_KEYWORD':
                                wh=+1
                                break
                        if self.hold_repeat:
                            while not thread_dict[when_text][0] is None:
                                if wh==0:
                                    func()
                                else:
                                    func(self)
                                sleep(self.hold_time)
                            else:
                                break
                        else:
                            if wh==0:
                                func()
                            else:
                                func(self)
                            self.wait_for_release()
                        if thread_dict[when_text][0] == None:
                            break
                    else:
                        thread_dict[when_text][0] = None
                        break
                   
        except Exception as e:
            logger.error(f"{str(e)}")
        finally:
            thread_dict[when_text][0] = None
            thread_dict[when_text][1] = None
#########################################################################
## for parametrizing of wait_for... funtions
#########################################################################
    def _wait_task(self,wait_text,gen_function,**my_kwargs):
        if 'timeout' in my_kwargs.keys():
            if not my_kwargs['timeout'] is None:
                t=Timer(my_kwargs['timeout'],timeOut,(self.obj_type,wait_text))
                t.start()
                while t.is_alive(): 
                    for value in gen_function(wait_text):
                        if value==True:
                            t.cancel()
                            return 0
                        break
                else:
                    return 1   
        for value in gen_function(wait_text):
            if value==True:
                return 0

#############################################################
############################################################# 
# Example usage:
#############################################################
#############################################################
if __name__ == "__main__":
    from gpiozero.tones import Tone
    from colorzero import Color,Red,Green,Blue
    from signal import pause 
    from time import sleep
    try:
        time = 2000
        server_ip = "raspy5"
        server_port = 8509
    

        # Create instance of remote Raspberry Pi
        remote_server = RemoteServer(server_ip, server_port)
        
        from gpiozero import * #TrafficLights,RGBLED,LED,Button,PWMLED
        from time import sleep
        from signal import pause

        #lights = RGBLED(21, 20, 16)
        #lights = LED(21)
        #lights.source = led_light_sequence()

        def gen():
                try:
                    while True:
                        yield 1
                        sleep(1)
                        yield 0
                        sleep(1)
                except:
                    pass

        def traffic_light_sequence():
            while True:    
                yield (0,0,1) # green
                sleep(10)
                yield (0,1,0) # amber
                sleep(1)
                yield (1,0,0) # red
                sleep(10)
                yield (1,1,0) # red+amber
                sleep(1)
        #remote_pin = remote_server.pin(21, 'g')
        #remote_pin1 = remote_server.pin((20,),  'g')
        #remote_pin2 = remote_server.pin( (16,), 'g')

        #remote_tuz = remote_server.tuz(21, 'g')
        
        #remote_rgb.set(color="Color('yellow')")
        
        #remote_buz.beep(on_time=2,off_time=3)
        #sleep(5)
        
        
        #remote_tuz.play(tone="Tone(frequency=500.0)")
        #remote_tuz.play(tone="Tone(midi=71)")
        #remote_tuz.play(tone=220.0)
        #remote_tuz.play(tone="Tone('A4')")
        #while True:
        #    remote_tuz.play(tone="'A4'")
        #    sleep(4.0)
        #    remote_tuz.stop()
        #    sleep(4)
        #print(remote_buz.get(property='pin'))
        #print(remote_buz.getProperty('is_lit'))
        #while True:
        #    pass
        #remote_led.set(value='(1,1,1)')
        #sleep(5)
        #if  remote_led.is_lit():
            #print('Halo')
            #print(remote_led.get(property=('closed',))['closed'])
            #pass        

        #logger.info(eval(message))
        #val=eval(message)['value']
        #logger.info(val)
        #remote_led.off()
        #z=0
        
        #remote_led.close()
        #print(remote_led.closed)
        #print(remote_led.getProperty('is_lit'))
        #print(remote_led.getProperty('is_active'))

        #remote_led.open()
        #remote_led.set(value='(1,1,1)')
        #print(remote_led.closed)
        #print(remote_led.getProperty('closed'))
        #print(remote_led.getProperty('is_active'))    
            
        #z=z+1
        
        #while True:
        #    pass
        #remote_pin1 = remote_server.pwmled(38, 'b')
        #remote_pem=remote_server.asr((16,), 'g')
        def wpfunc(x):
            logger.info(f"wp {x}")
        def wrfunc(x):
            logger.info(f"wr {x}")
        def whfunc(x):
            logger.info(f"wh {x}")
        
        def wlfunc(x):
            logger.info(f"wl {x}")
        def wnlfunc(x):
            logger.info(f"wnl {x}")
        def wmfunc(x):
            logger.info(f"wm {x}")
        def wnmfunc(x):
            logger.info(f"wnm {x}")
        def wllsfunc(x):
            logger.info(f"wlls {x}")
        def wllsdfunc(x):
            logger.info(f"wllsd {x}")
        def wdsifunc(x):
            logger.info(f"wdsi {x}")
        def wdsofunc(x):
            logger.info(f"wdso {x}")
        #def wrofunc(x):
        #    logger.info(f"wro {x} {remote_ro._steps_saved_wr}")
        #def wrocfunc(x):
        #    logger.info(f"wroc {x} {remote_ro._steps_saved_wr_c_cc}")           
        #def wroccfunc(x):
        #    logger.info(f"wrocc {x} {remote_ro._steps_saved_wr_c_cc}")
            
        
            
        #remote_pin = remote_server.pinDevice('PWMLED',(40,),'b')
        #remote_pin1 = remote_server.pinDevice('PWMLED',(20,), 'g')
        #remote_pin2 = remote_server.pinDevice('PWMLED',(16,), 'g')
        #button=remote_server.pinDevice('Button',5,'g',pull_up=False)
        #remote_mcp=remote_server.pinDevice('MCP3208',8,channel=0) # select_pin = 8
        #remote_ls=remote_server.pinDevice('LineSensor',6,'g')
        #remote_ms=remote_server.pinDevice('MotionSensor',13,'g')
        #remote_lls=remote_server.pinDevice('LightSensor',19,'g')
        #remote_lb=remote_server.pinDevice('LEDBarGraph',16,20,21,'g',pwm=True)
        #remote_lb.source=remote_mcp
        #remote_lb2.source=remote_lb
        #remote_lb3.source=remote_lb
        #remote_lb.value=2/3
        #sleep(5)
        #remote_lb.value=-1/3
        #sleep(5)
        #remote_lb.value=-2/3
        #sleep(5)
        #remote_lb.value=1
        
        #remote_ds.close()
        #remote_ds.open()
        #remote_pin.source=remote_ds
        #remote_ro=remote_server.pinDevice('RotaryEncoder',(37,13),numbering='b',wrap=True) # 
        #sleep(10)
        #button1=Button(5)
        #remote_pin.on()
        
        pause()
        #remote_ro.wait_for_rotate()
        #print('wr')
        #remote_ro.wait_for_rotate_clockwise()
        #print('wrc')
        #remote_ro.wait_for_rotate_counter_clockwise()
        #print('wrcc')
        #remote_ro.when_rotated=wrofunc
        #remote_ro.when_rotated_clockwise=wrocfunc
        #remote_ro.when_rotated_counter_clockwise=wroccfunc
        
        #remote_ls.threshold=0.6
        #print(remote_ls.values)
        #remote_pin.source= remote_lls
        
        #remote_pin.blink()
        #remote_ls.wait_for_no_line()
        #remote_ls.wait_for_line()
        #remote_pin.source=remote_mcp
        #remote_pin1.source=remote_pin
        #remote_pin2.source=remote_pin1
        #logger.info(remote_mcp.voltage)
        #print(remote_mcp.value)
        #remote_pin.source=traffic_light_sequence
        #remote_pin.blink()
        #remote_pin1.source=remote_pin
        #remote_pin2.source=remote_pin1
        #ret =button.wait_for_press()
        #print(ret)
        #sleep(100)
        #button.hold_time=1.0
        #button.when_pressed=wpfunc
        #button.when_released=wrfunc
        #button.when_held=whfunc
        #remote_ls.when_line=wlfunc
        #remote_ls.when_no_line=wnlfunc
        #remote_ms.when_motion=wmfunc
        #remote_ms.when_no_motion=wnmfunc
        #print(remote_lls.is_active)
        #remote_pin.source=remote_ds
        #remote_ds.when_in_range=wdsifunc
        #remote_ds.when_out_of_range=wdsofunc
        #remote_ds.wait_for_out_of_range()
        #remote_ds.wait_for_in_range()
        #while True:
        #    sleep(1)
        #    print(remote_ds.distance)
        pause()
        #remote_lls.when_light=wllsfunc
        
        #remote_lls.when_dark=wllsdfunc
        #remote_lls.wait_for_light()
        #remote_lls.wait_for_dark()
        #button.wait_for_press()
        #button.wait_for_release(timeout=3)
        #remote_ls.wait_for_no_line(timeout=3)
        #remote_ls.wait_for_line()
 
        pause()
        #remote_pin.source=button
        #sleep(1.0)
        #button.when_pressed=None
        #button.when_released=None
        #button.when_held=None
        #pause()
        #button.hold_repeat=False
        
        #button.when_held=whfunc
        #sleep(1)
        #button.when_pressed=None
        #button.when_released=None
        #pause()
        #button.when_pressed=remote_pin.blink
        #button.when_released=remote_pin.off
        #remote_pin.source=button
        #logger.info(remote_pin._source)
        #remote_pin1.source=remote_pin
        #remote_pin2.source=remote_pin1
        #logger.info(remote_pin._source)
        #led.pulse()
        #remote_pin1.source=led
        #while True:
        #     sleep(1)
        #    logger.info(remote_mcp.value)
        #    pass
        #sleep(15)
        #print(remote_pin.source)
        #remote_pin.source=None
        #print(remote_pin.source)
        #remote_pin.source=traffic_light_sequence
        #print(remote_pin.source)
        #z=0
        #while z<1:   
            # Create instance of remote Raspberry Pi
            #remote_server = RemoteServer(server_ip, server_port)
            #remote_pin1 = remote_server.pin(38, 'b')
            
            #remote_pin.play(tone="Tone('A4')")
            #remote_pin.get(property='is_active')
            ##x=remote_pin.value
            #print(x)
            #sleep(2)
            #remote_pin.value=0
            #print(remote_pin.value)
            #remote_pin.source=Button(5)
            #print(remote_pin.source)
            #print(remote_pin.max_tone)
            #print(remote_pin.mid_tone)
            #print(remote_pin.min_tone)
            #print(remote_pin.octaves)
            #print(remote_pin.tone)
            #print(remote_pin.all)
            #print(remote_pin.is_active)
            #print(remote_pin.active_high)
            #print(remote_pin.is_lit)
            #print(remote_pin.closed)
            #print(remote_pin.frame_width)
            #print(remote_pin.pulse_width)
            #print(remote_pin.max_pulse_width)
            #print(remote_pin.min_pulse_width)
            #print(remote_pin.max_angle)
            #print(remote_pin.min_angle)
            #print(remote_pin.angle)
            #print(remote_pin.pin_factory)

        #while True:
        #    pass
            #remote_pin._create()
            #remote_pin1 = remote_server.pin(38, 'b') 
            # Demo features
            #remote_pem.max()
            #sleep(5)
            #remote_pem.mid()
            #sleep(5)
            #remote_pem.min()
            #sleep(5)
            #remote_pem.detach()
            #sleep(5)
            #remote_pem.set(value=0.6)
            #z=z+1
            #message=remote_pem.get(property=(
            #            'is_active',
            #            'value',
            ##            'all',
            #            'angle',
            #            'max_angle',
            #            'min_angle',
            #            'closed',
            #            'frame_width',
            #            'pulse_width',
            #            'max_pulse_width', 
            #            'min_pulse_width', 
            #            'pin_factory'
            #    ))
            #logger.info(message)
            #message=remote_rgb.get(property=('value','is_active'))
            #
            #logger.info(message)
            #while True:
            #    pass
    
            #sleep(5)
            #remote_rgb.pulse(fade_in_time=1,fade_out_time=1)
            #sleep(5)
            #remote_rgb.blink(on_time=2,off_time=2,fade_in_time=0,fade_out_time=0)
            #sleep(15)
            #z=z+1
            #sleep(5)

        #while True:
        #    pass
            #remote_pin.off() 
            #sleep(4)
            #remote_pin1.on() 
            #remote_pin.on() 
            #remote_pin1.on() 
            #remote_pin2.on() 
        # sleep(10)
        # remote_pin.off ()
        # remote_pin1.off()
            #remote_pin2.off()
            #remote_pin.value(arg1=0.1)
            #logger.info(remote_pin.get(property='value'))
            #remote_pin1.set(value=0.4)
            #remote_pin2.set(value=0.6)
            #logger.info(remote_pin2.get(property='value'))
            #sleep(4)
            #remote_pin.value(arg1=0)
            #logger.info(remote_pin.get(property='value'))
            #logger.info(remote_pin.get(property='values'))
            #logger.info(remote_pin.get(property='source'))
            #logger.info(remote_pin.get(property='is_active'))
            #logger.info(remote_pin.get(property='closed'))
            #logger.info(remote_pin.get(property='pin'))
            #logger.info(remote_pin.get(property='frequency'))
            #logger.info(remote_pin.get(property='active_high'))
            #logger.info(remote_pin.get(property='pin_factory'))
            #sleep(10)
            #remote_pin.blink(on_time=1,off_time=1)
            #remote_pin1.blink(on_time=1,off_time=1)
            #remote_pin2.blink(on_time=1,off_time=1)
            #sleep(10)
            #remote_pin.off ()
            #remote_pin1.off()
            #remote_pin2.off()
            #sleep(10)
            #remote_pin.pulse(fade_in=1,fade_out=1)
            #remote_pin1.pulse(fade_in=1,fade_out=1)
            #remote_pin2.pulse(fade_in=1,fade_out=1)
            #sleep(10)
            #remote_pin.off ()
            #remote_pin1.off()
            #remote_pin2.off()
            #sleep(10)
            #z=z+1

        #while True:
        #        pass


        #sleep(4)
        
        #remote_pin.close()
        #remote_pin1.close()
        #sleep(4)
        #remote_pin.close()
        #remote_pin.off(time_ms=4000) 
        #remote_pin1.off(time_ms=4000) 
        #sleep(10)        

        #remote_pin.blink(time_ms=4000)
        #remote_pin1.blink(time_ms=4000)
        #sleep(4)
        
        #remote_pin.off ()
        #remote_pin1.off()
        #remote_pin2.off()
        #while True:
        #    pass

        #sleep(4)

        #remote_pin.pulse(time_ms=4000,fading_in_time=0.5,fading_out_time=0.5)
        #remote_pin1.pulse(time_ms=4000)
        #sleep(4)
        #remote_pin.off (time_ms=4000)
        #remote_pin1.off (time_ms=4000)
        #sleep(4)
        #remote_pin.blink(time_ms=4000,arg1=0.5,off_time=2.0)
        #remote_pin1.blink(time_ms=4000,on_time=0.003,arg2=0.003)
        #sleep(4)
        #remote_pin.off (time_ms=4000)
        #remote_pin1.off (time_ms=4000)
        #sleep(4)
        #remote_pin.value(arg1=0.4)
        #remote_pin1.set(value=0.1)
        #sleep(4)
        #remote_pin.off (time_ms=4000)
        #remote_pin1.off (time_ms=4000)
        #sleep(4)
        #remote_server.close()  

        #z=z+1
        

        #while True:
        #   pass
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")
    
