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
    tree = make_random_tree(4)
    print(tree)
    first_vowel = next((x for x in breadth_first_walk(tree) if x[0] in 'aeiou'), None)
    contains_a = any('a' in x for x in breadth_first_walk(tree))
    num_nodes = sum(1 for _ in breadth_first_walk(tree))
    print(first_vowel, contains_a, num_nodes)
