from collections import defaultdict, Counter
from random import choice


def mystery(n):
    a, b, c, d = n, 1, 0, 0
    while b <= n: b <<= 2
    while b > 1:
        b >>= 2
        c <<= 1
        e = d + b
        d >>= 1
        if e <= a:
            a -= e
            c += 1
            d += b
    return c, a


def int_sqrt(n):
    root, m, k, h = 0, n, 1, 0
    while k <= n:
        k <<= 2

    def invariant():
        print(f'root = {root:3d}, m = {m:3d}, k = {k:4d}, h = {h:3d}')
        return k * root ** 2 + m == n and 0 <= m < k * (2 * root + 1) and k * root == h

    while k > 1:
        assert invariant()
        k >>= 2
        root <<= 1
        d = h + k  # d == k * (2 * root + 1)
        h >>= 1
        if d <= m:
            m -= d
            root += 1
            h += k
    assert invariant() and k == 1
    return root, m


######################################################################
# How we normally compute the integer square root for large integers #
######################################################################

def int_sqrt_newton(n, start=None):
    guess = start or 1 << n.bit_length() // 2
    y = n // guess
    while abs(guess - y) > 1:
        guess = (guess + y) >> 1
        y = n // guess
    return min(guess, y)


def longest_palindrome(s):
    """
    Find the longest palindromic substring in s. If there are multiple such substrings,
    the first occurrence is returned.
    """
    # s_sep = '|' + '|'.join(s) + '|'
    n = 2 * len(s) + 1
    r = [0] * n
    start = max_ctr = ctr = end = 0
    while end < n - 1:
        # Loop invariant:
        # ctr is the index some character in s_sep
        # start is the index of first character of the longest palindromic
        # substring of s_sep centered at ctr
        # end is the index of last character of the longest palindromic
        # substring of s_sep centered at ctr
        # r[k] == radius of the longest palindromic substring of s_sep
        # centered at k, for 0 <= k <= ctr
        i, j = ctr - 1, ctr + 1
        while j <= end and r[i] != end - j:
            r[j] = min(r[i], end - j)
            i, j = i - 1, j + 1
        ctr, end = j, max(end, j)
        start = ctr - (end - ctr)
        while start & 1 or 0 < start and end < n - 1 and s[(start >> 1) - 1] == s[end >> 1]:
            start, end = start - 1, end + 1
        r[ctr] = end - ctr
        if r[ctr] > r[max_ctr]: max_ctr = ctr
    return s[max_ctr - r[max_ctr] >> 1: max_ctr + r[max_ctr] >> 1]


def longest_palindrome_2(s):
    """
    Find the longest palindromic substring in s. If there are multiple such substrings,
    the first occurrence is returned.
    """
    # s_sep = '|' + '|'.join(s) + '|'
    n = 2 * len(s) + 1
    r = [0] * n
    start = max_ctr = ctr = end = 0
    while end < n - 1:
        # Loop invariant:
        # ctr is the index some character in s_sep
        # start is the index of first character of the longest palindromic
        # substring of s_sep centered at ctr
        # end is the index of last character of the longest palindromic
        # substring of s_sep centered at ctr
        # r[k] == radius of the longest palindromic substring of s_sep
        # centered at k, for 0 <= k <= ctr
        i, j = ctr - 1, ctr + 1
        while j <= end:
            if r[i] < end - j:
                r[j] = r[i]
            elif r[i] > end - j:
                r[j] = end - j
            else:
                break
            i, j = i - 1, j + 1
        else:
            end = j
        ctr = j
        start = ctr - (end - ctr)
        while start & 1 or 0 < start and end < n - 1 and s[(start >> 1) - 1] == s[end >> 1]:
            start, end = start - 1, end + 1
        r[ctr] = end - ctr
        if r[ctr] > r[max_ctr]: max_ctr = ctr
    return s[max_ctr - r[max_ctr] >> 1: max_ctr + r[max_ctr] >> 1]


def longest_palindrome_everted(s):
    n = 2 * len(s) + 1
    r = [0] * n
    start = ctr = max_j = 0
    for end in range(n):
        while start & 1 == 0 and ctr <= end and (start == 0 or end == n - 1 or s[start - 1 >> 1] != s[end + 1 >> 1]):
            r[ctr] = end - ctr
            if r[ctr] > r[max_j]: max_j = ctr
            i, j = ctr - 1, ctr + 1
            while j <= end and r[i] != end - j:
                r[j] = min(r[i], end - j)
                i, j = i - 1, j + 1
            ctr = j
            start = ctr - (end - ctr)
        start -= 1
        # start & 1 == 1 or ctr > end or (start > 0 and end < n - 1 and s[start - 1 >> 1] == s[end + 2 >> 1])
    return s[max_j - r[max_j] >> 1:max_j + r[max_j] >> 1]


if __name__ == "__main__":
    int_sqrt(5000)
    # print([(i, *mystery(i)) for i in range(5, 101, 5)])
    # d = defaultdict(int)
    # for _ in range(100):
    #     s = ''.join(choice('ucga') for _ in range(100000))
    #     p1 = longest_palindrome(s)
    #     p2 = longest_palindrome_2(s)
    #     assert p1 == p2
    #     d[len(p1)] += 1
    # print(sorted(d.items()))

# [(18, 8), (19, 125), (20, 164), (21, 336), (22, 111), (23, 156), (24, 39), (25, 33),
#  (26, 8), (27, 12), (28, 6), (29, 2)]
