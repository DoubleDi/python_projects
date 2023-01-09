'''
Start with 2 words, eg NO and POINT. A "ladder" is a set of "steps" that connects the words.

For example, this is a ladder:

NO -> NOT -> INTO -> POINT

Write a function that takes 2 words, the index, and the 15-word wordlist and returns the "best" ladder that connects them, if any exists. The "best" ladder is the one that maximizes the sum of the occurrence counts of each word in the ladder, as found in the original download.

ladder('NO', 'POINT', index, wordlist) -> ['NO', 'NOT', 'INTO', 'POINT']
ladder('OF', 'FORMS', index, wordlist) -> [ 'OF', 'FOR', 'FROM', 'FORMS ]
ladder('ON', 'LEFT', index, wordlist) -> None

Complexity analysis variables:

n: Number of words
e: number of edges between words in index
'''


counts = [
    'OF,30966074232',
    'FOR,6545282031',
    'ON,4594521081',
    'NOT,4522732626',
    'FROM,3469207674',
    'ONE,2148983086',
    'NO,1400645478',
    'INTO,1144226142',
    'NOW,679337516',
    'FORM,352032932',
    'POINT,333858038',
    'LEFT,306802162',
    'OFF,302535533',
    'FOUR,262968583',
    'FORMS,136468034',
]
wordlist = [
    ('OF', 30966074232),
    ('FOR', 6545282031),
    ('ON', 4594521081),
    ('NOT', 4522732626),
    ('FROM', 3469207674),
    ('ONE', 2148983086),
    ('NO', 1400645478),
    ('INTO', 1144226142),
    ('NOW', 679337516),
    ('FORM', 352032932),
    ('POINT', 333858038),
    ('LEFT', 306802162),
    ('OFF', 302535533),
    ('FOUR', 262968583),
    ('FORMS', 136468034),
]

index = [
    ('OF', ['FOR', 'OFF']),
    ('FOR', ['FROM', 'FORM', 'FOUR']),
    ('ON', ['NOT', 'ONE', 'NOW']),
    ('NOT', ['INTO']),
    ('FROM', ['FORMS']),
    ('ONE', []),
    ('NO', ['NOT', 'ONE', 'NOW']),
    ('INTO', ['POINT']),
    ('NOW', []),
    ('FORM', ['FORMS']),
    ('POINT', []),
    ('LEFT', []),
    ('OFF', []),
    ('FOUR', []),
    ('FORMS', []),
]


def ladder(fr: str, to: str, index: list[tuple[str, int]], wordlist: list[tuple[str, list[str]]]):
    # print(dict(index))
    # print(dict(wordlist))
    has_path, count, wl = find(fr, to, dict(index), dict(wordlist))
    if not has_path:
        return None
    return [fr] + wl


def find(fr: str, to: str, index: dict[str, int], wordlist: dict[str, list[str]]) -> tuple[bool, int, list[str]]:
    if fr == to:
        return True, 0, []
    max_count, max_wl = 0, []
    for word in index[fr]:
        has_path, count, wl = find(word, to, index, wordlist)
        if not has_path:
            continue
        count += wordlist[word]
        wl = [word] + wl

        if count > max_count:
            max_count = count
            max_wl = wl
    return max_count != 0, max_count, max_wl


print(ladder('NO', 'POINT', index, wordlist))
print(ladder('OF', 'FORMS', index, wordlist))
print(ladder('ON', 'LEFT', index, wordlist))


def to_dict(word: str) -> dict[str, int]:
    d = {}
    for w in word:
        d.setdefault(w, 0)
        d[w] += 1
    return d


def step_index(wordlist: list[tuple[str, int]]) -> list[tuple[str, list[str]]]:
    words = []
    word_to_dict = {}
    for w in wordlist:
        words.append(w[0])
        word_to_dict[w[0]] = to_dict(w[0])

    result = []
    for w in words:
        similair = []
        for w2 in words:
            # print(w,w2)
            if match(word_to_dict[w], word_to_dict[w2]):
                similair.append(w2)
        result.append((w, similair))
    return result


def match(w: dict[str, int], w2: dict[str, int]) -> bool:
    diffs = 0
    for k, v in w.items():
        if k not in w2:
            return False
    for k2, v2 in w2.items():
        v = w.get(k2, 0)
        if v > v2 or v + 1 < v2:
            return False
        if v == v2:
            continue
        if v + 1 == v2:
            diffs += 1
            continue
    # print(w, w2, diffs)
    return diffs == 1


print(step_index(counts))


def get_list(counts: list[str], top: int, l: int) -> list[tuple[str, int]]:
    filtered = []
    for c in counts:
        (word, count) = c.split(',')
        if len(word) > l or len(word) < 2:
            continue
        filtered.append((word, int(count)))
    filtered.sort(key=lambda v: v[1], reverse=True)
    return filtered[:top]


print(get_list(counts, 15, 5))
