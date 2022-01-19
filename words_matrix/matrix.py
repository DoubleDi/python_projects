# import requests
# import mysql.connector
# import pandas as pd
#
# Given a 2-dimensional grid of characters, and a dictionary, find all words in the grid that also appear in the dictionary. A word can be formed by traversing the grid by going either left, right, top, or down, but NOT diagonal. Also, a single grid position can not be used more than once in a word.
# For instance, in the following 3x3 grid, with a dictionary of

# [ CAT, COPY, ASK, SOS ] M K
#
# C A T
# O S K
# P Y U
#
# The first 3 words can be found in the grid, but not SOS, since one cannot use S twice.

from typing import Dict, List, Tuple

# N*N*M + M*K


# N*N*N*N


def f(m: List[List[str]], d: List[str]) -> List[str]:
    result = []
    for w in d:
        indexes = find_indexes(m, w)
        for index in indexes:
            if has_path(m, index[0], index[1], w[1:], {(index[0], index[1]): True}):
                result.append(w)
                break
    return result


def find_indexes(m: List[List[str]], w: str) -> List[Tuple[int, int]]:
    result = []
    for i, r in enumerate(m):
        for j, c in enumerate(r):
            if m[i][j] == w[0]:
                result.append((i, j))
    return result


def has_path(m: List[List[str]], i: int, j: int, w: str, visited: Dict[Tuple[int, int], bool]) -> bool:
    if len(w) == 0:
        return True

    if i > 0 and not visited.get((i - 1, j)) and m[i - 1][j] == w[0]:
        result = has_path(m, i - 1, j, w[1:], {**visited, (i - 1, j): True})
        if result:
            return True
    if j > 0 and not visited.get((i, j - 1)) and m[i][j - 1] == w[0]:
        result = has_path(m, i, j - 1, w[1:], {**visited, (i, j - 1): True})
        if result:
            return True
    if i + 1 < len(m) and not visited.get((i + 1, j)) and m[i + 1][j] == w[0]:
        result = has_path(m, i + 1, j, w[1:], {**visited, (i + 1, j): True})
        if result:
            return True
    if j + 1 < len(m[0]) and not visited.get((i, j + 1)) and m[i][j + 1] == w[0]:
        result = has_path(m, i, j + 1, w[1:], {**visited, (i, j + 1): True})
        if result:
            return True

    return False


print(f([['C', 'A', 'T'], ['O', 'S', 'K'], ['P', 'Y', 'U']], ['CAT', 'COPY', 'ASK', 'SOS']))
