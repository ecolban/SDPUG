from random import randrange


def rng(i):
    n = randrange(1, 101)
    yield f"{i:<3d}: {n}"
    return n


def f():
    yield "Random Numbers"
    yield "=============="
    total = 0
    for i in range(1, 21):
        # g = rng(i)
        # keep_going = True
        # while keep_going:
        #     try:
        #         yield next(g)
        #     except StopIteration as e:
        #         keep_going = False
        #         total += e.value
        total += yield from rng(i)
    yield f'Total = {total}'


if __name__ == '__main__':
    # print(*f(), sep='\n')
    for s in f():
        print(s)
