# import requests
# import mysql.connector
# import pandas as pd

# Verify whether a long text is following the order rule defined in order string.
# For example the order string is "abcd", which means "a" can't appear at any position after "b", "c" and "d" in the text,
# "b" can't appear at any position after "c" and "d" in the text and "c" can't appear at any position after "d" in the text.
# if the text is "axubbxcxbxd", then the text didn't follow the rule, since "b" appears after "c" in substring "cxb".

# abcd
# aaaaaa
# bbbbbb
# aaaaabbb
# aaaacccccdddd
# aaadddd
# aaaxxxxdddd


# invalid
# ddddaaaa


# abcdabcd

# abcd abcd
# a -> b,c,d
# b -> c,d
# c -> d
# d ->

import concurrent.futures
from typing import List, Tuple

cpus = 2


def parallel_check_text_ordering(text: str, ordering_string: str) -> Tuple[bool, str]:
    text_parts = []
    l = int(len(text) / cpus)
    while text:
        text_parts.append(text[:l])
        text = text[l:]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for part in text_parts:
            future = executor.submit(check_text_ordering, part, ordering_string)
            futures.append(future)

        results = []
        for future in futures:
            ordered, visited = future.result()
            results.append((ordered, visited))

    return merge_results(results, ordering_string)


def merge_results(results: List[Tuple[bool, str]], ordering_string: str) -> Tuple[bool, str]:
    result_string = ''
    for (ordered, visited) in results:
        if not ordered:
            return False
        result_string += visited
    return check_text_ordering(result_string, ordering_string)


# aaaacccccdddd
def check_text_ordering(text: str, ordering_string: str) -> Tuple[bool, str]:
    letters = set(ordering_string)
    after = {}
    for i, l in enumerate(ordering_string):
        after[l] = set(ordering_string[i + 1 :])
    visited = set()
    result_string = ''

    for l in text:
        if not l in letters:
            continue
        if len(after.get(l, set()) & visited):
            return False, result_string
        if not l in visited:
            visited.add(l)
            result_string += l

    return True, result_string


print(check_text_ordering('aaaaaa', 'abcd'))
print(check_text_ordering('bbbbbb', 'abcd'))
print(check_text_ordering('aaaaabbb', 'abcd'))
print(check_text_ordering('aaaacccccdddd', 'abcd'))
print(check_text_ordering('aaadddd', 'abcd'))
print(check_text_ordering('aaaxxxxdddd', 'abcd'))

print(check_text_ordering('ddddaaaa', 'abcd'))

print(parallel_check_text_ordering('abcdabcd', 'abcd'))
print(parallel_check_text_ordering('abbbcccd', 'abcd'))
