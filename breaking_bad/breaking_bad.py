import json
from collections import deque
from dataclasses import dataclass
from random import randrange, choice


@dataclass(frozen=True)
class TreeNode:
    root: str
    children: tuple

    def __str__(self):
        def h(tree):
            yield tree.root
            if not tree.children: return
            for i, child in enumerate(tree.children, start=1):
                last = i == len(tree.children)
                child_lines = h(child)
                yield ('└── ' if last else '├── ') + next(child_lines)
                for line in child_lines:
                    yield ('    ' if last else '│   ') + line

        return '\n'.join(h(self))


def json_tree(root, children):
    yield ('' if isinstance(root, str) else ' ') + json.dumps(root)
    if children is None: return
    if isinstance(children, dict):
        for i, (k, v) in enumerate(children.items()):
            last = i == len(children) - 1
            yield from prepend_lines(json_tree(k, v), last)
    elif isinstance(children, list):
        for i, v in enumerate(children):
            last = i == len(children) - 1
            yield from prepend_lines(json_tree(i, v), last)
    else:
        yield ' └──' + ('' if isinstance(children, str) else ' ') + json.dumps(children)


def prepend_lines(line_iterator, last):
    yield (' └──' if last else ' ├──') + next(line_iterator)
    for line in line_iterator:
        yield ('    ' if last else ' │  ') + line


def make_random_tree(height):
    with open('words.txt', 'r') as f:
        word_list = [word.strip() for word in f]
    if height <= 1: return TreeNode(choice(word_list), ())
    return TreeNode(choice(word_list),
                    tuple(make_random_tree(height - 1) for _ in range(randrange(1, 4))))


def breadth_first_search(tree, matcher):
    q = deque()
    q.append(tree)
    while q:
        node = q.popleft()
        if matcher(node.root):
            return node.root
        q.extend(node.children)


def breadth_first_walk(tree):
    q = deque()
    q.append(tree)
    while q:
        node = q.popleft()
        yield node.root
        q.extend(node.children)


def process_data(_chunk):
    pass


if __name__ == '__main__':
    abc_ = {
        'a_lo....ooong_key': {
            '0': True},
        'bb': [
            101,
            "true",
            False],
        'ccc': 1.2,
        'dddd': 10,
        'eeeee': 'ABC'
    }
    print('\n'.join(json_tree('*', abc_)))
    print(json.dumps(abc_, indent=2))
