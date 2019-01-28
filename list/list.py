import copy

class List(object):

    def __init__(self, value=None, next_=None):
        self._value = value
        self._next = next_

    def _last(self):
        head = self
        while head._next is not None:
            head = head._next

        return head

    def print(self):
        # empty list
        if self._value is None:
            return

        print(self._value)
        if self._next is not None:
            self._next.print()

    def append(self, *values):
        head = self._last()

        for v in values:
            head._next = List(value=v)
            head = head._next

    def __add__(self, obj):
        if type(obj) == list:
            last = None
            while len(obj):
                cur = List(value=obj.pop(), next_=last)
                last = cur
            obj = last

        head = self._last()
        head._next = copy.deepcopy(obj)

        return self

    def __iter__(self):
        self._cur = self
        return self

    def __next__(self):
        cur = self._cur
        if cur is None:
            raise StopIteration
        self._cur = self._cur._next
        return cur._value

    def print_reversed(self):
        # empty list
        if self._value is None:
            return

        if self._next is not None:
            self._next.print_reversed()
        print(self._value)

if __name__ == '__main__':
    list_ = List(value=1, next_=List(value=2, next_=List(value=3)))
    list_.print()  # output: 1 2 3
    print("====")
    list_.append(4)
    list_.print()  # output: 1 2 3 4
    print("====")
    tail = List(value=5, next_=List(value=6))
    list_ += tail  # shallow copy, see examples below
    list_.print()  # output: 1 2 3 4 5 6
    print("====")
    tail._value = 0
    tail.print()  # output: 0 6; element 5 in tail is changed
    print("====")
    list_.print()  # output: 1 2 3 4 5 6; element 5 in list_ is NOT changed
    print("====")
    list_ += [7, 8]
    list_.print()  # output: 1 2 3 4 5 6 7 8
    print("====")
    for elem in list_:
        print(2 ** elem)  # output: 2 4 8 16 32 64 128 256
    print("====")
    list_.print_reversed()  # output: 8 7 6 5 4 3 2 1
