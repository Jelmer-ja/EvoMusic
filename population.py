import pysynth
import random


class Population:
    def __init__(self,population_size,nr_of_notes):
        self.key = Keys().cmajor()
        self.population_size = population_size
        self.nr_of_notes = nr_of_notes
        population = []
        for i in range(self.population_size):
            population.append(self.random_melody())

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
            melody2 = [(melody[i],rhythm[i]) for i in range(self.nr_of_notes)]
            pysynth.make_wav(melody2, fn="output/" + str(self.feasibles.index(melody)) + ".wav")

#TODO: add more scales
class Keys:
    def cmajor(self):
        return ['c3','d3','e3','f3','g3','a3','b3','c4','d4','e4','f4','g4','a4','b4']

    def dminor(self):
        return['d3','e3','f3','g3','a3','bd3','c4','d4','e4','f4','g4','a4','bd4','c5']