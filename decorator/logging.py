
import time
from math import sqrt


def is_prime(number: int):
    if number == 1:
        return False
    elif number == 2:
        return True
    else:
        for i in range(2, int(sqrt(number)) + 1):
            if number % i == 0:
                return False
        return True


def benchmark(func):
    def wrapper(number):
        start = time.time()
        value = func(number)
        end = time.time()
        print(f"there is approximatively {value} prime number between 0 and {number}.")
        print(f"this function took {end-start} to execute.")
        return value
    return wrapper


@benchmark
def how_many_primes(number: int):
    counter = 0
    for i in range(1, number):
        if is_prime(i):
            counter += 1
    return counter

@benchmark
def how_many_big_number(number):
    time.sleep(5)
    return 1000

how_many_primes(1000000)
#how_many_big_number(10000)