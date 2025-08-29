from scipy.integrate import quad
import re

integral = input("enter the integration: ")
low = int(input("lowest number: "))
high = int(input("highest number: "))

integral = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', integral)
integral = re.sub(r'([a-zA-Z])(\()', r'\1*\2', integral)
integral = re.sub(r'(\))([a-zA-Z])', r'\1*\2', integral)

def integrand(x):
    return eval(integral)

result, error = quad(integrand, low, high)
print(f"Result of integration: {result}")
print(f"Estimated error: {error}")
