from itertools import groupby


def gen_prime_factors(n):
    """Generate all the prime factors of n in ascending order"""
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            yield factor
            n //= factor
        else:
            factor = factor + (1 if factor == 2 else 2)
    if n > 1:
        yield n


def prime_factors(n):
    """Returns a list of pairs in ascending order where the first
    element of each pair is a prime, and the second element is the
    number of times the prime divides n. For example:
    prime_factors(360) returns [(2, 3), (3, 2), (5, 1)]"""

    return [(p, sum(1 for _ in g)) for p, g in groupby(gen_prime_factors(n))]


def totient(n):
    """Euler's totient function, a.k.a. Euler's phi funtion.
    Returns the number of integers between 1 and n that are coprime
    with n. For example: totient(60) = 16. The 16 numbers that coprime
    with 60 are: 1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49,
    53, 59"""

    for p, _ in groupby(gen_prime_factors(n)):
        n -= n // p
    return n


def is_prime(n):
    """:returns True if n is a prime number, False otherwise."""
    return 1 < n == next(gen_prime_factors(n))


def smallest_prime_factor(n):
    """Returns the smallest prime factor of n
    n: An int >= 2
    Raises a StopIteration if n < 2
    """
    return next(gen_prime_factors(n))


def largest_prime_factor(n):
    """Returns the largest prime factor of n
    n: An int >= 2
    Raises a ValueError if n < 2
    """
    return max(gen_prime_factors(n))
