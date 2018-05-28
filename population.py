import pysynth
import random
import xlrd
import xlwt
import xlsxwriter
import numpy as np

class Population:
    def __init__(self,population_size,nr_of_notes):
        self.key = Keys().cmajor()
        self.chords = Chords(self.key,4)
        self.population_size = population_size
        self.nr_of_notes = nr_of_notes
        self.notes_per_chord = 3

        #chordsequence = self.chords.getChordSequence()
        quit()
        population = []
        for i in range(self.population_size):
            population.append()

        self.feasibles= [x for x in population if self.is_feasible(x)]
        self.infeasibles = [x for x in population if not self.is_feasible(x)]

    # TODO: Generate from chord sequence instead of purely random
    def random_melody(self):
        output = [random.choice(range(0,14)) for i in range(self.nr_of_notes)]

    # Taken from MetaCompose paper
    def is_feasible(self, melody):
        output = True
        leaps = [abs(melody[i] - melody[i+1]) for i in range(0,self.nr_of_notes-1)]
        # A melody not  have  leaps between  notes  bigger  than  a  fifth (difference of 4)
        if [x for x in leaps if x > 4] is not []:
            output = False
        # A melody should contain at least 0.5 leaps of a second (difference of 1)
        if len([x for x in leaps if x == 1]) < 0.5 * self.nr_of_notes:
            output = False
        # Each note should be different than the preceding one
        if True in [melody[i] == melody[i+1] for i in range(0,self.nr_of_notes-1)]:
            output = False
        return output

    def export_to_mp3(self):
        # TODO: Add evolving rhythm or random rhythm to create variation in the music
        rhythm = [3 for i in range(self.nr_of_notes)]
        for melody in self.feasibles:
            melody2 = [(melody[i], rhythm[i]) for i in range(self.nr_of_notes)]
            pysynth.make_wav(melody2, fn="output/" + str(self.feasibles.index(melody)) + ".wav")


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
        return [key[i] for i in self.chorddict[name]]

    def get_chord_sequence(self):
        workbook = xlsxwriter.Workbook('chords.xls')
        sheet = workbook.add_worksheet()
        matrix = []
        for row in range(sheet.nrows):
            _row = []
            for col in range(sheet.ncols):
                _row.append(sheet.cell_value(row, col))
            matrix.append(_row)
        print(matrix)


