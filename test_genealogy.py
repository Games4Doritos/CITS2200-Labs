#! /usr/bin/env python3

import unittest

import genealogy
from genealogy import *

import inspect
import warnings


class TestGenealogy(unittest.TestCase):
    def setUp(self):
        source = inspect.getsource(genealogy)
        redflags = [
            ('import', 'It looks like you are using imports, which is not allowed!'),
        ]
        for redflag, warning in redflags:
            if redflag in source:
                warnings.warn(warning)

    @staticmethod
    def __construct_example():
        genealogy = Genealogy('A')
        genealogy.add_child('A', 'B')
        genealogy.add_child('A', 'C')
        genealogy.add_child('B', 'D')
        genealogy.add_child('B', 'E')
        genealogy.add_child('C', 'F')
        genealogy.add_child('C', 'G')
        genealogy.add_child('D', 'H')
        genealogy.add_child('D', 'I')
        genealogy.add_child('D', 'J')
        genealogy.add_child('F', 'K')
        return genealogy

    def test_get_primogeniture_order_example(self):
        genealogy = self.__construct_example()
        expected = [c for c in 'ABDHIJECFKG']
        self.assertEqual(genealogy.get_primogeniture_order(), expected)

    def test_get_seniority_order_example(self):
        genealogy = self.__construct_example()
        expected = [c for c in 'ABCDEFGHIJK']
        self.assertEqual(genealogy.get_seniority_order(), expected)

    def test_get_cousin_dist_example(self):
        genealogy = self.__construct_example()
        self.assertEqual(genealogy.get_cousin_dist('B', 'C'), (0, 0))
        self.assertEqual(genealogy.get_cousin_dist('D', 'E'), (0, 0))
        self.assertEqual(genealogy.get_cousin_dist('B', 'F'), (0, 1))
        self.assertEqual(genealogy.get_cousin_dist('D', 'F'), (1, 0))
        self.assertEqual(genealogy.get_cousin_dist('B', 'D'), (-1, 1))
        self.assertEqual(genealogy.get_cousin_dist('B', 'J'), (-1, 2))
        self.assertEqual(genealogy.get_cousin_dist('J', 'K'), (2, 0))
        self.assertEqual(genealogy.get_cousin_dist('J', 'F'), (1, 1))
        self.assertEqual(genealogy.get_cousin_dist('D', 'K'), (1, 1))
        self.assertEqual(genealogy.get_cousin_dist('B', 'K'), (0, 2))

    def test_get_primogeniture_order_addition(self):
        genealogy = self.__construct_example()
        genealogy.add_child('I', 'X')
        expected = [c for c in 'ABDHIXJECFKG']
        self.assertEqual(genealogy.get_primogeniture_order(), expected)
        genealogy.add_child('B', 'Y')
        expected = [c for c in 'ABDHIXJEYCFKG']
        self.assertEqual(genealogy.get_primogeniture_order(), expected)
        genealogy.add_child('A', 'Z')
        expected = [c for c in 'ABDHIXJEYCFKGZ']
        self.assertEqual(genealogy.get_primogeniture_order(), expected)

    def test_get_seniority_order_addition(self):
        genealogy = self.__construct_example()
        genealogy.add_child('I', 'X')
        expected = [c for c in 'ABCDEFGHIJKX']
        self.assertEqual(genealogy.get_seniority_order(), expected)
        genealogy.add_child('B', 'Y')
        expected = [c for c in 'ABCDEYFGHIJKX']
        self.assertEqual(genealogy.get_seniority_order(), expected)
        genealogy.add_child('A', 'Z')
        expected = [c for c in 'ABCZDEYFGHIJKX']
        self.assertEqual(genealogy.get_seniority_order(), expected)


if __name__ == '__main__':
    unittest.main()
