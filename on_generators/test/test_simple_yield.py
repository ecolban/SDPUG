import re
from pathlib import Path
import sys

import pytest

SRC_DIR = Path(__file__).parent.parent / 'src'
sys.path.append(str(SRC_DIR))

from simple_yield import *


class TestSimpleYield:

    @pytest.mark.parametrize('i', [1, 3, 63])
    def test_rng(self, i):
        g = rng(i)
        m = re.match(r'(\d{1,2})\s*:\s+(\d{1,3})$', next(g))
        assert m is not None
        assert int(m.group(1)) == i
        n = int(m.group(2))
        assert 1 <= n <= 100
        with pytest.raises(StopIteration) as e_info:
            next(g)
            assert e_info.value.value == n

    def test_f(self):
        gen = f()
        assert next(gen) == "Random Numbers"
        assert next(gen) == "=============="
        for _ in range(20):
            assert re.match(r'\d+\s*:\s+\d+$', next(gen))
        assert re.match(r'Total = \d+$', next(gen))
        with pytest.raises(StopIteration):
            next(gen)
