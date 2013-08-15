#!/usr/bin/env python

import sys
import itertools


class FPNode(object):
    """
    A node in the FP tree.
    """

    def __init__(self, value, count, parent):
        """
        Create the node.
        """
        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def hasChild(self, value):
        """
        Check if node has a particular child node.
        """
        for node in self.children:
            if node.value == value:
                return True

        return False

    def getChild(self, value):
        """
        Return a child node with a particular value.
        """
        for node in self.children:
            if node.value == value:
                return node

        return None

    def addChild(self, value):
        """
        Add a node as a child node.
        """
        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree(object):
    """
    A frequent pattern tree.
    """

    def __init__(self, transactions, threshold, rootValue, rootCount):
        """
        Initialize the tree.
        """
        self.frequent = self.findFrequentItems(transactions, threshold)
        self.headers = self.buildHeaderTable(self.frequent)
        self.root = self.buildFPTree(
            transactions, rootValue,
            rootCount, self.frequent, self.headers)

    def findFrequentItems(self, transactions, threshold):
        """
        Create a dictionary of items with occurrences above the threshold.
        """
        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for key in items.keys():
            if items[key] < threshold:
                del items[key]

        return items

    def buildHeaderTable(self, frequent):
        """
        Build the header table.
        """
        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers

    def buildFPTree(self, transactions, rootValue,
                    rootCount, frequent, headers):
        """
        Build the FP tree and return the root node.
        """
        root = FPNode(rootValue, rootCount, None)

        for transaction in transactions:
            sortedItems = [x for x in transaction if x in frequent]
            sortedItems.sort(key=lambda x: frequent[x], reverse=True)
            if len(sortedItems) > 0:
                self.insertTree(sortedItems, root, headers)

        return root

    def insertTree(self, items, node, headers):
        """
        Recursively grow FP tree.
        """
        first = items[0]
        child = node.getChild(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.addChild(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remainingItems = items[1:]
        if len(remainingItems) > 0:
            self.insertTree(remainingItems, child, headers)

    def treeHasSinglePath(self, node):
        """
        If there is a single path in the tree,
        return True, else return False.
        """
        numChildren = len(node.children)
        if numChildren > 1:
            return False
        elif numChildren == 0:
            return True
        else:
            return True and self.treeHasSinglePath(node.children[0])

    def minePatterns(self, threshold):
        """
        Mine the constructed FP tree for frequent patterns.
        """
        if self.treeHasSinglePath(self.root):
            return self.generatePatternList()
        else:
            return self.zipPatterns(self.mineSubTrees(threshold))

    def zipPatterns(self, patterns):
        """
        Append suffix to patterns in dictionary if
        we are in a conditional FP tree.
        """
        suffix = self.root.value

        if suffix is not None:
            # We are in a conditional tree.
            newPatterns = {}
            for key in patterns.keys():
                newPatterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return newPatterns

        return patterns

    def generatePatternList(self):
        """
        Generate a list of patterns with support counts.
        """
        patterns = {}
        items = self.frequent.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.value is None:
            suffixValue = []
        else:
            suffixValue = [self.root.value]
            patterns[tuple(suffixValue)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffixValue))
                patterns[pattern] = \
                    min([self.frequent[x] for x in subset])

        return patterns

    def mineSubTrees(self, threshold):
        """
        Generate subtrees and mine them for patterns.
        """
        patterns = {}
        miningOrder = sorted(self.frequent.keys(),
                             key=lambda x: self.frequent[x])

        # Get items in tree in reverse order of occurrences.
        for item in miningOrder:
            suffixes = []
            conditionalTreeInput = []
            node = self.headers[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.link

            # For each occurrence of the item, 
            # trace the path back to the root node.
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                for i in range(frequency):
                    conditionalTreeInput.append(path)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FPTree(conditionalTreeInput, threshold,
                             item, self.frequent[item])
            subtreePatterns = subtree.minePatterns(threshold)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtreePatterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtreePatterns[pattern]
                else:
                    patterns[pattern] = subtreePatterns[pattern]

        return patterns


def generateAssociationRules(patterns, confidenceThreshold):
    """
    Given a set of frequent itemsets, return a dict
    of association rules in the form
    {(left): ((right), confidence)}
    """
    rules = {}
    for itemset in patterns.keys():
        upperSupport = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lowerSupport = patterns[antecedent]
                    confidence = float(upperSupport) / lowerSupport

                    if confidence >= confidenceThreshold:
                        rules[antecedent] = (consequent, confidence)

    return rules


def main():
    """
    Main function including tests.
    """
    print "*** Testing FPGrowth Algorithm ***"
    sys.setrecursionlimit(10000)

    # Example from Data Mining textbook.
    transactions = [[1, 2, 5],
                    [2, 4],
                    [2, 3],
                    [1, 2, 4],
                    [1, 3],
                    [2, 3],
                    [1, 3],
                    [1, 2, 3, 5],
                    [1, 2, 3]]

    supportThreshold = 2
    tree = FPTree(transactions, supportThreshold, None, None)
    patterns = tree.minePatterns(supportThreshold)

    print "Frequent patterns:", patterns
    print "Patterns found:", len(patterns)

    # Belgian supermarket checkout data.
    data = open("belgian_retail_baskets.dat")
    lines = data.readlines()
    bigDataset = [None] * len(lines)
    for i, line in enumerate(lines):
        bigDataset[i] = [int(x) for x in lines[i].split()]

    supportThreshold = 100
    tree = FPTree(bigDataset, supportThreshold, None, None)
    patterns = tree.minePatterns(supportThreshold)

    print "Frequent patterns:", patterns
    print "Patterns found:", len(patterns)

    # Generate association rules from the frequent itemsets.
    minConfidence = 0.7
    rules = generateAssociationRules(patterns, minConfidence)
    for rule in rules.keys():
        print rule, "=>", rules[rule]

    print "Number of rules found:", len(rules)


if __name__ == "__main__":
    main()
