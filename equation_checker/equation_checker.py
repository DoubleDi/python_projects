# [('a', '<', 'c'), ....]

# (a < c), (a < b) - correct
# (a < c), (a > b), (b > c) - incorrect


# --------a------b---------c---------

# ------b-----a----------------c-----

# (a < c), (a > b), (d > a)

# ------b-----a-----------d?--------c-----d?-


# {
#   c: a,
#   a: b
# }

# b: c


# set()
# {}

# (a < c)
# set(a,c)
# {c: a}

# (a > b)
# set(a,c,b)
# {c: set(a), a: set(b)}

# (b > c)
# set(a,c,b)
# {b: c} is there a path from c to b?
# if there is => False

# [('a', '<', 'c'), ('c' '>' 'b')]


# (a<b), (b<a)

# (a<a)

# {b:a}
# has_path({b:a}, b, a)


from collections import deque
from typing import Deque, Dict, List, Set, Tuple


def f(eqs: List[Tuple[str, str, str]]) -> bool:
    if not len(eqs):
        return True
    al: Set[str] = set()
    m: Dict[str, Set[str]] = {}
    for eq in eqs:
        if eq[0] == eq[2]:
            return False

        if not eq[0] in al or not eq[2] in al:
            if eq[1] == '<':
                m.setdefault(eq[2], set())
                m[eq[2]].add(eq[0])
            if eq[1] == '>':
                m.setdefault(eq[0], set())
                m[eq[0]].add(eq[2])
            al.add(eq[0])
            al.add(eq[2])
            continue

        if eq[1] == '<':
            if has_path(m, eq[0], eq[2]):
                return False

        if eq[1] == '>':
            if has_path(m, eq[2], eq[0]):
                return False
    return True


def has_path(m: Dict[str, Set[str]], start: str, to: str) -> bool:
    seen: Set[str] = set([])
    processing: Deque[str] = deque([start])
    while len(processing):
        v = processing.popleft()
        if v == to:
            return True
        if v in seen:
            continue
        for vv in list(m.get(v, set())):
            if not vv in seen:
                processing.append(vv)
        seen.add(v)

    return False
