#!/usr/bin/env python3
from remoteio import RemoteServer
from time import sleep
from signal import pause
from gpiozero import *
from remoteio import getFunctions,getReadOnlyProperties,getWriteableProperties


if __name__=='__main__':
    server_ip = "raspy5"
    server_port = 8509
    # Create instance of remote Raspberry Pi
    rs = RemoteServer(server_ip, server_port)

    #from remoteio import getFunctions, getReadOnlyProperties,getWriteableProperties
######################################################################################
    from remoteio import Remote_LED
        #l=LED(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
    #
    ### Example Remote_LED ##
    ## Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_LED(rs,21)
    #rl1=Remote_LED(rs,20)
    #print(rl.is_active)
    #rl1.source=rl
    #print(rl1.source)
    #rl.blink()
    #sleep(5)
    #print(rl.active_high)
    #rl.on()
    #print(rl.is_active)
    #sleep(5)
    #rl.off()
    #sleep(5)
    #rl.toggle()
    #pause()
######################################################################################
    from remoteio import Remote_PWMLED
    
        #l=PWMLED(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
    ##   
    ## Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_PWMLED(rs,21)
    #rl1=Remote_PWMLED(rs,20)
    #rl1.source=rl
    #rl.blink()
    #sleep(5)
    ##rl.pulse(time_ms=5000) # leads to pipe connection timed out
                            # there is a timeout of 3 seconds, but
                            # the concerned process takes no further command along 5 seconds
    #rl.pulse()
    #sleep(6)
    #rl.on()
    #sleep(5)
    #rl.off()
    #sleep(5)
    #rl.toggle()
    #pause()
##########################################################################################
    from remoteio import Remote_RGBLED
        #l=RGBLED(16,20,21)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
       
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
    #from remoteio import Remote_Buzzer
    #rl=Remote_Buzzer(rs,40,'b')
        #l=Buzzer(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
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
####################################################################
    from remoteio import Remote_TonalBuzzer
        #l=TonalBuzzer(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
   
    #Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    #rl=Remote_TonalBuzzer(rs,40,'b')
    #print(rl.all)
    #rl.play(tone="Tone('A4')")
    #sleep(4)
    #rl.stop()       # signal stays high or low at the end --> no tone
    #                # but simulation with LED  let LED with light even if there is no tone
    #                # try with speaker
    #sleep(5)
    #rl.value=None
    #sleep(5)
    #rl.tone=220.0
    #sleep(4)
    #rl.stop()
    #sleep(4)
    #print(rl.tone)
    #sleep(5)
    #pause() 
####################################################################################
    from remoteio import Remote_Motor
        #l=Motor(16,20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
   
    ##Create instance of remote Raspberry Pi
    #rs = RemoteServer(server_ip, server_port)
    rl=Remote_Motor(rs,17,27,enable=22)
    #rl=Remote_Motor(rs,17,27,22) # also ok
    print(rl.all) 
    
    b=Button(5)  # not remote
    rp=Remote_PWMLED(rs,21)
    
    i=0
    while i<=109:
        print(i%2)
        if i%2 ==0:
            rp.source=rl
        else:
            rp.source=b
        rl.forward()
        sleep(4)
        rl.stop()
        print(rl.is_active)
        rl.reverse()
        sleep(4)
        rl.backward()
        print(rl.is_active)
        sleep(4)
        rl.stop()
        sleep(5)
        rl.forward()
        rl.value=0.5
        i+=1
        
    #pause()   
############################################################
    from remoteio import Remote_PhaseEnableMotor
        #l=PhaseEnableMotor(16,20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))

    #rl=Remote_PhaseEnableMotor(rs,16,20)
    #while True:
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
    #   sleep(4)
    #    rl.stop()
    #    sleep(5)
    #    pause()
########################################################################
#    from remoteio import Remote_Servo
#       #l=Servo(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
#   
#    rl=Remote_Servo(rs,26)
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
    from remoteio import Remote_AngularServo
        #l=AngularServo(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))
   

#    rl=Remote_AngularServo(rs,26)
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
    from remoteio import Remote_Button
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

        #l=Button(20)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))

#    rl=Remote_Button(rs,5,hold_repeat=False,pull_up=True)
#    rl.hold_time=1.0
#    logger.info(rl.hold_time)
#    #rl.hold_repeat=True
#    logger.info(rl.hold_repeat)
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
    from remoteio import Remote_MCP3208
        #l=MCP3208(0,0)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))

#    ## take a potentiometer to feed chnnel 0 of the MCP
#    rl=Remote_MCP3208(rs,8,channel=0)   # GPIO Pin 8 is the select pin, rs and select pin are positional arguments
#    rp=Remote_PWMLED(rs,21)
#    rp.source=rl
#    while True:
#        sleep(0.1)
#        print(rl.value)
#    pause()
##############################################################################
    from remoteio import Remote_LineSensor
        #l=LineSensor(5)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l))
        #print(getWriteableProperties(l))

#   def wlfunc(x):
#        print(f"wl {x}")
#    def wnlfunc(x):
#        print(f"wnl {x}")
#
#    rl=Remote_LineSensor(rs,5)   
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
    from remoteio import Remote_MotionSensor
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
###########################################################
    from remoteio import Remote_LightSensor
#    ####################################
#    # try functions one after the other
#    #l=LightSensor(5)
#    #print(getFunctions(l))
#    #print(getReadOnlyProperties(l)
#    #print(getWriteableProperties(l))
#    #####################################
#
#  not tested because no lightsensor here!!!
#  a lightsensor can be made by an ADC-converter and a photoresistor
#    def wmfunc(x):
#        print(f"wm {x}")
#    def wnmfunc(x):
#        print(f"wnm {x}")
#
#    rl=Remote_LightSensor(rs,8)   
#    rp=Remote_PWMLED(rs,22)
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
    from remoteio import Remote_DistanceSensor
    # 
    #l=DistanceSensor(22,26)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l)
    #print(getWriteableProperties(l))
    #####################################

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
###########################################################
    from remoteio import Remote_RotaryEncoder
    ####################################
    # 
    #l=RotaryEncoder(26,22)
    #print(getFunctions(l)
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



   #or
    #rl=Remote_RotaryEncoder(rs,17,18, wrap=True)   # CLK, DT
    #rb=Remote_Button(rs,27,pull_up=False)          # SW pullup=False important
    #rb.when_pressed = rl.reset_counter  # method, because dependent from object
                                        # well interpreted
                    
#   rp=Remote_PWMLED(rs,21)
#   print(rl.is_active)
#   rl.when_rotated=wrfunc               # function
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
    from remoteio import Remote_LEDBoard
    #l=LedBoard(16,20)
    #print(getFunctions(l))
    #print(getReadOnlyProperties(l))
    #print(getWriteableProperties(l))
   

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
    from remoteio import Remote_LEDBarGraph
        #l=LEDBarGraph(16,20,21)
        #print(getFunctions(l))
        #print(getReadOnlyProperties(l)) 
        #print(getWriteableProperties(l)) 
        # curiously lit_count is changeable


#   rl=Remote_LEDBarGraph(rs,16,20,21)
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

