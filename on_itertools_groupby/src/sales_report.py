import csv
from collections import namedtuple
from itertools import groupby
from operator import attrgetter
from pathlib import Path

RES = Path(__file__).parent.parent / 'res'
Record = namedtuple('Record', 'product product_group value')


def process_product(prod_id, prod_records):
    prod_total = sum(int(record.value) for record in prod_records)
    yield f'    Product: {prod_id} Value: {prod_total:6d}'
    return prod_total


def process_product_group(group_id, group_records):
    group_total = 0
    yield f'Group: {group_id}'
    for prod_id, prod_records in groupby(group_records, key=attrgetter('product')):
        group_total += yield from process_product(prod_id, prod_records)
    yield f'    Group total:                {group_total:6d}'
    yield ''
    return group_total


def process_all(all_records):
    total = 0
    for prod_group_id, prod_group_records in groupby(all_records, key=attrgetter('product_group')):
        total += yield from process_product_group(prod_group_id, prod_group_records)
    yield f'Total:                          {total:6d}'


def generate_report(file_path):
    with open(file_path, mode='r') as f:
        reader = csv.reader(f)
        records = (Record(*row) for row in reader)
        yield from process_all(records)


if __name__ == '__main__':
    for line in generate_report(RES / 'sales_records.csv'):
        print(line)
