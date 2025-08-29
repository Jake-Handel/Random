def compoundInterest(tP, iM, r):
	for i in range(tP):
		l = iM * (1 + r/100)**i
		print(f"Year is {i + 1}, PRn = ${l}")
	pass

def simpleInterest(tP, iM, r):
	for i in range(tP):
		l = iM * (1 + r/100) * i
		print(f"Year is {i + 1}, PRn = ${l}")
	pass

def superanuation(tP, iM, r):
	pass

def main():
    choice = int(input("What type of interest would you like to use? compound (1), simple (2) or superanuation (3): "))
    tP = int(input("amount of years:  "))
    iM = int(input("Intial Money deposit:  "))
    r = float(input("rate: ")) / 100
    
    if choice == 1:
        compoundInterest(tP, iM, r)
    elif choice == 2:
        simpleInterest(tP, iM, r)
    elif choice == 3:
        superanuation(tP, iM, r)
    else:
        print("Invalid choice")

main()