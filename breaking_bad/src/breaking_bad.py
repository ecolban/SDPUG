from collections import deque
from dataclasses import dataclass
from pathlib import Path

with open(Path(__file__).parent.parent / 'assets/words.txt', mode='r') as f:
    WORDS = [word.strip() for word in f]


@dataclass(frozen=True)
class TreeNode:
    root: str
    children: tuple

    def __str__(self):
        def h(tree):
            yield tree.root
            for i, child in enumerate(tree.children, start=1):
                last = i == len(tree.children)
                child_lines = h(child)
                yield ('└── ' if last else '├── ') + next(child_lines)
                for line in child_lines:
                    yield ('    ' if last else '│   ') + line

        return '\n'.join(h(self))

    def breadth_first_iterator(self):
        q = deque()
        q.append(self)
        while q:
            node = q.popleft()
            yield node.root
            q.extend(node.children)

    def depth_first_iterator(self):
        yield self.root
        for child in self.children:
            yield from child.depth_first_iterator()

    __iter__ = depth_first_iterator

    def __len__(self):
        return sum(1 for _ in self)


def breadth_first_search(tree, matcher):
    q = deque()
    q.append(tree)
    while q:
        node = q.popleft()
        if matcher(node.root):
            return node.root
        q.extend(node.children)
