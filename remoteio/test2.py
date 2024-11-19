#!/usr/bin/env python3
from gpiozero import *
from time import sleep

l=LEDBarGraph(20,21)
l.on()
print(l.lit_count)
l.off()
l.value=1/2
print(l.lit_count)
l.lit_count=-1
print(l.lit_count)

