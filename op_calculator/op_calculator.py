# expr ::= int | '(' func expr* ')'
# func ::= '+' | '*' | '$'


# value(int n) = n
# value(( + e0 e1 ... )) = value(e0) + value(e1) + ...
# value(( * e0 e1 ... )) = value(e0) * value(e1) * ...

# value(($ a b)) = expensive(a, b)

# "3"= 3
# "( + 1 2 )"= 3
# "( + 3 4 5 )"= 12
# "( + 7 ( * 8 12 ) ( * 2 ( + 9 4 ) 7 ) 3 )" = + 7 96 (* 2 13 7) 3 =


# ( + 1 2 3 4 ( + 7 12))

# ($ 1 (+ 7 12))
# ($ 1)


from typing import Dict


def value(s: str) -> int:
    if s.isdigit():
        return int(s)
    chars = s.split()
    op = chars[1]
    if op == '+':
        result = 0
    if op == '*':
        result = 1
    i = 2
    while i < len(chars):
        if chars[i].isdigit():
            result = do_op(op, result, chars[i])
            i += 1
            continue

        cum = ''
        total_br = 1
        while total_br:
            cum += chars[i]
            if chars[i] == '(':
                total_br += 1
            if chars[i] == ')':
                total_br -= 1
            i += 1

        result = do_op(op, result, cum)

    return result


cache: Dict[str, int] = {}

def do_dollar_op(*args) -> int:
    return 1

def do_op(op: str, cum: int, line: str) -> int:
    if op == '$':
        if v := cache.get(line):
            return v
        else:
            args = []
            chars = line.split()  # ['(', '$', 'a', '(', '+', ... ]
            i = 2
            while i < len(chars):
                if chars[i].isdigit():
                    args.append(value(chars[i]))
                    i += 1
                    continue

                cum = ''
                total_br = 1
                while total_br:
                    cum += chars[i]
                    if chars[i] == '(':
                        total_br += 1
                    if chars[i] == ')':
                        total_br -= 1
                    i += 1
                args.append(value(cum))
            v = do_dollar_op(*args)
            cache[line] = v
            return v
    v = value(line)
    if op == '+':
        return cum + v
    if op == '*':
        return cum * v
