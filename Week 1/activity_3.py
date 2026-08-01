def fibonacci_series(N):
    """
    Generate Fibonacci series up to N.
    """
    series = []
    a, b = 0, 1

    while a <= N:
        series.append(a)
        a, b = b, a + b

    return series


def factorial(N):
    """
    Calculate factorial of N.
    """
    result = 1

    for i in range(1, N + 1):
        result *= i

    return result


def main():
    # Ask user for input
    N = int(input("Enter a number (N): "))

    # Get and print Fibonacci series
    fib = fibonacci_series(N)
    print("Fibonacci series up to", N, ":")
    print(fib)

    # Calculate and print factorial
    fact = factorial(N)
    print("Factorial of", N, "is:")
    print(fact)


# Run the program
if __name__ == "__main__":
    main()