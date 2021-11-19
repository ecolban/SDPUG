from pathlib import Path
import sys

import pytest

SRC_DIR = Path(__file__).parent.parent / 'src'
sys.path.append(str(SRC_DIR))

from prime_factorization import *


class TestPrimeFactorization:

    def test_is_prime(self):
        assert is_prime(101)
        assert is_prime(103)
        assert [i for i in range(101, 165, 2) if is_prime(i)] == [
            101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
        ]

    def test_prime_factors(self):
        assert prime_factors(10) == [(2, 1), (5, 1)]
        assert prime_factors(12) == [(2, 2), (3, 1)]
        assert prime_factors(16) == [(2, 4)]
        assert prime_factors(98) == [(2, 1), (7, 2)]
        assert prime_factors(2 ** 6 * 3 ** 4 * 5 ** 2 * 107) == [(2, 6), (3, 4), (5, 2), (107, 1)]

    def test_totient(self):
        assert totient(36) == 12
        assert totient(100) == 40
        assert totient(11 * 101) == 1000
        n = 2 ** 6 * 3 ** 4 * 5 ** 2 * 107
        assert totient(n) == n * (2 - 1) // 2 * (3 - 1) // 3 * (5 - 1) // 5 * (107 - 1) // 107

    def test_largest_prime_factor(self):
        assert largest_prime_factor(101 * 17 * 5) == 101
        with pytest.raises(ValueError):
            largest_prime_factor(1)

    def test_smallest_prime_factor(self):
        assert smallest_prime_factor(101 * 17 * 5) == 5
        with pytest.raises(StopIteration):
            smallest_prime_factor(1)
