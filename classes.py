import pysynth
import random
import xlrd
import os
import shutil
import numpy as np


#TODO: add more scales
class Keys:
    def cmajor(self):
        return ['c3','d3','e3','f3','g3','a3','b3','c4','d4','e4','f4','g4','a4','b4']

    def dminor(self):
        return['d3','e3','f3','g3','a3','bd3','c4','d4','e4','f4','g4','a4','bd4','c5']


class Chords:
    def __init__(self, key, nr_of_chords):
        self.key = key
        self.nr_of_chords = nr_of_chords
        self.chorddict = dict()
        self.name_list = ['I','II','III','IV','V','VI','VII']

        #Define chord degrees
        self.chorddict['I'] = [0,2,4]
        self.chorddict['II'] = [1,3,5]
        self.chorddict['III'] = [2,4,6]
        self.chorddict['IV'] = [3,5,7]
        self.chorddict['V'] = [4,6,8]
        self.chorddict['VI'] = [5,7,9]
        self.chorddict['VII'] = [6,8,10]
        """
        self.chorddict['I7'] = [0, 2, 4,6]
        self.chorddict['II7'] = [1, 3, 5,7]
        self.chorddict['III7'] = [2, 4, 6,8]
        self.chorddict['IV7'] = [3, 5, 7,9]
        self.chorddict['V7'] = [4, 6, 8,10]
        self.chorddict['VI7'] = [5, 7, 9,11]
        self.chorddict['VII7'] = [6, 8, 10,12]
        """

    def get_chord(self,name):
        return self.chorddict[name]

    def get_chord_sequence(self):
        # Get the chord sequence graph from the xls file
        workbook = xlrd.open_workbook("chords.xls")
        sheet = workbook.sheet_by_index(0)
        matrix = []
        for row in range(1,sheet.nrows):
            _row = []
            for col in range(1,sheet.ncols):
                _row.append(sheet.cell_value(row, col))
            matrix.append(_row)

        # Use the probabilities to generate a unique chord sequence
        starting_chord = random.choice(range(0,7))
        output_chords = [starting_chord]
        for i in range(0,self.nr_of_chords-1):
            probabilities = matrix[output_chords[-1]]
            next_chords = [i for i in range(0,7) if probabilities[i] == 1]
            output_chords.append(random.choice(next_chords))

        # Convert chords to string notation and return
        return [self.name_list[i] for i in output_chords]
