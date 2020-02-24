from random import randrange
from unittest import TestCase
from time import perf_counter as now

from strmath.src.strmath import StrNum


class TestStrNum(TestCase):
    def test_init(self):
        eleven = StrNum('11')
        self.assertIsNotNone(eleven, "eleven should be a Number instance")
        eleven_1 = StrNum('11010000000000000000000000000000', binary=True)
        self.assertIsNotNone(eleven_1, "eleven_1 should be a Number instance")
        self.assertEqual(eleven, eleven_1)

    def test_value(self):
        eleven = StrNum('11')
        self.assertEqual('11010000000000000000000000000000', eleven._value)

    def test_neg(self):
        self.assertEqual(StrNum('-3'), -StrNum('3'))

    def test_add(self):
        eleven = StrNum('11')
        twelve = StrNum('12')
        self.assertEqual(eleven + twelve, StrNum('23'))

    def test_mul(self):
        start = now()
        bound = int(1e9)
        for _ in range(10):
            op1 = randrange(-bound, bound + 1)
            op2 = randrange(-bound, bound + 1)
            mod = randrange(-bound, bound)
            if mod == 0: mod = bound
            expected = StrNum(str(op1 * op2 % mod))
            actual = StrNum(str(op1)).__mul__(StrNum(str(op2)), StrNum(str(mod)))
            self.assertEqual(expected, actual, f"Failed for op1 = {op1}, op2 = {op2}, mod = {mod}")
        bound = int(1e4)
        for _ in range(10):
            op1 = randrange(-bound, bound + 1)
            op2 = randrange(-bound, bound + 1)
            expected = StrNum(str(op1 * op2))
            actual = StrNum(str(op1)).__mul__(StrNum(str(op2)))
            self.assertEqual(expected, actual, f"Failed for op1 = {op1}, op2 = {op2}")
        print(f'test_mul: {now() - start}')

    def test_divmod(self):
        start = now()
        bound = int(1e9)
        for _ in range(10):
            dividend = randrange(-bound, bound + 1)
            divisor = randrange(-bound, bound)
            if divisor == 0: divisor = bound
            q, r = divmod(dividend, divisor)
            expected = (StrNum(str(q)), StrNum(str(r)))
            actual = divmod(StrNum(str(dividend)), StrNum(str(divisor)))
            self.assertEqual(expected, actual, f"Failed for dividend = {dividend}, divisor = {divisor}")
        print(f'test_divmod: {now() - start}')

    def test_div(self):
        start = now()
        bound = int(1e9)
        for _ in range(10):
            dividend = randrange(-bound, bound + 1)
            divisor = randrange(-bound, bound)
            if divisor == 0: divisor = bound
            expected = StrNum(str(dividend // divisor))
            actual = StrNum(str(dividend)) // StrNum(str(divisor))
            self.assertEqual(expected, actual, f"Failed for dividend = {dividend}, divisor = {divisor}")
        print(f'test_div: {now() - start}')

    def test_modulo(self):
        start = now()
        bound = int(1e9)
        for _ in range(10):
            dividend = randrange(-bound, bound + 1)
            divisor = randrange(-bound, bound)
            if divisor == 0: divisor = bound
            expected = StrNum(str(dividend % divisor))
            actual = StrNum(str(dividend)) % StrNum(str(divisor))
            self.assertEqual(expected, actual, f"Failed for dividend = {dividend}, divisor = {divisor}")
        print(f'test_modulo: {now() - start}')

    def test_pow_with_mod(self):
        start = now()
        bound = int(1e9)
        for _ in range(10):
            base = randrange(-bound, bound + 1)
            exp = randrange(1, bound + 1)
            mod = randrange(-bound, bound)
            if mod == 0: mod = bound
            expected = StrNum(str(pow(base, exp, mod)))
            actual = pow(StrNum(str(base)), StrNum(str(exp)), StrNum(str(mod)))
            self.assertEqual(expected, actual, f"Failed for base = {base}, exp = {exp}, mod = {mod}")
        print(f'test_pow_with_mod: {now() - start}')

    def test_pow_without_mod(self):
        self.assertEqual(StrNum('3') ** StrNum('4'), StrNum('81'))
        self.assertEqual(StrNum('5') ** StrNum('6'), StrNum('15625'))
        self.assertEqual(StrNum('100') ** StrNum('2'), StrNum('10000'))

    def test_repr(self):
        bound = int(1e9)
        for _ in range(10):
            n = randrange(-bound, bound + 1)
            expected = f"StrNum('{str(n)}')"
            actual = repr(StrNum(str(n)))
            self.assertEqual(expected, actual)

    def test_str(self):
        bound = int(1e9)
        for _ in range(10):
            n = randrange(-bound, bound + 1)
            expected = str(n)
            actual = str(StrNum(str(n)))
            self.assertEqual(expected, actual)
