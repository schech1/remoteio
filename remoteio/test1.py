from gpiozero import *

l1=LEDBarGraph(16,20)
l3=LEDBarGraph(l1,21)
l3.value=1/2