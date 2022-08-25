# It is assumed that performing multiple applications of the following function to any integer greater than zero will
# eventually produce a result of 1:
# f(x) -> x / 2; if x is even
# f(x) -> 3 * x + 1; if x is odd

# For example, starting from 5, it takes five steps to get to 1:
# 1. f(5) -> 16                            (3 * 5 + 1 = 16)
# 2.       f(16) -> 8                      (   16 / 2 =  8)
# 3.              f(8) -> 4                (    8 / 2 =  4)
# 4.                    f(4) -> 2          (    4 / 2 =  2)
# 5.                          f(2) -> 1    (    2 / 1 =  1)

# 1. How many steps does it take when starting from 57?
# 2. What number below 1000 takes the most steps in order to reach 1?

cache: dict[int, int] = {}


def f(x: int) -> int:
    if x % 2 == 0:
        return x / 2
    return 3 * x + 1


def steps(x: int) -> int:
    if x == 1:
        return 0
    if x in cache:
        return cache[x]
    new_x = f(x)
    r = steps(new_x) + 1
    cache[x] = r
    return r


print(steps(57))


max_steps = 0
max_i = 0
for i in range(1000000):
    step = steps(i + 1)
    if step > max_steps:
        max_steps = step
        max_i = i

print(max_steps, max_i)
