#!/usr/bin/env python2.7
# Script for reading Clarostat 600-128-CBL optical encoder. 
# github/latomja
from datetime import datetime
import RPi.GPIO as GPIO

ch_a=16
ch_b=12

GPIO.setmode(GPIO.BCM)
GPIO.setup(ch_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ch_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class pot:
    def __init__(self,channel_a,channel_b):
        self.latest_0=0
        self.latest_1=0
        self.latest_2=0

        self.channel_a=channel_a
        self.channel_b=channel_b
        
        self.up_a=0
        self.down_a=0
        self.long_a=0

        self.up_b=0
        self.down_b=0
        self.long_b=0
        
        GPIO.add_event_detect(self.channel_a, GPIO.BOTH, self.event)
        GPIO.add_event_detect(self.channel_b, GPIO.BOTH, self.event)
        

    def event(self,channel):
        if channel==self.channel_a:                                                                     # A kanava trigger
            if GPIO.input(self.channel_a):                                                              # A=1 -> nouseva reuna
                self.up_a=int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)        # Nouseva reuna talteen
            else:                                                                                       # A=0 -> laskeva reuna
                self.down_a=int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)      # Laskeva reuna talteen

        if channel==self.channel_b:                                                                     # B kanava trigger
            if GPIO.input(self.channel_b):                                                              # B=1 -> nouseva reuna
                self.up_b=int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)        # Nouseva reuna talteen
            else:                                                                                       # B=0 -> laskeva reuna
                self.down_b=int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)      # Laskeva reuna talteen


        if self.up_a<self.up_b<self.down_a:     # Clockwise. Channel #B rises when channel #A is up
            self.latest_2=self.latest_1         
            self.latest_1=self.latest_0
            self.latest_0=1                 
            if self.latest_2==1 and self.latest_1==1 :  # Let's do some filtering. Three latest reading must be clocwise
                print("Clockwise")

        if self.up_b<self.up_a<self.down_b:     # AntiClockwise. Channel #A rises when channel #B is up
            self.latest_2=self.latest_1
            self.latest_1=self.latest_0
            self.latest_0=0                 
            if self.latest_2==0 and self.latest_1==0:
                print("AntiClockwise")
            

encoder=pot(ch_a,ch_b)

try:
    while(1==1):
        pass

except KeyboardInterrupt:
    GPIO.cleanup()       
GPIO.cleanup()           

