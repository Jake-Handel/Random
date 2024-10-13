from machine import Pin
from time import sleep

pin = Pin("LED", Pin.OUT)

while True:
    try: 
        pin.toggle()
        sleep(1)
    except KeyboardInterrupt:
        break
pin.off()
print("Finished. ")