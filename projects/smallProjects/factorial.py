def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

# Get user input
num = int(input("Enter a number to calculate its factorial: "))

# Calculate and display the factorial
result = factorial(num)
print(f"The factorial of {num} is {result}")
