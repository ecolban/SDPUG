from pathlib import Path

import pytest
import sys

SRC_DIR = Path(__file__).parent.parent / 'src'
sys.path.append(str(SRC_DIR))

from sales_report import *

records = [
    Record('0001', '001', '12'),
    Record('0012', '001', '1000'),
    Record('0012', '001', '32'),
    Record('0009', '007', '207'),
    Record('0112', '007', '12119'),
    Record('1009', '007', '200'),
]


class TestSalesReport:

    def test_process_product(self):
        prod = process_product('0001', iter(records[:1]))
        assert next(prod) == '    Product: 0001 Value:     12'
        with pytest.raises(StopIteration) as e_info:
            next(prod)
        assert e_info.value.value == 12

        prod = process_product('0012', records[1:3])
        assert next(prod) == '    Product: 0012 Value:   1032'
        with pytest.raises(StopIteration) as e_info:
            next(prod)
        assert e_info.value.value == 1032

    def test_process_product_group(self):
        prod_group = process_product_group('001', iter(records[:3]))
        assert next(prod_group) == 'Group: 001'
        assert next(prod_group) == '    Product: 0001 Value:     12'
        assert next(prod_group) == '    Product: 0012 Value:   1032'
        assert next(prod_group) == '    Group total:                  1044'
        assert next(prod_group) == ''
        with pytest.raises(StopIteration) as e_info:
            next(prod_group)
        assert e_info.value.value == 1044

        prod_group = process_product_group('007', iter(records[3:]))
        assert next(prod_group) == 'Group: 007'
        assert next(prod_group) == '    Product: 0009 Value:    207'
        assert next(prod_group) == '    Product: 0112 Value:  12119'
        assert next(prod_group) == '    Product: 1009 Value:    200'
        assert next(prod_group) == '    Group total:                 12526'
        assert next(prod_group) == ''
        with pytest.raises(StopIteration) as e_info:
            next(prod_group)
        assert e_info.value.value == 12526

    def test_generate_report(self):
        report_lines = process_all(records)
        assert '\n'.join(report_lines) == """\
Group: 001
    Product: 0001 Value:     12
    Product: 0012 Value:   1032
    Group total:                  1044

Group: 007
    Product: 0009 Value:    207
    Product: 0112 Value:  12119
    Product: 1009 Value:    200
    Group total:                 12526

Total:                           13570"""
