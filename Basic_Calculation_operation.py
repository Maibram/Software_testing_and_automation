def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    if y == 0:
        raise ValueError("Error: Division by zero")
    return x / y


def main():
    try:
        print("Enter first number:")
        num1 = float(input())

        print("Enter second number:")
        num2 = float(input())

        print("Select operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")

        choice = input("Enter choice (1/2/3/4): ")

        if choice == "1":
            print(num1, "+", num2, "=", add(num1, num2))
        elif choice == "2":
            print(num1, "-", num2, "=", sub(num1, num2))
        elif choice == "3":
            print(num1, "*", num2, "=", mul(num1, num2))
        elif choice == "4":
            print(num1, "/", num2, "=", div(num1, num2))
        else:
            print("Invalid input")
    except ValueError as error:
        print(error)


def test_add_two_numbers():
    result = add(10, 10)
    assert result == 20

def test_subtract_two_numbers():
    result = sub(10, 10)
    assert result == 0

def test_multiply_two_numbers():
    result = mul(10, 10)
    assert result == 100

def test_divide_two_numbers():
    result = div(10, 10)
    assert result == 1

if __name__ == "__main__":
    main()