import unittest

from client_python.graph import Location


class MyTestCase(unittest.TestCase):
    l1 = Location.Location(1,2.3545,0)
    l2 = Location.Location(5.215,3,0)
    l3 = Location.Location(1,2,0)
    l4 = Location.Location(0.2315,0.9845,0)
    l5 = Location.Location(1.54848,1.279135,0)

    def test_get_x(self):
        self.assertEqual(self.l1.get_x(), 1)
        self.assertEqual(self.l2.get_x(), 5.215)
        self.assertEqual(self.l3.get_x(), 1)
        self.assertEqual(self.l4.get_x(), 0.2315)
        self.assertEqual(self.l5.get_x(), 1.54848)

    def test_get_y(self):
        self.assertEqual(self.l1.get_y(), 2.3545)
        self.assertEqual(self.l2.get_y(), 3)
        self.assertEqual(self.l3.get_y(), 2)
        self.assertEqual(self.l4.get_y(), 0.9845)
        self.assertEqual(self.l5.get_y(), 01.279135)

    def test_get_z(self):
        # all should be 0
        self.assertEqual(self.l1.get_z(), 0)
        self.assertEqual(self.l2.get_z(), 0)
        self.assertEqual(self.l3.get_z(), 0)
        self.assertEqual(self.l4.get_z(), 0)
        self.assertEqual(self.l5.get_z(), 0)


if __name__ == '__main__':
    runner = unittest.main()
    runner.runTests()
