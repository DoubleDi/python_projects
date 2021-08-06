# // Заменить последовательности пробелов в строке на одиночные пробелы
# // normalize("some    string  ") -> "some string "


def normalize(s: str) -> str:
    result = ""
    is_space = False
    for c in s:
        if c == " ":
            is_space = True
            continue
        else:
            if is_space:
                result += " "
                is_space = False
            result += c

    if is_space:
        result += " "
    return result

    # s -> s
    # o -> so
    # m -> som
    # e -> some
    #   -> some
    # s -> some string
