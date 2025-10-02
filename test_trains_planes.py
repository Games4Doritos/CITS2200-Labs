#! /usr/bin/env python3

import unittest

from trains_planes import *

import datetime
from datetime import date
from pathlib import Path


class TestTrainsPlanes(unittest.TestCase):
    def test_example(self):
        trains = [
            (date(2024, 11, 27), 'Paris', 'Stuttgart'),
            (date(2024,  8, 18), 'Dijon', 'Paris'),
            (date(2024,  5,  5), 'Frankfurt', 'Hannover'),
            (date(2024,  9, 11), 'Bordeaux', 'Madrid'),
            (date(2024, 10, 24), 'Milan', 'Zurich'),
            (date(2024,  5, 17), 'Munich', 'Zurich'),
            (date(2024,  2,  5), 'Munich', 'Stuttgart'),
            (date(2024,  3, 31), 'Bordeaux', 'Paris'),
            (date(2024,  2, 13), 'Amsterdam', 'Lille'),
            (date(2024, 11,  2), 'Milan', 'Rome'),
            (date(2024, 10, 19), 'Dijon', 'Zurich'),
            (date(2024,  6, 23), 'Lille', 'Paris'),
            (date(2024,  5,  9), 'Lille', 'London'),
            (date(2024,  8, 18), 'Frankfurt', 'Stuttgart'),
            (date(2024,  7, 28), 'Berlin', 'Hannover'),
            (date(2024, 10, 22), 'Lyon', 'Milan'),
            (date(2024,  5, 22), 'Stuttgart', 'Zurich'),
            (date(2024,  9, 20), 'Dijon', 'Lyon'),
            (date(2024,  3, 18), 'Barcelona', 'Lyon'),
        ]
        planes = [
            ('LH2145', date(2024,  2, 10), 'Stuttgart', 'Munich'),
            ('FR6341', date(2024, 11,  1), 'Barcelona', 'Rome'),
            ('LH1520', date(2024, 10, 19), 'Frankfurt', 'London'),
            ('LH1520', date(2024, 10, 18), 'Frankfurt', 'London'),
            ('BAW427', date(2024,  5, 11), 'Amsterdam', 'London'),
            ('KL1319', date(2024,  9, 12), 'Amsterdam', 'Madrid'),
            ('BAW427', date(2024,  5,  4), 'Amsterdam', 'London'),
            ('LH2309', date(2024,  2, 27), 'Amsterdam', 'Munich'),
        ]
        expected = [
            ('LH2145', date(2024,  2, 10), 'Stuttgart', 'Munich'),
            ('LH1520', date(2024, 10, 19), 'Frankfurt', 'London'),
            ('BAW427', date(2024,  5, 11), 'Amsterdam', 'London'),
            ('KL1319', date(2024,  9, 12), 'Amsterdam', 'Madrid'),
        ]
        expected.sort()
        received = trains_planes(trains, planes)
        received.sort()
        self.assertEqual(received, expected)

    @staticmethod
    def __read_problem(path):
        with open(path) as fp:
            num_trains = int(fp.readline())
            trains = []
            for _ in range(num_trains):
                date, lcity, rcity = fp.readline().strip().split()
                date = datetime.date.fromisoformat(date)
                trains.append((date, lcity, rcity))
            num_planes = int(fp.readline())
            planes = []
            for _ in range(num_planes):
                code, date, depart, arrive = fp.readline().strip().split()
                date = datetime.date.fromisoformat(date)
                planes.append((code, date, depart, arrive))
            num_expected = int(fp.readline())
            expected = []
            for _ in range(num_expected):
                code, date, depart, arrive = fp.readline().strip().split()
                date = datetime.date.fromisoformat(date)
                expected.append((code, date, depart, arrive))
        return trains, planes, expected

    def test_randoms(self):
        cases_dir = Path('testcases_trains_planes')
        for case_file in cases_dir.iterdir():
            trains, planes, expected = self.__read_problem(case_file)
            expected.sort()
            received = trains_planes(trains, planes)
            received.sort()
            msg = f'failed test case {case_file.name}'
            self.assertEqual(received, expected, msg=msg)


if __name__ == '__main__':
    unittest.main()
