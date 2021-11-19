from random import randrange


def f():
    print("Random Numbers")
    print("==============")
    total = 0
    for i in range(1, 21):
        n = randrange(1, 101)
        print(f"{i :<2d}: {n}")
        total += n
    print(f'Total = {total}')


if __name__ == '__main__':
    f()
