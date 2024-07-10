import random

uppercaseLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercaseLetters = uppercaseLetters.lower()
digits = "0123456789"
symbols = "!@#$%^&*(){}|:<>?,.;'[]_+-=~` "

upper, lower, nums, syms =  True, True, True, True

all = ""

if upper: 
    all += uppercaseLetters
if lower:
    all += lowercaseLetters
if nums:
    all += digits
if syms:
    all += symbols

length = int(input("What is the length of the password: "))
amount = int(input("Enter the amount: "))

for x in range(amount):
    password = "".join(random.sample(all, length))
    print(password)