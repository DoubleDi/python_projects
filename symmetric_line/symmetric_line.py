from typing import List, Tuple

# // Дан массив точек с целочисленными координатами (x, y).
# // Определить, существует ли вертикальная прямая, делящая все точки, не лежащие на ней, на 2 симметричных относительно этой прямой множества.


def f(a: List[Tuple[int, int]]) -> bool:
    if not len(a):
        return False

    minx = min(x for (x, y) in a)
    maxx = max(x for (x, y) in a)

    result = {}
    for x, y in a:
        b = -1
        r = x - minx
        if maxx - x == r:
            b = 0
        if maxx - x < r:
            b = 1
            r = maxx - x

        if (r, y) in result:
            result[(r, y)] += b
        else:
            result[(r, y)] = b

    for v in result.values():
        if v != 0:
            return False

    return True


# (-3, 1), (3, 1)

# (-2, 1), (4, 1)

# maxx = 4
# minx = -2

# (-2, 1)
# 4 + 2 = 6 ? -2 +2 = 0 => 0

# (4, 1)
# 4-4 = 0 ? 4 + 2 = 6

# (-3, 1), (3, 1), (-2, 1), (-2, 1)
