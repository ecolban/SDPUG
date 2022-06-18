import string
from pathlib import Path

BIBLE_PATH = Path(__file__).parent.parent / 'assets/bible.txt'
ALPHABET = string.ascii_uppercase


def clean_line(line):
    return ''.join(c for c in line.upper() if c in ALPHABET)


def get_bible_as_str():
    with open(BIBLE_PATH, mode='r') as f:
        s = ''.join(clean_line(line) for line in f)
    return s


if __name__ == '__main__':
    s = get_bible_as_str()
    print(s[:200])
    print(f'{len(s) = }')
