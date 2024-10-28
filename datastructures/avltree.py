from __future__ import annotations
from typing import Callable, Generic, List, Optional, Sequence, Tuple

from datastructures.iavltree import IAVLTree, K, V
from datastructures.avlnode import AVLNode
from collections import deque

class AVLTree(IAVLTree[K, V], Generic[K, V]):
    def __init__(self, starting_sequence: Optional[Sequence[Tuple[K, V]]]=None) -> None: 
        self._root: Optional[AVLNode] = None
        self._size: int = 0
        for key, value in starting_sequence or []: self.insert(key, value)

    def insert(self, key: K, value: V) -> None:
        def _insert(node: Optional[AVLNode], key: K, value: V) -> AVLNode:
            if not node: return AVLNode(key, value)
            elif key < node.key: node.left = _insert(node.left, key, value)
            else: node.right = _insert(node.right, key, value)

            node.height = 1 + max(AVLTree._node_height(node.left), AVLTree._node_height(node.right))
            return AVLTree._balance_tree(node)
    
        if self.search(key): raise KeyError(f"Key {key} already exists in the tree.")
        self._root = _insert(self._root, key, value)
        self._size += 1

    def search(self, key: K) -> Optional[V]:
        def _search(root: Optional[AVLNode], key: K) -> Optional[V]:
            if not root: return None
            
            if key == root.key: return root.value
            elif key < root.key: return _search(root.left, key)
            else: return _search(root.right, key)
            
        return _search(self._root, key)
        
    def delete(self, key: K) -> None:
        def _delete(root: Optional[AVLNode], key: K) -> Optional[AVLNode]:
            if not root: return root
            
            if key < root.key: root.left = _delete(root.left, key)
            elif key > root.key: root.right = _delete(root.right, key)
            else:
                if not root.left or not root.right: root = root.left or root.right
                else:
                    successor: AVLNode[K, V] = AVLTree._find_successor(root.right)
                    root.key = successor.key
                    root.value = successor.value
                    root.right = _delete(root.right, successor.key)
            if root: 
                root.height = 1 + max(AVLTree._node_height(root.left), AVLTree._node_height(root.right))        
                return AVLTree._balance_tree(root)
            
            return None # tree is now empty

        self._root = _delete(self._root, key)
        self._size -= 1

    def inorder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
        def _inorder(node: Optional[AVLNode]):
            if not node: 
                return
            _inorder(node.left)
            AVLTree._visit(node, keys, visit)
            _inorder(node.right)

        keys: List[K] = []
        _inorder(self._root)
        return keys

    def preorder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
        def _preorder(node: Optional[AVLNode]):
            if not node: return
            AVLTree._visit(node, keys, visit)
            _preorder(node.left)
            _preorder(node.right)

        keys: List[K] = []
        _preorder(self._root)
        return keys

    def postorder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
        def _postorder(node: Optional[AVLNode]):
            if not node: return
            _postorder(node.left)
            _postorder(node.right)
            AVLTree._visit(node, keys, visit)

        keys: List[K] = []
        _postorder(self._root)
        return keys
    
    def bforder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
        if not self._root: return []
        
        keys: List[K] = []
        queue = deque([self._root])

        while queue:
            node = queue.popleft()
            AVLTree._visit(node, keys, visit)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        return keys

    def size(self) -> int: return self._size

    def __str__(self) -> str:
        def draw_tree(node: Optional[AVLNode], level: int=0) -> None:
            if not node: return 
            draw_tree(node.right, level + 1)
            level_outputs.append(f'{" " * 4 * level} -> {str(node.value)}')
            draw_tree(node.left, level + 1)
        level_outputs: List[str] = []
        draw_tree(self._root)
        return '\n'.join(level_outputs)
    
    def __repr__(self) -> str:
        descriptions = ['Breadth First: ', 'In-order: ', 'Pre-order: ', 'Post-order: ']
        traversals = [self.bforder(), self.inorder(), self.preorder(), self.postorder()]
        return f'{"\n".join([f'{desc} {"".join(str(trav))}' for desc, trav in zip(descriptions, traversals)])}\n\n{str(self)}' 
   
    @staticmethod
    def _balance_tree(node: AVLNode) -> AVLNode:
        # Left rotation (LL)
        if AVLTree._balance_factor(node) > 1 and node.left and AVLTree._balance_factor(node.left) >= 0:
            return AVLTree._rotate_right(node)

        # Right rotation (RR)
        if AVLTree._balance_factor(node) < -1 and node.right and AVLTree._balance_factor(node.right) <= 0:
            return AVLTree._rotate_left(node)

        # Left-Right rotation (LR)
        if AVLTree._balance_factor(node) > 1 and node.left and AVLTree._balance_factor(node.left) < 0:
            node.left = AVLTree._rotate_left(node.left)
            return AVLTree._rotate_right(node)

        # Right-Left rotation (RL)
        if AVLTree._balance_factor(node) < -1 and node.right and AVLTree._balance_factor(node.right) > 0:
            node.right = AVLTree._rotate_right(node.right)
            return AVLTree._rotate_left(node)

        return node 

    @staticmethod
    def _rotate_left(node: AVLNode) -> AVLNode:
        new_root = node.right
        if not new_root: raise ValueError("new_root cannot be None for left rotation")

        new_left_subtree = new_root.left

        new_root.left = node
        node.right = new_left_subtree

        node.height = 1 + max(AVLTree._node_height(node.left), AVLTree._node_height(node.right))
        new_root.height = 1 + max(AVLTree._node_height(new_root.left), AVLTree._node_height(new_root.right))

        return new_root
    
    @staticmethod
    def _rotate_right(node: AVLNode) -> AVLNode:
        new_root = node.left
        if not new_root: raise ValueError("new_root cannot be None for right rotation")

        new_right_subtree = new_root.right

        new_root.right = node
        node.left = new_right_subtree

        node.height = 1 + max(AVLTree._node_height(node.left), AVLTree._node_height(node.right))
        new_root.height = 1 + max(AVLTree._node_height(new_root.left), AVLTree._node_height(new_root.right))

        return new_root
    
    @staticmethod
    def _find_successor(node: AVLNode) -> AVLNode:
        current = node
        while current.left: current = current.left
        return current

    @staticmethod
    def _node_height(node: Optional[AVLNode]) -> int: return node.height if node else 0

    @staticmethod
    def _balance_factor(node: AVLNode) -> int: return AVLTree._node_height(node.left) - AVLTree._node_height(node.right) if node else 0
 
    @staticmethod
    def _visit(node: AVLNode, result: List[K], visit: Optional[Callable[[V], None]] = None) -> None:
        visit and visit(node.value)
        result.append(node.key)