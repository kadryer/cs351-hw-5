from __future__ import annotations
from typing import Generic, Optional

from datastructures.iavltree import K, V

class AVLNode(Generic[K, V]):
    def __init__(self, key: K, value: V, left: Optional[AVLNode]=None, right: Optional[AVLNode]=None):
        self._key: K = key
        self._value: V = value
        self._left: Optional[AVLNode] = left
        self._right: Optional[AVLNode] = right
        self._height: int = 1

    @property 
    def key(self) -> K: return self._key
    @key.setter
    def key(self, key: K) -> None: self._key = key
    @property
    def value(self) -> V: return self._value
    @value.setter
    def value(self, value: V) -> None: self._value = value
    @property
    def left(self) -> Optional[AVLNode]: return self._left
    @left.setter
    def left(self, left: Optional[AVLNode]) -> None: self._left = left
    @property
    def right(self) -> Optional[AVLNode]: return self._right
    @right.setter
    def right(self, right: Optional[AVLNode]) -> None: self._right = right
    @property
    def height(self) -> int: return self._height
    @height.setter
    def height(self, height: int) -> None: self._height = height