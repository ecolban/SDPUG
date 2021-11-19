from random import randrange


def g(i):
    n = randrange(1, 101)
    yield f"{i:<2d}: {n}"
    return n


def f():
    c = 0
    yield "Random Numbers"
    yield "=============="
    for i in range(1, 21):
        c += yield from g(i)
    yield f'Total = {c}'


if __name__ == '__main__':
    print(*f(), sep='\n')
