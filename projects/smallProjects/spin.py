import random


for i in range(10000):
    num = random.randint(0,100)
    i += 1
    
if num > 50 :
    print(63)
    print('The random number was 63')
else: 
    print(27)
    print('The random number was 27')