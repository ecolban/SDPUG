from operator import itemgetter
from random import randrange, sample, choice


def generate_data(num_records):
    product_groups = sample(range(1, 1000), 5)
    products = sample(range(1, 10000), 10)
    d = {prod: choice(product_groups) for prod in products}
    res = [generate_row(products, d) for _ in range(num_records)]
    res.sort(key=itemgetter(1, 0))
    return res


def generate_row(products, d):
    product = choice(products)
    return f'{product:04d},{d[product]:03d},{randrange(1, 2000)}'


if __name__ == '__main__':
    with open('../res/sales_records.csv', mode='w') as f:
        for r in generate_data(20):
            print(r, file=f)