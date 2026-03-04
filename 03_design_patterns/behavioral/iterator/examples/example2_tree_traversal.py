"""
Iterator Pattern — Example 2: Binary Tree Traversal

Demonstrates how to apply the Iterator pattern to a non-linear data
structure (a binary tree).  Three iterator classes use an **explicit stack**
(no recursion) so that traversal state is fully encapsulated and can be
paused / resumed.

Traversal orders:
  - InOrderIterator   : left → root → right  (yields sorted values for a BST)
  - PreOrderIterator  : root → left → right  (useful for copying a tree)
  - PostOrderIterator : left → right → root  (useful for deleting a tree)

Run:
    python3 examples/example2_tree_traversal.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Tree node
# ---------------------------------------------------------------------------

@dataclass
class TreeNode:
    value: int
    left: Optional[TreeNode] = field(default=None, repr=False)
    right: Optional[TreeNode] = field(default=None, repr=False)

    def __repr__(self) -> str:
        return f"TreeNode({self.value})"


# ---------------------------------------------------------------------------
# In-order iterator  (left, root, right)
# ---------------------------------------------------------------------------

class InOrderIterator:
    """
    Iterates a binary tree in-order using an explicit stack.
    Pushing left children eagerly mirrors the recursive call stack.
    """

    def __init__(self, root: Optional[TreeNode]) -> None:
        self._stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: Optional[TreeNode]) -> None:
        while node is not None:
            self._stack.append(node)
            node = node.left

    def __iter__(self) -> InOrderIterator:
        return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        self._push_left(node.right)
        return node.value


# ---------------------------------------------------------------------------
# Pre-order iterator  (root, left, right)
# ---------------------------------------------------------------------------

class PreOrderIterator:
    """
    Iterates a binary tree in pre-order using an explicit stack.
    Push right child first so left is processed first (LIFO).
    """

    def __init__(self, root: Optional[TreeNode]) -> None:
        self._stack: list[TreeNode] = []
        if root is not None:
            self._stack.append(root)

    def __iter__(self) -> PreOrderIterator:
        return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        # Push right first — left will be processed next (stack is LIFO)
        if node.right is not None:
            self._stack.append(node.right)
        if node.left is not None:
            self._stack.append(node.left)
        return node.value


# ---------------------------------------------------------------------------
# Post-order iterator  (left, right, root)
# ---------------------------------------------------------------------------

class PostOrderIterator:
    """
    Iterates a binary tree in post-order using two stacks.
    Stack 1 is the work stack; stack 2 collects the reverse post-order,
    which is then yielded in reverse to produce the correct order.

    Alternative: use a single stack with a 'last visited' pointer, but
    two stacks are easier to understand.
    """

    def __init__(self, root: Optional[TreeNode]) -> None:
        self._output: list[int] = []
        if root is not None:
            stack1: list[TreeNode] = [root]
            stack2: list[TreeNode] = []
            while stack1:
                node = stack1.pop()
                stack2.append(node)
                if node.left is not None:
                    stack1.append(node.left)
                if node.right is not None:
                    stack1.append(node.right)
            # stack2 holds nodes in reverse post-order; reverse it
            self._output = [n.value for n in reversed(stack2)]
        self._index = 0

    def __iter__(self) -> PostOrderIterator:
        return self

    def __next__(self) -> int:
        if self._index >= len(self._output):
            raise StopIteration
        value = self._output[self._index]
        self._index += 1
        return value


# ---------------------------------------------------------------------------
# BinaryTree — the iterable collection
# ---------------------------------------------------------------------------

class BinaryTree:
    """
    A binary tree that supports three traversal modes via iterator objects.
    The tree itself is the *iterable*; each traversal returns a distinct
    *iterator*, so multiple traversals can run simultaneously.
    """

    def __init__(self, root: Optional[TreeNode] = None) -> None:
        self.root = root

    def __iter__(self) -> InOrderIterator:
        """Default iteration is in-order."""
        return InOrderIterator(self.root)

    def inorder(self) -> InOrderIterator:
        return InOrderIterator(self.root)

    def preorder(self) -> PreOrderIterator:
        return PreOrderIterator(self.root)

    def postorder(self) -> PostOrderIterator:
        return PostOrderIterator(self.root)


# ---------------------------------------------------------------------------
# Helper: build a sample BST
# ---------------------------------------------------------------------------

def build_sample_tree() -> TreeNode:
    """
    Builds:
              4
            /   \
           2     6
          / \   / \
         1   3 5   7
    In-order  : 1 2 3 4 5 6 7
    Pre-order : 4 2 1 3 6 5 7
    Post-order: 1 3 2 5 7 6 4
    """
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)
    return root


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    root = build_sample_tree()
    tree = BinaryTree(root)

    print("Tree structure:")
    print("        4")
    print("      /   \\")
    print("     2     6")
    print("    / \\   / \\")
    print("   1   3 5   7")
    print()

    print("In-order   (left→root→right):", list(tree.inorder()))
    print("Pre-order  (root→left→right):", list(tree.preorder()))
    print("Post-order (left→right→root):", list(tree.postorder()))
    print()

    # Default for loop uses in-order
    print("Default 'for' loop (in-order):", end=" ")
    for value in tree:
        print(value, end=" ")
    print()
    print()

    # Multiple simultaneous iterators share no state
    print("=== Two simultaneous in-order iterators ===")
    it1 = tree.inorder()
    it2 = tree.inorder()
    print(f"it1 → {next(it1)}, it2 → {next(it2)}, it1 → {next(it1)}, it2 → {next(it2)}")
    print()

    # Edge case: empty tree
    empty_tree = BinaryTree()
    print("Empty tree in-order   :", list(empty_tree.inorder()))
    print("Empty tree pre-order  :", list(empty_tree.preorder()))
    print("Empty tree post-order :", list(empty_tree.postorder()))
    print()

    # Single-node tree
    single = BinaryTree(TreeNode(42))
    print("Single-node in-order  :", list(single.inorder()))
    print("Single-node pre-order :", list(single.preorder()))
    print("Single-node post-order:", list(single.postorder()))


if __name__ == "__main__":
    main()
