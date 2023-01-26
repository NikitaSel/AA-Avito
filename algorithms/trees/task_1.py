from typing import Tuple
from collections import deque


class TreeNode:

    def __init__(self, parent, key: int):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

    def insert(self, node) -> None:
        if node is None:
            return
        if node.key < self.key:
            if self.left is None:
                node.parent = self
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                node.parent = self
                self.right = node
            else:
                self.right.insert(node)

    def breadth_first(self) -> Tuple[list, list]:
        key_level = {}
        q = deque()
        q.append((self, 0))
        while q:
            node, level = q.popleft()
            key_level[node.key] = level
            if node.left:
                q.append((node.left, level + 1))
            if node.right:
                q.append((node.right, level + 1))

        return key_level.keys(), key_level.values()


def build_tree(keys: list) -> TreeNode:
    root = TreeNode(None, keys[0])
    if len(keys) != 1:
        for key in keys[1:]:
            root.insert(TreeNode(None, key))

    return root

def get_level_order_keys_and_levels(preorder_keys: list) -> Tuple[list, list]:
    root = build_tree(preorder_keys)
    if len(preorder_keys) != 1:
        return root.breadth_first()
    else:
        return [root.key], [0]
