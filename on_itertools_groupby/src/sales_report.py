from collections import namedtuple
from itertools import groupby

Record = namedtuple('Record', 'product product_group value')


def process_product(prod_id, prod_records):
    prod_total = sum(int(record.value) for record in prod_records)
    yield '    Product: %s Value: %6d' % (prod_id, prod_total)
    return prod_total


def process_product_group(group_id, group_records):
    group_total = 0
    yield 'Group: %s' % group_id
    for prod_id, prod_records in groupby(group_records, key=lambda record: record.product):
        group_total += yield from process_product(prod_id, prod_records)
    yield '    Group total:                %6d' % group_total
    yield ''
    return group_total


def generate_report(all_records):
    total = 0
    for prod_group_id, prod_group_records in groupby(all_records, key=lambda record: record.product_group):
        total += yield from process_product_group(prod_group_id, prod_group_records)
    yield 'Total:                          %6d' % total
