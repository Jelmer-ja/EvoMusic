import pysynth
import random
import xlrd
import os
import shutil
import numpy as np


class Population:
    def __init__(self,population_size,nr_of_chords,epochs):
        # Get the parameters
        self.key = Keys().cmajor()
        self.chords = Chords(self.key,4)
        self.mutation_rate = 0.2 # Chance for every note to switch up or down during mutation
        self.population_size = population_size
        self.nr_of_chords = nr_of_chords
        self.notes_per_chord = 3
        self.chord_sequence = self.chords.get_chord_sequence()

        # Create a population and sort them into feasible or infeasible melodies
        population = []
        for i in range(self.population_size):
            population.append(self.melody_from_chords(self.chord_sequence))
        self.feasibles= [x for x in population if self.is_feasible(x)]
        self.infeasibles = [x for x in population if not self.is_feasible(x)]

        # Start the evolution process
        for i in range(0,epochs):
            self.evolve()

        self.export_to_mp3()

    def random_melody(self,nr_of_notes):
        output = [random.choice(range(0,14)) for i in range(nr_of_notes)]

    def melody_from_chords(self, chords):
        output = []
        for chord in chords:
            for i in range(self.notes_per_chord):
                output += [random.choice(self.chords.get_chord(chord))]
        return output

    def mutate(self, genome):
        #TODO: mutate genome in a gaussian distribution
        output = []
        chance = random.random()
        for i in range(0,len(genome)):
            if 0 < genome[i] < 13:
                if chance < 0.8:
                    output.append(genome[i])
                elif chance < 0.9:
                    output.append(genome[i] - 1)
                else:
                    output.append(genome[i] + 1)
            elif genome[i] == 0:
                if chance < 0.8:
                    output.append(genome[i])
                else:
                    output.append(genome[i] + 1)
            elif genome[i] == 13:
                if chance < 0.8:
                    output.append(genome[i])
                else:
                    output.append(genome[i] - 1)
        return output

    def evolve(self):
        # Form new populations out of mutated versions of individuals with the highest fitness
        # TODO: sexual reproduction
        fittest_feasibles = sorted(self.feasibles,key=self.fitness)
        self.feasibles = [self.mutate(fittest_feasibles[i//2]) for i in range(len(self.feasibles))]
        fittest_infeasibles = sorted(self.infeasibles, key=self.fitness)
        self.infeasibles = [self.mutate(fittest_infeasibles[i // 2]) for i in range(len(self.infeasibles))]

        # Interchange the right individuals between the feasible and infeasible populations
        population = self.feasibles + self.infeasibles
        self.feasibles = [x for x in population if self.is_feasible(x)]
        self.infeasibles = [x for x in population if not self.is_feasible(x)]

    # Taken from MetaCompose paper
    def is_feasible(self, melody):
        output = True
        nr_of_notes = self.notes_per_chord*self.nr_of_chords
        leaps = [abs(melody[i] - melody[i+1]) for i in range(0, nr_of_notes-1)]
        # A melody not  have  leaps between  notes  bigger  than  a  fifth (difference of 4)
        if [x for x in leaps if x > 4] is not []:
            output = False
        # A melody should contain at least 0.5 leaps of a second (difference of 1)
        if len([x for x in leaps if x == 1]) < 0.5 * nr_of_notes:
            output = False
        # Each note should be different than the preceding one
        if True in [melody[i] == melody[i+1] for i in range(0,nr_of_notes-1)]:
            output = False
        return output

    def fitness(self,melody):
        score = 0
        exact_chords = [self.chords.get_chord(x) for x in self.chord_sequence]
        nr_of_notes = self.notes_per_chord * self.nr_of_chords
        leaps = [melody[i + 1] - melody[i] for i in range(0, nr_of_notes - 1)]
        abs_leaps = [abs(melody[i] - melody[i + 1]) for i in range(0, nr_of_notes - 1)]

        # The melody should approach and follow  big leaps (larger than a second) in a counter step-wise motion
        for i in range(1, len(leaps)-1):
            if abs(leaps[i]) > 1:
                if leaps[i] > 0:
                    if leaps[i-1] == -1 and leaps[i+1] == -1:
                        score += 1/len(leaps)
                if leaps[i] < 0:
                    if leaps[i-1] == 1 and leaps[i+1] == 1:
                        score += 1/len(leaps)
        s1 = score
        # Where the melody presents big leaps, notes should belong to the underlying chord
        big_leap_indices = [(i,i+1) for i in range(0,nr_of_notes-1)]
        for i in big_leap_indices:
            # Right now the implementation is such that a point is assigned if the first note of the leap belongs to its
            # chord, and the second note belongs to the chord of the first
            if melody[i[0]] in exact_chords[i[0]//self.notes_per_chord] and melody[i[1]] in exact_chords[i[0]//self.notes_per_chord]:
                score += 1/len(leaps)
        s2 = score-s1
        # The first note played on a chord should be part of the chord
        score += 1 * (sum([1 for i in range(self.nr_of_chords) if melody[i*self.notes_per_chord] in exact_chords[i]]) / self.nr_of_chords)
        s3 = score - s2
        #print('fitness by individual function: ' + str(s1) + ':' + str(s2) + ':' + str(s3))
        return score

    def export_to_mp3(self):
        # TODO: Add evolving rhythm or random rhythm to create variation in the music
        # Delete and recreate output folder
        if (os.path.isdir('output/feasibles') & os.path.isdir('output/infeasibles')):
            shutil.rmtree('output/feasibles')
            shutil.rmtree('output/infeasibles')
        try:
            os.makedirs('output/feasibles')
            os.makedirs('output/infeasibles')
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                raise

        # Write melodies to wav
        nr_of_notes = self.notes_per_chord * self.nr_of_chords
        rhythm = [3 for i in range(nr_of_notes)]
        for melody in self.feasibles:
            # Convert melody from numerical notation to string notes
            melody2 = [(self.key[melody[i]], rhythm[i]) for i in range(nr_of_notes)]
            pysynth.make_wav(melody2, fn="output/feasibles/" + str(self.feasibles.index(melody)) + ".wav")
        for melody in self.infeasibles:
            # Convert melody from numerical notation to string notes
            melody2 = [(self.key[melody[i]], rhythm[i]) for i in range(nr_of_notes)]
            pysynth.make_wav(melody2, fn="output/infeasibles/" + str(self.infeasibles.index(melody)) + ".wav")


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


