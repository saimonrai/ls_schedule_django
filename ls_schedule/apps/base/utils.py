#!/usr/bin/env python
import csv

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2013 Poolsidelabs Inc.'


class CSVFile(object):

    def __init__(self, filename):
        self.grid = []

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                elements = [element for element in row]
                self.grid.append(elements)

    def elements_by_row(self, row_index):
        return [element for element in self.grid[row_index]]

    def elements_by_column(self, column_index):
        elements = []
        for row in self.grid:
            elements.append(row[column_index])
        return elements

    def element(self, row_index, column_index):
        return self.grid[row_index][column_index]
