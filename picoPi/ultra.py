from machine import Pin
import utime

rightTrigger = Pin(2, Pin.OUT)
rightEcho = Pin(3, Pin.IN)

leftTrigger = Pin(16, Pin.OUT)
leftEcho = Pin(17, Pin.IN)

frontTrigger = Pin(14, Pin.OUT)
frontEcho = Pin(15, Pin.IN)

def ultra(trigger, echo):
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   
   while echo.value() == 0:
       signaloff = utime.ticks_us()
       
   while echo.value() == 1:
       signalon = utime.ticks_us()
       
   timepassed = int(signalon) - int(signaloff)
   distance = (timepassed * 0.0343) / 2
   return distance

while True:    
    print(f"This is the distance to the right wall: {ultra(rightTrigger, rightEcho)} cm")
    print(f"This is the distance to the left wall: {ultra(leftTrigger, leftEcho)} cm")
    print(f"This is the distance to the front wall: {ultra(frontTrigger, rightEcho)} cm")
    print("")
    utime.sleep(1)