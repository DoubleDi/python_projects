import copy
import io
import sys
import unittest

from list import List


class TestList(unittest.TestCase):

    def setUp(self):
        self.stdout, self.stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        self.cases = [
            List(value=1, next_=List(value=2, next_=List(value=3))),
            List(value=5, next_=List(value=6)),
            List(value=1),
            List(),
        ]

    def tearDown(self):
        sys.stdout, sys.stderr = self.stdout, self.stderr

    def test_print(self):
        correct = [
            "1\n2\n3\n",
            "5\n6\n",
            "1\n",
            "",
        ]
        for i in range(len(self.cases)):
            with self.subTest(case=i):
                sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
                self.cases[i].print()
                self.assertEqual(sys.stdout.getvalue(), correct[i])
                self.assertEqual(sys.stderr.getvalue(), '')

    def test_print_reversed(self):
        correct = [
            "3\n2\n1\n",
            "6\n5\n",
            "1\n",
            "",
        ]
        for i in range(len(self.cases)):
            with self.subTest(case=i):
                sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
                self.cases[i].print_reversed()
                self.assertEqual(sys.stdout.getvalue(), correct[i])
                self.assertEqual(sys.stderr.getvalue(), '')

    def test_plus(self):
        correct = [
            List(value=1, next_=List(value=2, next_=List(
                value=3, next_=List(value=7)))),
            List(value=5, next_=List(value=6, next_=List(value=7))),
            List(value=1, next_=List(value=7)),
            List(value=7),
        ]
        for i in range(len(self.cases)):
            with self.subTest(case=i):
                l = copy.deepcopy(self.cases[i])
                l += [7]
                self.assertEqual(l._last()._value, correct[i]._last()._value)

    def test_range(self):
        correct = [
            "1\n2\n3\n",
            "5\n6\n",
            "1\n",
            "None\n",
        ]
        for i in range(len(self.cases)):
            with self.subTest(case=i):
                sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
                for l in self.cases[i]:
                    print(l)
                self.assertEqual(sys.stdout.getvalue(), correct[i])
                self.assertEqual(sys.stderr.getvalue(), '')


    def test_append(self):
        correct = [
            List(value=1, next_=List(value=2, next_=List(value=3, next_=List(value=7)))),
            List(value=5, next_=List(value=6, next_=List(value=7))),
            List(value=1, next_=List(value=7)),
            List(value=7),
        ]
        for i in range(len(self.cases)):
            with self.subTest(case=i):
                l = copy.deepcopy(self.cases[i])
                l.append(7)
                self.assertEqual(l._last()._value, correct[i]._last()._value)
