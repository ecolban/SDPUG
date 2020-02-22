from functools import wraps
from urllib.parse import quote
import pyperclip


def render_svg_in_markdown(svg_file):
    """After calling this function, paste the contents of the clipboard into markdown,
     which will be rendered as the image of svg_file."""
    with open(svg_file, mode='r') as f:
        s = ''.join(line.strip() for line in f)
    pyperclip.copy(f'![svg image](data:image/svg+xml,{quote(s)})')


def log(msg):
    def h(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            args_str = [repr(v) for v in args]
            args_str += [f'{k}={repr(v)}' for k, v in kwargs.items()]
            res = None
            try:
                res = f(*args, **kwargs)
                return res
            finally:
                print(f'[{msg}] {f.__name__}({", ".join(args_str)}) => {res}')

        return wrapper

    return h
