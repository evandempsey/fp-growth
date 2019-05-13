#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyfpgrowth
----------------------------------

Tests for pyfpgrowth` module.
"""

import unittest
from itertools import chain, combinations

from pyfpgrowth import *
from pyfpgrowth.pyfpgrowth import FPNode, FPTree


class FPNodeTests(unittest.TestCase):
    """
    Tests for the FPNode class.
    """

    def setUp(self):
        """
        Build a node then test the features of it.
        """
        self.node = FPNode(1, 2, None)
        self.node.add_child(2)

    def test_has_child(self):
        """
        Create a root node and test that it has no parent.
        """
        self.assertEquals(self.node.has_child(3), False)
        self.assertEquals(self.node.has_child(2), True)

    def test_get_child(self):
        """
        Test that getChild() returns a node for a valid value
        and None for an invalid value.
        """
        self.assertNotEquals(self.node.get_child(2), None)
        self.assertEquals(self.node.get_child(5), None)

    def test_add_child(self):
        """
        Test that addChild() successfully adds a child node.
        """
        self.assertEquals(self.node.get_child(3), None)
        self.node.add_child(3)
        self.assertNotEquals(self.node.get_child(3), None)
        self.assertEquals(type(self.node.get_child(3)), type(self.node))


class FPTreeTests(unittest.TestCase):
    """
    Tests for the FPTree class.
    """

    def test_build_header_table(self):
        """
        Test that buildHeaderTable() returns a dict with all None values.
        """
        tree = FPTree([], 3, None, None)
        frequent = {1: 12, 2: 43, 6: 32}
        headers = tree.build_header_table(frequent)

        self.assertEquals(headers[1], None)
        self.assertEquals(headers[2], None)
        self.assertEquals(headers[6], None)


class FPGrowthTests(unittest.TestCase):
    """
    Tests everything together.

    Example is taken from [Agrawal1994]_.

    .. [Agrawal1994] Rakesh Agrawal and Ramakrishnan Srikant. 1994. Fast Algorithms for
       Mining Association Rules in Large Databases. In Proceedings of the 20th
       International Conference on Very Large Data Bases (VLDB '94), Jorge B. Bocca,
       Matthias Jarke, and Carlo Zaniolo (Eds.). Morgan Kaufmann Publishers Inc., San
       Francisco, CA, USA, 487-499.
    """
    support_threshold = 2
    transactions = [
        [1, 3, 4],
        [2, 3, 5],
        [1, 2, 3, 5],
        [2, 5]
    ]
    expected_frequent_item_sets = {(1,): 2, (2,): 3, (3,): 3, (5,): 3, (1, 3): 2, (2, 3): 2, (2, 5): 3, (3, 5): 2,
                                   (2, 3, 5): 2}

    def test_find_frequent_patterns(self):
        patterns = find_frequent_patterns(self.transactions, self.support_threshold)

        self.assertEquals(patterns, self.expected_frequent_item_sets)

    def test_generate_association_rules(self):
        confidence_threshold = 0.1

        def get_non_empty_subsets(iterable):
            """Return all non empty subsets of ``iterable`` including ``iterable`` itself."""
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

        expected = {}
        for frequent_item in self.expected_frequent_item_sets:
            for left_side in get_non_empty_subsets(frequent_item):
                support = self.expected_frequent_item_sets[frequent_item]
                support_of_left_side = self.expected_frequent_item_sets[left_side]
                right_side = tuple(sorted(set(frequent_item) - set(left_side)))
                confidence = self.expected_frequent_item_sets[frequent_item] / support_of_left_side

                if confidence >= confidence_threshold:
                    expected[(left_side, right_side)] = (support, confidence)

        association_rules = generate_association_rules(self.expected_frequent_item_sets, confidence_threshold)
        self.assertEquals(expected, association_rules)


if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
