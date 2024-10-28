from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple

from datastructures.avltree import AVLTree
from datastructures.avlnode import AVLNode



# I opted for a traversal strategy which I think would be fairly unique. Instead of traversing the 
# nested trees as we would when traversing one AVLTree on its own, I've decided to traverse by 
# cutting away subtrees which could not qualify for the query based on the parameters, and using
# .inorder() to traverse across the valid nodes in the "lows" AVLTree to find valid "high" pairs, 
# and thus the relevant stock(s). This is to accommodate the difficulty of using binary strategies 
# to traverse non-binary nodes i.e. intervals, and the fact that the value we are looking for may 
# be in more than one node. While these superficial strategies may not have optimal time compexity,
# none are worse than O(n), and the most common and volumous tasks still use the embedded O(log(n))
# time complexity strategies. 
# 
# Also, it seems like your 'synthetic_stock_data.csv' and 'synthetic_stock_test_outputs.txt' files
# do not line up correctly. I've combed through both files personally and found that the outputs 
# must have came from the synthetic data, but entries in the synthetic data which should be picked
# up by certain queries are not shown in the output text file. This means that the outputs are missing
# stock entries that should qualify for the query.

@dataclass
class IntervalNode:
    key: int
    value: Any
    max_end: int = 0
    intervals_at_low: AVLTree = AVLTree()
    def __repr__(self):
        return f'{self.key}, {self.max_end}'

class IntervalTree:
    def __init__(self):
        self._tree: AVLTree = AVLTree()

    def insert(self, low: int, high: int, value: Any):
        node: IntervalNode = self._tree.search(low)
        if node:
            silly_duplicate_low_high_combo_bool = True      # stocks having the same low works fine because of using the high as
            while silly_duplicate_low_high_combo_bool:      # a differentiator. But if the low AND the high are the same, this goofy
                try:                                        # loop solves that by nudging the high up by an unnoticable amount.
                    node.intervals_at_low.insert(high, value)
                    silly_duplicate_low_high_combo_bool = False
                except:
                    high += 0.001

        else:
            node = IntervalNode(key=low, value=value, max_end=high, intervals_at_low=AVLTree())
            node.intervals_at_low.insert(high, value)
            self._tree.insert(low, node)

        node.max_end = self._update_max_end(node.intervals_at_low._root)
    
    def _update_max_end(self, node: AVLNode):
        check = node
        while check.right:
            check = check.right
        return check.key
    
    def delete(self, value: Any):
        start: AVLTree = self._tree
        lows = start.inorder() 
        for low in lows:
            node: IntervalNode = start.search(low)
            highs_tree: AVLTree = node.intervals_at_low
            highs = highs_tree.inorder()
            for high in highs:
                value_associated_with_high = highs_tree.search(high)
                if value_associated_with_high == value:
                    highs_tree.delete(high)
    
    def search(self, start: int, end: int | None = None, fancy: bool = False):
        intervals = self._search_range(start, end) if end else self._search_point(start)
        if fancy:
            if end: string = f"Range query for stocks with low-high intervals overlapping with [${start}, ${end}]:"
            else: string = f"Search query for stocks containing price point ${start}:"
            for i in intervals:
                string += f"\n{i}"
            return string
        return intervals
    
    def _search_point(self, value: int):
        intervals = []
        valid_lows = [self._tree.search(low) for low in self._tree.inorder() if self._tree.search(low).key <= value and value <= self._tree.search(low).max_end] # only search through nodes whos low is <= the Value and max_end is >= the Value, cutting off unnecessary searches on both sides.
        for node in valid_lows:
            node: IntervalNode
            for high in node.intervals_at_low.inorder():
                if value <= high:
                    intervals.append(node.intervals_at_low.search(high))
        return intervals
    
    def _search_range(self, start: int, end: int):
        intervals = []
        valid_lows = [self._tree.search(low) for low in self._tree.inorder() if self._tree.search(low).key <= end and start <= self._tree.search(low).max_end] # only search through nodes whos low is <= the Value and max_end is >= the Value
        for node in valid_lows:
            node: IntervalNode
            for high in node.intervals_at_low.inorder():
                intervals.append(node.intervals_at_low.search(high))
        return intervals

    def bottom_k(self, k: int, fancy: bool = False):
        intervals = []
        lows = self._tree.inorder()
        for low in lows:
            low_node: IntervalNode = self._tree.search(low)
            highs_tree = low_node.intervals_at_low
            for high in highs_tree.inorder():
                high_node = highs_tree.search(high)
                if len(intervals) < k: intervals.append(high_node)
                else: break
            else: continue
            break

        if fancy:
            string = f"Bottom {len(intervals)} Queries:"
            for i in intervals:
                string += f"\n{i}"
            return string
        return intervals
    
    def top_k(self, k: int, fancy: bool = False):
        intervals = []
        lows = self._tree.inorder()
        lows.reverse()
        for low in lows:
            low_node: IntervalNode = self._tree.search(low)
            highs_tree = low_node.intervals_at_low
            highs = highs_tree.inorder()
            highs.reverse()
            for high in highs:
                high_node = highs_tree.search(high)
                if len(intervals) < k: intervals.append(high_node)
                else: break
            else: continue
            break
        
        if fancy:
            string = f"Top {len(intervals)} Queries:"
            for i in intervals:
                string += f"\n{i}"
            return string
        return intervals
        

