from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple


@dataclass
class FPNode:
    """A node in the FP tree."""

    value: Any
    count: int
    parent: Optional["FPNode"]
    link: Optional["FPNode"] = None
    children: List["FPNode"] = field(default_factory=list)

    def has_child(self, value: Any) -> bool:
        """Return ``True`` if a child with ``value`` exists."""
        return any(node.value == value for node in self.children)

    def get_child(self, value: Any) -> Optional["FPNode"]:
        """Return a child node with a particular value if present."""
        for node in self.children:
            if node.value == value:
                return node
        return None

    def add_child(self, value: Any) -> "FPNode":
        """Add and return a new child node."""
        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree:
    """A frequent pattern tree."""

    def __init__(
        self,
        transactions: Iterable[Iterable[Any]],
        threshold: int,
        root_value: Optional[Any],
        root_count: Optional[int],
    ) -> None:
        """Initialize the tree."""
        self.frequent: Dict[Any, int] = self.find_frequent_items(transactions, threshold)
        self.headers: Dict[Any, Optional[FPNode]] = self.build_header_table(self.frequent)
        self.root: FPNode = self.build_fptree(
            transactions, root_value, root_count, self.frequent, self.headers
        )

    @staticmethod
    def find_frequent_items(
        transactions: Iterable[Iterable[Any]],
        threshold: int,
    ) -> Dict[Any, int]:
        """Return items appearing at least ``threshold`` times."""
        items: Dict[Any, int] = {}

        for transaction in transactions:
            for item in transaction:
                items[item] = items.get(item, 0) + 1

        return {item: count for item, count in items.items() if count >= threshold}

    @staticmethod
    def build_header_table(frequent: Dict[Any, int]) -> Dict[Any, Optional[FPNode]]:
        """Build the header table."""
        return {key: None for key in frequent}

    def build_fptree(
        self,
        transactions: Iterable[Iterable[Any]],
        root_value: Optional[Any],
        root_count: Optional[int],
        frequent: Dict[Any, int],
        headers: Dict[Any, Optional[FPNode]],
    ) -> FPNode:
        """Build the FP tree and return the root node."""
        root = FPNode(root_value, root_count if root_count is not None else 1, None)

        for transaction in transactions:
            sorted_items = sorted(
                (item for item in transaction if item in frequent),
                key=lambda x: frequent[x],
                reverse=True,
            )
            if sorted_items:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(
        self,
        items: List[Any],
        node: FPNode,
        headers: Dict[Any, Optional[FPNode]],
    ) -> None:
        """Recursively grow FP tree."""
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if remaining_items:
            self.insert_tree(remaining_items, child, headers)

    def tree_has_single_path(self, node: FPNode) -> bool:
        """Return ``True`` if the tree has a single path starting at ``node``."""
        num_children = len(node.children)
        if num_children > 1:
            return False
        if num_children == 0:
            return True
        return self.tree_has_single_path(node.children[0])

    def mine_patterns(self, threshold: int) -> Dict[Tuple[Any, ...], int]:
        """Mine the constructed FP tree for frequent patterns."""
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        return self.zip_patterns(self.mine_sub_trees(threshold))

    def zip_patterns(
        self, patterns: Dict[Tuple[Any, ...], int]
    ) -> Dict[Tuple[Any, ...], int]:
        """Append suffix to patterns in dictionary if in a conditional tree."""
        suffix = self.root.value

        if suffix is None:
            return patterns

        return {
            tuple(sorted((*key, suffix))): value
            for key, value in patterns.items()
        }

    def generate_pattern_list(self) -> Dict[Tuple[Any, ...], int]:
        """Generate a list of patterns with support counts."""
        patterns: Dict[Tuple[Any, ...], int] = {}
        items = list(self.frequent)

        # If we are in a conditional tree, the suffix is a pattern on its own.
        if self.root.value is None:
            suffix_value: List[Any] = []
        else:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted((*subset, *suffix_value)))
                patterns[pattern] = min(self.frequent[x] for x in subset)

        return patterns

    def mine_sub_trees(self, threshold: int) -> Dict[Tuple[Any, ...], int]:
        """Generate subtrees and mine them for patterns."""
        patterns: Dict[Tuple[Any, ...], int] = {}
        mining_order = sorted(self.frequent, key=self.frequent.get)

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes: List[FPNode] = []
            conditional_tree_input: List[List[Any]] = []
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
                path: List[Any] = []
                parent = suffix.parent

                while parent and parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                conditional_tree_input.extend([path] * frequency)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(
    transactions: Iterable[Iterable[Any]], support_threshold: int
) -> Dict[Tuple[Any, ...], int]:
    """Given a set of transactions, return patterns meeting ``support_threshold``."""
    tree = FPTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)


def generate_association_rules(
    patterns: Dict[Tuple[Any, ...], int], confidence_threshold: float
) -> Dict[Tuple[Any, ...], List[Tuple[Tuple[Any, ...], float]]]:
    """Return rules grouped by antecedent with confidence >= ``confidence_threshold``."""
    rules: Dict[Tuple[Any, ...], List[Tuple[Tuple[Any, ...], float]]] = {}
    for itemset, upper_support in patterns.items():
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = upper_support / float(lower_support)

                    if confidence >= confidence_threshold:
                        rules.setdefault(antecedent, []).append(
                            (consequent, confidence)
                        )

    return rules
