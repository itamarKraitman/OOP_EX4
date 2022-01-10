import unittest

from client_python.graph import Location, Node


class NodeTest(unittest.TestCase):
    n1 = Node.Node(key=1, position=(1, 3, 0))
    n2 = Node.Node(key=2, position=(2, 4, 0))
    n3 = Node.Node(key=3, position=(1, 5, 0))
    n4 = Node.Node(key=4, position=(3, 2, 0))
    n5 = Node.Node(key=5, position=(0, 3, 0))
    node_list = [n1, n2, n3, n4, n5]

    def test_getKey(self):
        self.assertEqual(self.n1.getKey(), 1)
        self.assertEqual(self.n2.getKey(), 2)
        self.assertEqual(self.n3.getKey(), 3)
        self.assertEqual(self.n4.getKey(), 4)
        self.assertEqual(self.n5.getKey(), 5)

if __name__ == '__main__':
    runner = unittest.main()
    runner.runTests()
