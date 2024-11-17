#!/usr/bin/env python3
from remoteio import *
#from remoteio import RemoteServer,map_bg
#from remoteio import getFunctions,getReadOnlyProperties,getWriteableProperties
from gpiozero import *
from signal import pause
from time import sleep
import logging
logging.basicConfig(level=logging.INFO,style="{",format="{asctime}[{levelname:8}]{message}")
logger = logging.getLogger(name="remoteio")
logger.setLevel(logging.INFO)


if __name__=='__main__':
    server_ip = "192.168.178.136"
    server_port = 8509
    # Create instance of remote Raspberry Pi
    rs = RemoteServer(server_ip, server_port)


######################################################################################
# Remote_LED
######################################################################################
#    #l=LED(16)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l))
#    #print(getWriteableProperties(l))
#
#    
#    # Create instance of remote Raspberry Pi
#    rs = RemoteServer(server_ip, server_port)
#    rl=Remote_LED(rs,pin=21)
#    rl.on(on_time=5.0) # on_time in sec instead of time_ms: harmonizing with gpiozero
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
#
######################################################################################
#Remote_PWMLED
######################################################################################       
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
#
##########################################################################################
# Remote_RGBLED
##########################################################################################
    #l=RGBLED(16,20,21)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
       
#    #Create instance of remote Raspberry Pi
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
#
##################################################################
# Remote_Buzzer
##################################################################  
    #l=Buzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
    #   
#    # Create instance of remote Raspberry Pi
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
#
####################################################################
# Remote_TonalBuzzer
####################################################################
    #l=TonalBuzzer(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

#    #rl=Remote_TonalBuzzer(rs,pin=map_bg(40,'b'))
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
#   
#####################################################################
# Remote_Motor
#####################################################################
    #l=Motor(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
#    #Create instance of remote Raspberry Pi
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
#
############################################################
# Remote_PhaseEnableMotor
############################################################
    #l=PhaseEnableMotor(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
#    #Create instance of remote Raspberry Pi
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
#
########################################################################
# Remote_Servo
########################################################################
    #l=Servo(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

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
#    pause()
#
##################################################################
# Remote_AngularServo
##################################################################
    #l=AngularServo(16)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   
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
########################################################################
#    from remoteio import Remote_Button
########################################################################
#    def wpfunc(x):
#           logger.info(f"wp {x}")
#    def wrfunc(x):
#        logger.info(f"wr {x}")
#    def whfunc(x):
#        logger.info(f"wh {x}")
#
#    
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
#    pause()
#
############################################################################
# Remote_MCP3208
############################################################################
#    #l=MCP3208(0,0)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l))
#    #print(getWriteableProperties(l))
#
#    rl=Remote_MCP3208(rs,0)   # GPIO Pin 8 is the select pin
#    rp=Remote_PWMLED(rs,21)
#    rp.source=rl
#    while True:
#        sleep(0.1)
#        print(rl.value)
#    pause()
#
##############################################################################
# Remote_LineSensor
##############################################################################
    #l=LineSensor(5)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

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
#    pause()
#
###########################################################
# Remote_MotionSensor
###########################################################
        #l=MotionSensor(5)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))

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
#
#####################################
# Remote_LightSensor
#####################################
####### not tested because no light sensor in the archiv #####
#    #l=LightSensor(5)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l)
#    #print(getWriteableProperties(l))
#
#    def wmfunc(x):
#        print(f"wm {x}")
#    def wnmfunc(x):
#        print(f"wnm {x}")
#
#    rl=Remote_LightSensor(rs,5)   
#    rp=Remote_PWMLED(rs,21)
#    while True:
#        sleep(.5)
#        print(rl.is_active)
#    rp.source=rl
#    rl.wait_for_dark()
#    print('A')
#    rl.when_dark=wnmfunc
#    rl.wait_for_light()
#    print('B')
#    rl.when_light=wmfunc
#    rl.when_dark=wnmfunc  
#
#   pause()
#
########################################
# Remote_DistanceSensor
#######################################
    #l=DistanceSensor(22,26)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l)
    #print(getWriteableProperties(l))

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
#    pause()
#
###########################################################
# Remote_RotaryEncoder
###########################################################
    #l=RotaryEncoder(26,22)
    #print(getFunctions(l)
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))

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
#    pin=map_bg(29,'b')  # GpioPin 5
#    rl=Remote_RotaryEncoder(rs,a=19,b=26, wrap=True)           # CLK, DT
#    rl.activateSW(pin,pull_up=True)                            # push button of the rotary encoder, default pull_up=True
#    #or
#    #rl.SW=Remote_Button(rs,pin,pull_up=true)        # SW pullup=True expected by the rotary encoder used here
#
#    rl.SW.when_pressed = rl.reset_counter           # method not function, because dependent from object
#                                                    # well interpreted by gpiozero
#    print(rl.SW.ident)                 
#    rp=Remote_PWMLED(rs,21)
#    print(rl.is_active)
#    rl.when_rotated=wrfunc               # function
#    rl.when_rotated_clockwise=wrcfunc    # function
#    rl.when_rotated_counter_clockwise=wrccfunc # method
#    rl._source_delay=0.01                 # generator_function of rl made slower, seems fast enough
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
#    pause()
#
###############################################################################
#    from remoteio import Remote_LEDBoard
###############################################################################
    #l=LedBoard(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))    

#    # _order in combination with named leds defines how the property value has to be interpreted.
#    # here value=(led1.value,led2.value,led3.value)
#    #rl=Remote_LEDBoard(rs,led2=16,led1=20,led3=21,pwm=True,_order=('led1','led2','led3'))
#    #rl.value=(1,0,1) # pin20,pin16,pin21
#    #logger.info(RemoteDigitalDevice.value.fget(rl))
#    #pause()
#
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
#    #pause()
#    print(rl.is_active)
#    sleep(10)
#    rl.off(-1)
#    sleep(10)
#    rl.toggle(0,1,2)
#    pause()
#
####################################################################
#    from remoteio import Remote_LEDBarGraph
####################################################################
        #l=LEDBarGraph(16,20,21)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l)) 
        #print(getWriteableProperties(l)) 
        # curiously lit_count is changeable

#    rl = Remote_LEDBarGraph(rs,16,20,21)
#    remote_mcp=Remote_MCP3208(rs,0,0)
#    #print(remote_mcp.value)
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
#
##########################################################################
# Remote_Compositum
#########################################################################
#    rl1=Remote_RGBLED(rs,16,18,20,pwm=True)
#    rl2=Remote_PWMLED(rs,22)
#    rl3=Remote_PWMLED(rs,21)
#    rc=Remote_Compositum(rl1,rl2)
#    rc1=Remote_Compositum(rc,rl3)
#    rl1.setClientIdent('rs.rl1')       # is valid for all remote devices
#    rl2.setClientIdent('rs.rl2')
#    rl3.setClientIdent('rs.rl3') 
#    rc.setClientIdent('__.rc')
#    rc1.setClientIdent('__.rc1') 
#    print(rl1.getClientIdent())        # is valid for all remote devices
#    print(rl2.getClientIdent())  
#    print(rl3.getClientIdent())
#    print(rc.getClientIdent())
#    print(rc1.getClientIdent())
#    print([child.getClientIdent() for child in rc1._childs])
#    print([element.getClientIdent() for element in rc1._gpiozero_elements])
#    rl1.on()
#    rl2.on()
#    rl3.on()
#    print(rl1.value)
#    print(rl2.value)
#    print(rl3.value)
#    rc1.off()
#    rc1.on(-1)
#    print(rc1.value)
#    sleep(5)
#    rc1.off(-2,-1)
#    print(rc1.value)
#    sleep(5)
#    rc1.toggle(0,1)
#    print(rc1.value)
#    sleep(5)
#    rc1.value={rc.getClientIdent(): {rl1.getClientIdent(): (0,1,0), rl2.getClientIdent(): 1}, rl3.getClientIdent(): 0}
#    print(rc1.value)
#    sleep(5)
#    rc1.pulse()
#    pause()
