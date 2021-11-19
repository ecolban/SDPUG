import re
from pathlib import Path
import sys

import pytest

SRC_DIR = Path(__file__).parent.parent / 'src'
sys.path.append(str(SRC_DIR))

from simple_yield import *


class TestSimpleYield:
    def test_g(self):
        gen = g(3)
        m = re.match(r'(\d{1,2})\s*:\s+(\d{1,3})$', next(gen))
        assert m is not None
        i = int(m.group(1))
        n = int(m.group(2))
        assert i == 3
        assert 1 <= n < 101
        with pytest.raises(StopIteration) as e_info:
            next(gen)
            assert e_info.value.value == n

    def test_f(self):
        gen = f()
        assert next(gen) == "Random Numbers"
        assert next(gen) == "=============="
        for _ in range(20):
            assert re.match(r'\d{1,2}\s*:\s+\d{1,3}$', next(gen))
        assert re.match(r'Total = \d+$', next(gen))
        with pytest.raises(StopIteration):
            next(gen)
