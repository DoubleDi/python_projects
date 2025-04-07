import sys
from typing import Optional


class Digit:

    data: int
    next: "Optional[Digit]" = None

    def __init__(self, data: list[str]):
        self.data = int(data[0])
        data = data[1:]
        if data:
            self.next = Digit(data)

    def sum(self, acc: int) -> int:
        if self.data > 0:
            acc += self.data**2
        if self.next:
            acc = self.next.sum(acc)
        return acc


class Line:

    digit: Digit

    def __init__(self, data: str):
        self.digit = Digit(data.split(' '))

    def print(self):
        print(self.digit.sum(0))


class Group:

    line: Line
    next: "Optional[Group]" = None

    def __init__(self, data: list[str]):
        data = data[1:]
        self.line = Line(data[0])
        data = data[1:]
        if data:
            self.next = Group(data)

    def print(self):
        self.line.print()
        if self.next:
            self.next.print()


class Tokenizer:

    group: Optional[Group] = None

    def __init__(self, data: list[str]):
        data = data[1:]
        if data:
            self.group = Group(data)

    def print(self):
        if self.group:
            self.group.print()


def main():
    Tokenizer(sys.stdin.readlines()).print()


if __name__ == "__main__":
    main()
