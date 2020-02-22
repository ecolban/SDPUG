def truncate_left(s):
    return reversed(truncate_right(reversed(s)))


def truncate_right(s):
    return ''.join(c for c, _ in zip(s, '00000000000000000000000000000000'))


def last(s):
    return s[-1]


class StrNum(object):
    """
    Created on Jan 31, 2016

    @author: Erik Colban
    """

    # Defining 32-bit numbers in little-endian
    digit_to_binary = {
        '0': '00000000000000000000000000000000',
        '1': '10000000000000000000000000000000',
        '2': '01000000000000000000000000000000',
        '3': '11000000000000000000000000000000',
        '4': '00100000000000000000000000000000',
        '5': '10100000000000000000000000000000',
        '6': '01100000000000000000000000000000',
        '7': '11100000000000000000000000000000',
        '8': '00010000000000000000000000000000',
        '9': '10010000000000000000000000000000'}

    binary_to_digit = {b: d for d, b in digit_to_binary.items()}

    def __init__(self, s, binary=False):
        # should have validated s, but trusting the client instead
        if binary:
            self._value = s
        elif s in StrNum.digit_to_binary:
            self._value = StrNum.digit_to_binary[s]
        else:
            n = zero
            sgn = one
            for d in s:
                if d == '-':
                    sgn = -sgn
                else:
                    n *= ten
                    n += StrNum(d)
            self._value = (sgn * n)._value

    def __add__(self, other):

        def bit_gen():
            carry = '0'
            for x in zip(self._value, other._value):
                if x == ('0', '0'):
                    yield carry
                    carry = '0'
                elif x == ('1', '1'):
                    yield carry
                    carry = '1'
                else:
                    yield '1' if carry == '0' else '0'
        return StrNum(''.join(bit_gen()), binary=True)

    def __lshift__(self, other):
        b = one
        s = self._value
        while b <= other:
            s = truncate_right('0' + s)
            b = b + one
        return StrNum(s, binary=True)

    def __rshift__(self, other):
        b = one
        s = self._value
        c = '1' if self.__is_negative() else '0'
        while b <= other:
            s = truncate_left(s + c)
            b += one
        return StrNum(s, binary=True)

    def __neg__(self):
        one_complement = ''.join('1' if c == '0' else '0' for c in self._value)
        return StrNum(one_complement, binary=True) + one

    def __sub__(self, other):
        return self + -other

    def __is_negative(self):
        return last(self._value) == '1'

    def __abs__(self):
        return -self if self.__is_negative() else self

    def __eq__(self, other):
        return self._value == other._value

    def __ne__(self, other):
        return self._value != other._value

    def __gt__(self, other):
        return (other - self).__is_negative()

    def __ge__(self, other):
        return self == other or self > other

    def __lt__(self, other):
        return (self - other).__is_negative()

    def __le__(self, other):
        return self == other or self < other

    def __mul__(self, other, mod=None):
        if self.__is_negative():
            return -(-self).__mul__(other, mod)
        result = zero
        for b in reversed(self._value):
            result <<= one
            if b == '1':
                result += other
            while mod and result >= mod:
                result -= mod
        return result

    def __divmod__(self, other):
        if self.__is_negative() and other.__is_negative():
            q, r = (-self).__divmod__(-other)
            return q, -r
        elif self.__is_negative():
            q, r = (-self).__divmod__(other)
            q, r = -q, -r
            if r != zero:
                r += other
                q -= one
            return q, r
        elif other.__is_negative():
            q, r = self.__divmod__(-other)
            q = -q
            if r != zero:
                r += other
                q -= one
            return q, r
        else:  # neither self nor other is negative
            q, r = zero, zero
            for b in reversed(self._value):
                q, r = q << one, r << one
                if b == '1':
                    r += one
                if r >= other:
                    r -= other
                    q += one
            return q, r

    def __floordiv__(self, other):
        q, _ = self.__divmod__(other)
        return q

    def __mod__(self, other):
        _, r = self.__divmod__(other)
        return r

    def __pow__(self, n, mod=None):
        if mod and self >= mod:
            return pow((self % mod), n, mod)
        p = one
        for b in reversed(n._value):
            p = p.__mul__(p, mod)
            if b == '1':
                p = p.__mul__(self, mod)
        return p

    def __repr__(self):
        return "StrNum('%s')" % str(self)

    def __str__(self):
        if self == zero: return '0'
        if self < zero: return '-' + str(-self)
        result = ""
        s = self
        while s > zero:
            s, r = s.__divmod__(ten)
            result = StrNum.binary_to_digit[r._value] + result
        return result

    def __hash__(self):
        return hash(self._value)


zero = StrNum('0')
one  = StrNum('1')
ten  = StrNum('01010000000000000000000000000000', binary=True)
