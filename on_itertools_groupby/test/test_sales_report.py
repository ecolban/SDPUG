from unittest import TestCase

from on_itertools_groupby.src.sales_report import *

records = [Record(*line.split(',')) for line in ['0001,001,12',
                                                 '0012,001,1000',
                                                 '0012,001,32',
                                                 '0009,007,207',
                                                 '0112,007,12119',
                                                 '1009,007,200']]


class TestSalesReport(TestCase):

    def test_process_product(self):
        prod = process_product('0001', records[:1])
        self.assertEqual('    Product: 0001 Value:     12',           next(prod))
        with self.assertRaises(StopIteration) as context_manager:
            next(prod)
        self.assertEqual(12, context_manager.exception.value)

        prod = process_product('0012', records[1:3])
        self.assertEqual('    Product: 0012 Value:   1032',           next(prod))
        with self.assertRaises(StopIteration) as context_manager:
            next(prod)
        self.assertEqual(1032, context_manager.exception.value)

    def test_process_product_group(self):
        prod_group = process_product_group('001', records[:3])
        self.assertEqual('Group: 001',                                next(prod_group))
        self.assertEqual('    Product: 0001 Value:     12',           next(prod_group))
        self.assertEqual('    Product: 0012 Value:   1032',           next(prod_group))
        self.assertEqual('    Group total:                  1044',    next(prod_group))
        self.assertEqual('',                                          next(prod_group))
        with self.assertRaises(StopIteration) as context_manager:
            next(prod_group)
        self.assertEqual(1044, context_manager.exception.value)

        prod_group = process_product_group('007', records[3:])
        self.assertEqual('Group: 007', next(prod_group))
        self.assertEqual('    Product: 0009 Value:    207',           next(prod_group))
        self.assertEqual('    Product: 0112 Value:  12119',           next(prod_group))
        self.assertEqual('    Product: 1009 Value:    200',           next(prod_group))
        self.assertEqual('    Group total:                 12526',    next(prod_group))
        self.assertEqual('',                                          next(prod_group))
        with self.assertRaises(StopIteration) as context_manager:
            next(prod_group)
        self.assertEqual(12526, context_manager.exception.value)

    def test_generate_report(self):
        report = generate_report(records)
        self.assertEqual('Group: 001',                                next(report))
        self.assertEqual('    Product: 0001 Value:     12',           next(report))
        self.assertEqual('    Product: 0012 Value:   1032',           next(report))
        self.assertEqual('    Group total:                  1044',    next(report))
        self.assertEqual('',                                          next(report))
        self.assertEqual('Group: 007',                                next(report))
        self.assertEqual('    Product: 0009 Value:    207',           next(report))
        self.assertEqual('    Product: 0112 Value:  12119',           next(report))
        self.assertEqual('    Product: 1009 Value:    200',           next(report))
        self.assertEqual('    Group total:                 12526',    next(report))
        self.assertEqual('',                                          next(report))
        self.assertEqual('Total:                           13570',    next(report))
        self.assertRaises(StopIteration, next, report)
