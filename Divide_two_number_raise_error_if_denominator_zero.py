print("Enter first number:")
num1 = float(input())

print("Enter second number:")
num2 = float(input())

if num2 == 0:
    raise ValueError("Error: Division by zero")
result = num1 / num2
print("Result:", result)


    