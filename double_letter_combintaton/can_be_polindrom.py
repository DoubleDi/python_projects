# Дана строка s. Необходимо сказать, можно ли переставить
# буквы в строке так, чтобы получился палиндром.


def f(s: str) -> bool:
    d = {}
    for c in s:
        d.setdefault(c, 0)
        d[c] += 1

    r = 0
    for v in d.values():
        if v % 2 == 1:
            r += 1

    if r > 1:
        return False

    return True
