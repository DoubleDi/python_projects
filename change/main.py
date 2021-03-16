def getChange(m, p):
    d = round(m - p, 2)
    result = []
    for i in [1, 0.5, 0.25, 0.1, 0.05, 0.01]:
        x = 0
        while d >= i:
            d -= i
            d = round(d, 2)
            x += 1
        result.append(x)

    return result[::-1]


# print(getChange(3.14, 1.99))
# print(getChange(3, 0.01))
# print(getChange(4, 3.14))
# print(getChange(0.45, 0.34))

###############################


def findWord(a):
    lefts = set()
    rights = set()
    l2r = dict()
    for c in a:
        x = c.split('>')
        l, r = x[0], x[1]
        l2r[l] = r
        lefts.add(l)
        rights.add(r)

    start = list(lefts - rights)[0]

    result = start
    cur = start
    while True:
        c = l2r.get(cur, None)
        if c is None:
            break
        result += c
        cur = c

    return result


print(findWord(["P>E", "E>R", "R>U"]))  # PERU
print(findWord(["I>N", "A>I", "P>A", "S>P"]))  # SPAIN
print(findWord(["U>N", "G>A", "R>Y", "H>U", "N>G", "A>R"])) # HUNGARY
print(findWord(["I>F", "W>I", "S>W", "F>T"])) # SWIFT
print(findWord(["R>T", "A>L", "P>O", "O>R", "G>A", "T>U", "U>G"])) # PORTUGAL
print(findWord(["W>I", "R>L", "T>Z", "Z>E", "S>W", "E>R", "L>A", "A>N", "N>D", "I>T"])) # SWITZERLAND
