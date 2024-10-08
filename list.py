def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            return False
    return True

# Function to find all prime numbers up to n
def find_primes_up_to_n(n):
    primes = []
    for i in range(2, n + 1):
        if is_prime(i):
            primes.append(i)
    return primes

# Read input from user
n = int(input("Enter a number: "))

# Get prime numbers up to n
prime_numbers = find_primes_up_to_n(n)

# Print the result
if prime_numbers:
    print(f"Prime numbers up to {n}: {prime_numbers}")
else:
    print(f"There are no prime numbers up to {n}.")