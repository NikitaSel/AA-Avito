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

    def find(self, k):
        if self.key == k:
            return self
        elif k < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(k)
        else:
            if self.right is None:
                return None
            else:
                return self.right.find(k)

    def pre_order(self, pre_order_list: list = None) -> list:
        if pre_order_list is None:
            pre_order_list = list()

        if self:
            pre_order_list.append(self.key)
            if self.left:
                self.left.pre_order(pre_order_list)
            if self.right:
                self.right.pre_order(pre_order_list)

        if self.parent is None:
            return pre_order_list

    def left_rotate(self):
        if self is None or self.right is None:
            return self
        parent = self.parent
        right = self.right
        right_left = right.left

        if parent:
            if parent.left == self:
                parent.left = right
            else:
                parent.right = right
        right.parent = parent

        right.left = self
        self.parent = right

        self.right = right_left
        if right_left:
            right_left.parent = self

        return right


def build_tree(keys: list) -> TreeNode:
    root = TreeNode(None, keys[0])
    if len(keys) != 1:
        for key in keys[1:]:
            root.insert(TreeNode(None, key))

    return root

def find_and_left_rotate(preorder_keys: list, key: int) -> list:
    root = build_tree(preorder_keys)
    node = root.find(key)
    node = node.left_rotate()
    return root.pre_order() or node.pre_order()
