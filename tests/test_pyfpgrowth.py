#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyfpgrowth
----------------------------------

Tests for pyfpgrowth` module.
"""

import unittest
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
    """
    support_threshold = 2
    transactions = [[1, 2, 5],
                    [2, 4],
                    [2, 3],
                    [1, 2, 4],
                    [1, 3],
                    [2, 3],
                    [1, 3],
                    [1, 2, 3, 5],
                    [1, 2, 3]]

    def test_find_frequent_patterns(self):
        patterns = find_frequent_patterns(self.transactions, self.support_threshold)

        expected = {(1, 2): 4, (1, 2, 3): 2, (1, 3): 4, (1,): 6, (2,): 7, (2, 4): 2,
                    (1, 5): 2, (5,): 2, (2, 3): 4, (2, 5): 2, (4,): 2, (1, 2, 5): 2}
        self.assertEqual(patterns, expected)

    def test_generate_association_rules(self):
        patterns = find_frequent_patterns(self.transactions, self.support_threshold)
        rules = generate_association_rules(patterns, 0.7)

        expected = {(1, 5): ((2,), 1.0), (5,): ((1, 2), 1.0),
                    (2, 5): ((1,), 1.0), (4,): ((2,), 1.0)}
        self.assertEqual(rules, expected)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
