import unittest


class Oset:
    def __init__(self, items=None):
        self.items = {}
        if items:
            for item in items:
                self.add(item)

    def __eq__(self, other):
        return self.items == other.items

    def __repr__(self):
        return f'Oset({[item for item in self.items]})'

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def add(self, item):
        self.items[item] = None

    def get_first(self):
        for item in self.items:
            return item

    def discard(self, item):
        if item in self.items:
            del self.items[item]

    def __iter__(self):
        return self.items.__iter__()


class Test(unittest.TestCase):
    def test1(self):
        s = Oset()
        for i in range(10):
            s.add(i // 2)
        print(s)
        self.assertEqual(s, Oset([0, 1, 2, 3, 4]))
        self.assertEqual(s, Oset([4, 3, 2, 1, 0]))

        for i, item in enumerate(s):
            self.assertEqual(i, item)


if __name__ == '__main__':
    unittest.main()