'''

You’ve found a room in the tomb which has a table. On this table, there are some letters written on stones, and there is a list of words on the wall.

To solve this puzzle you need to arrange the letters to form as many of the given words as possible. You can only use each letter once (and they cannot be reused across words), and you can only form each word once. The letters may be given in any order and not all letters need to be used.

Write a function that returns the words you should form. If there are multiple possible answers, return any valid answer.

Example
words1 = ["list", "of", "wall", "words"]
letters1 = "listofstoneletters"

find_words(words1, letters1)
  => ['list', 'of']
Words can be returned in any order, and not all letters need to be used.

Additional inputs:
words2 = ["and", "do", "like", "for", "us", "of", "part", "can", "have", "view"]
letters2 = "youcanhavepart"
letters3 = "aaacehnoprtuvy"
letters4 = "andcancanforfor"
letters5 = "aabcdeefghiijklmnoopqrstuuvwxyz"

words3 = ["abc", "a", "b", "c"]
letters6 = "abc"

Complexity Variables:
W = number of words in the list of words
L = number of letters in letters

All Test Cases:
finder(words1, letters1) => ["list", "of"]
finder(words2, letters2) => ["can", "have", "part"]
finder(words2, letters3) => ["can", "have", "part"]
finder(words2, letters4) => ["and", "can", "for", "of"]
finder(words2, letters5) => ["can", "do", "like", "of", "part", "us", "view"]
finder(words3, letters6) => ["a", "b", "c"]

'''


words1 = ["list", "of", "wall", "words"]
letters1 = "listofstoneletters"
words2 = ["and", "do", "like", "for", "us", "of", "part", "can", "have", "view"]
letters2 = "youcanhavepart"
letters3 = "aaacehnoprtuvy"
letters4 = "andcancanforfor"
letters5 = "aabcdeefghiijklmnoopqrstuuvwxyz"
words3 = ["abc", "a", "b", "c"]
letters6 = "abc"


def to_dict(word: str) -> dict[str, int]:
    d = {}
    for c in word:
        d.setdefault(c, 0)
        d[c] += 1
    return d


def sub(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
    d: dict[str, int] = {}
    for k, v in d2.items():
        d1[k] -= v
    return d1


def finder2(words: list[str], letters: str) -> list[str]:
    result: list[str] = []
    letter_dict = to_dict(letters)
    for w in sorted(words, key=lambda w: len(w)):
        word_dict = to_dict(w)
        accurate = True
        # print(letter_dict, w)
        for k, v in word_dict.items():
            if k not in letter_dict or letter_dict[k] < v:
                accurate = False
                break
        if not accurate:
            continue
        letter_dict = sub(letter_dict, word_dict)
        result.append(w)
    return result


def finder(words: list[str], letters: str) -> list[str]:
    letter_dict = to_dict(letters)
    return find(words, letter_dict)


def find(words: list[str], letter_dict: dict[str, int]) -> list[str]:
    accurate = False
    while not accurate and len(words):
        word_dict = to_dict(words[0])
        accurate = True
        for k, v in word_dict.items():
            if k not in letter_dict or letter_dict[k] < v:
                accurate = False
                words = words[1:]
                break
    if len(words) == 0:
        return []

    words1 = find(words[1:], sub(letter_dict.copy(), word_dict))
    words1.append(words[0])
    words2 = find(words[1:], letter_dict)

    if len(words1) > len(words2):
        return words1
    return words2


print(finder(words1, letters1))  # => ["list", "of"]
print(finder(words2, letters2))  # => ["can", "have", "part"]
print(finder(words2, letters3))  # => ["can", "have", "part"]
print(finder(words2, letters4))  # => ["and", "can", "for", "of"]
print(finder(words2, letters5))  # => ["can", "do", "like", "of", "part", "us", "view"]
print(finder(words3, letters6))  # => ["a", "b", "c"]


# {
#     "R" => 1
#     "B" => 2
# }

# {
#     "r" => [1,2,3]
#     "b" => [1,2,3]
# }


def distance(room: str) -> int:
    balls: dict[str, int] = {}
    holes: dict[str, int] = {}
    for i, k in enumerate(room):
        if k.upper() == k:
            balls[k] = i
        else:
            holes.setdefault(k, [])
            holes[k].append(i)

    result = 0
    for k, i in balls.items():
        places = holes.get(k.lower(), [])
        r = 0
        for place in places:
            if r == 0 or abs(place - i) < r:
                r = abs(place - i)
        result += r
    return result


print(distance(room1))
print(distance(room2))
print(distance(room3))
print(distance(room4))
print(distance(room5))
