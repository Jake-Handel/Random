def fibbinaci(n):
	if n == 0:
		return 0
	if n == 1:
		return 1
	return fibbinaci(n-1) + fibbinaci(n-2)

print(fibbinaci(int(input("Enter Index: "))))

