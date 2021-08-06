# Задана строка S из малых латинских букв, требуется узнать длину наибольшей
# подстроки состоящей не более чем из двух различных символов.
# Примеры:
# "ab" -> 2
# "aaa" -> 3
# "abaccab" -> 4
# "baacabb" -> 4


# abaccab
# abaaaccab

# baaabaac 3 {a: 2,b: 2}
# ^      ^
# |      |


def f(s: str) -> int:
    if not len(s):
        return 0
    i = 0
    j = 0
    max_len = -1
    cur_len = 0
    letters = {}
    while j < len(s):
        # уже есть буква
        if s[j] in letters:
            letters[s[j]] += 1
            j += 1
            cur_len += 1
            continue

        # больше 2х букв нужно удалить старую
        if len(letters) >= 2:
            max_len = max(cur_len, max_len)
            letter = s[i]
            count = letters[s[i]]
            diff = 0
            last_letter = s[j - 1]

            while count > 0:
                if s[i] == letter:
                    count -= 1
                letters[s[i]] -= 1
                if letters[s[i]] == 0:
                    letters.pop(s[i])
                i += 1
                diff += 1

            cur_len -= diff

            # возвращаем обратно последнюю уникальную букву
            if last_letter == letter:
                while i > 0 and s[i - 1] == last_letter:
                    i -= 1
                    cur_len += 1
                    letters.setdefault(last_letter, 0)
                    letters[last_letter] += 1

        # добавление новой
        letters[s[j]] = 1
        j += 1
        cur_len += 1

    return max(cur_len, max_len)


# 'abbacccc'
