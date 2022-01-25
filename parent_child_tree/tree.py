'''
Suppose we have some input data describing a graph of relationships between parents and children over multiple generations. The data is formatted as a list of (parent, child) pairs, where each individual is assigned a unique positive integer identifier.

For example, in this diagram, the earliest ancestor of 6 is 14, and the earliest ancestor of 15 is 2. 

         14
         |
  2      4
  |    / | \
  3   5  8  9
 / \ / \     \
15  6   7    11

Write a function that, for a given individual in our dataset, returns their earliest known ancestor -- the one at the farthest distance from the input individual. If there is more than one ancestor tied for "earliest", return any one of them. If the input individual has no parents, the function should return null (or -1).

Sample input and output:

parent_child_pairs_3_1 = [
    (2, 3), (3, 15), (3, 6), (5, 6), (5, 7),
    (4, 5), (4, 8), (4, 9), (9, 11), (14, 4),
]

find_earliest_ancestor(parent_child_pairs_3_1, 8) => 14
find_earliest_ancestor(parent_child_pairs_3_1, 7) => 14
find_earliest_ancestor(parent_child_pairs_3_1, 6) => 14
find_earliest_ancestor(parent_child_pairs_3_1, 15) => 2
find_earliest_ancestor(parent_child_pairs_3_1, 14) => null or -1
find_earliest_ancestor(parent_child_pairs_3_1, 11) => 14

Additional example:

  14
  |
  2      4    1
  |    / | \ /
  3   5  8  9
 / \ / \     \
15  6   7    11

parent_child_pairs_3_2 = [
    (2, 3), (3, 15), (3, 6), (5, 6), (5, 7),
    (4, 5), (4, 8), (4, 9), (9, 11), (14, 2), (1, 9)
]

find_earliest_ancestor(parent_child_pairs_3_2, 8) => 4
find_earliest_ancestor(parent_child_pairs_3_2, 7) => 4
find_earliest_ancestor(parent_child_pairs_3_2, 6) => 14
find_earliest_ancestor(parent_child_pairs_3_2, 15) => 14
find_earliest_ancestor(parent_child_pairs_3_2, 14) => null or -1
find_earliest_ancestor(parent_child_pairs_3_2, 11) => 4 or 1

n: number of pairs in the input



'''

from typing import Dict, List, Set, Tuple

parent_child_pairs_3_1 = [
    (2, 3),
    (3, 15),
    (3, 6),
    (5, 6),
    (5, 7),
    (4, 5),
    (4, 8),
    (4, 9),
    (9, 11),
    (14, 4),
]

parent_child_pairs_3_2 = [(2, 3), (3, 15), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (4, 9), (9, 11), (14, 2), (1, 9)]


def find_nodes_with_zero_and_one_parents(parent_child_pairs: List[Tuple[int, int]]) -> Tuple[List[int], List[int]]:
    parent_count = {}
    for parent, child in parent_child_pairs:
        if parent not in parent_count:
            parent_count[parent] = 0
        if child not in parent_count:
            parent_count[child] = 0
        parent_count[child] += 1

    zero_parents = []
    one_parent = []
    for child, count in parent_count.items():
        if count == 0:
            zero_parents.append(child)
        if count == 1:
            one_parent.append(child)
    return (zero_parents, one_parent)


# print(find_nodes_with_zero_and_one_parents(parent_child_pairs))


def has_common_ancestor(parent_child_pairs: List[Tuple[int, int]], child1: int, child2: int) -> bool:
    child_to_parents = {}
    for parent, child in parent_child_pairs:
        if child not in child_to_parents:
            child_to_parents[child] = []
        child_to_parents[child].append(parent)

    ancestors1 = collect_ancestors(child_to_parents, child1)
    #     print(ancestors1)
    ancestors2 = collect_ancestors(child_to_parents, child2)
    #     print(ancestors2)
    return len(ancestors1 & ancestors2) > 0


def collect_ancestors(child_to_parents: Dict[int, List[int]], child: int) -> Set[int]:
    ancestors = set()
    queue = [child]
    while queue:
        child = queue[0]
        queue = queue[1:]
        parents = child_to_parents.get(child, [])
        for parent in parents:
            ancestors.add(parent)
            queue.append(parent)
    return ancestors


# print(has_common_ancestor(parent_child_pairs_2, 3, 8))#   => false
# print(has_common_ancestor(parent_child_pairs_2, 5, 8))#   => true
# print(has_common_ancestor(parent_child_pairs_2, 6, 8))#   => true
# print(has_common_ancestor(parent_child_pairs_2, 6, 9))#   => true
# print(has_common_ancestor(parent_child_pairs_2, 1, 3))#   => false
# print(has_common_ancestor(parent_child_pairs_2, 3, 1))#   => false
# print(has_common_ancestor(parent_child_pairs_2, 7, 11))#  => true
# print(has_common_ancestor(parent_child_pairs_2, 6, 5))#   => true
# print(has_common_ancestor(parent_child_pairs_2, 5, 6))#   => true
# print(has_common_ancestor(parent_child_pairs_2, 3, 6))#   => true
# print(has_common_ancestor(parent_child_pairs_2, 21, 11))# => True


def find_earliest_ancestor(parent_child_pairs: List[Tuple[int, int]], child: int) -> bool:
    child_to_parents = {}
    for parent, c in parent_child_pairs:
        if c not in child_to_parents:
            child_to_parents[c] = []
        child_to_parents[c].append(parent)

    ancestors = collect_ancestors_with_levels(child_to_parents, child)
    if not ancestors:
        return -1
    max_a, max_l = -1, -1
    for a, l in ancestors:
        if l > max_l:
            max_a = a
            max_l = l
    return max_a


def collect_ancestors_with_levels(child_to_parents: Dict[int, List[int]], child: int) -> Set[Tuple[int, int]]:
    ancestors = set()
    queue = [(child, 0)]
    while queue:
        child, level = queue[0]
        queue = queue[1:]
        parents = child_to_parents.get(child, [])
        for parent in parents:
            ancestors.add((parent, level + 1))
            queue.append((parent, level + 1))
    return ancestors


print(find_earliest_ancestor(parent_child_pairs_3_2, 8))  # => 4
print(find_earliest_ancestor(parent_child_pairs_3_2, 7))  # => 4
print(find_earliest_ancestor(parent_child_pairs_3_2, 6))  # => 14
print(find_earliest_ancestor(parent_child_pairs_3_2, 15))  # => 14
print(find_earliest_ancestor(parent_child_pairs_3_2, 14))  # => null or -1
print(find_earliest_ancestor(parent_child_pairs_3_2, 11))  # => 4 or 1
