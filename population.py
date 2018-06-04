import pysynth
import random
import xlrd
import os
import shutil
import numpy as np
from classes import Chords, Keys


class Population:
    def __init__(self,population_size,nr_of_chords,epochs):
        # Get the parameters
        self.key = Keys().cmajor()
        self.chords = Chords(self.key, 4)
        self.mutation_rate = 0.05 # Chance for every note to switch up or down during mutation
        self.env_pressure = 4 # How many individuals procreate per generation
        self.population_size = population_size
        self.nr_of_chords = nr_of_chords
        self.notes_per_chord = 3
        self.nr_of_notes = self.notes_per_chord * self.nr_of_chords
        self.chord_sequence = self.chords.get_chord_sequence()

        # Create a population and sort them into feasible or infeasible melodies
        population = []
        for i in range(self.population_size):
            population.append(self.melody_from_chords(self.chord_sequence))
        self.feasibles= [x for x in population if self.is_feasible(x)]
        self.infeasibles = [x for x in population if not self.is_feasible(x)]

        # Start the evolution process
        for i in range(0,epochs):
            self.evolve(sexual=True)

        # Print results
        results = self.feasibles + self.infeasibles
        print('Nr of unique melodies = ' + str(len(set(tuple(x) for x in self.feasibles + self.infeasibles))))
        print('Nr of feasible melodies = ' + str(len(self.feasibles)))
        print('Highest fitness: ' + str(np.max([self.fitness(x) for x in results])))
        print('Average fitness: ' + str(np.mean([self.fitness(x) for x in results])))
        print('Standard deviation: ' + str(np.std([self.fitness(x) for x in results])))
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
        # TODO: mutate genome in a gaussian distribution
        output = []
        for i in range(0,len(genome)):
            chance = random.random()
            if 0 < genome[i] < 13:
                if chance < 1 - self.mutation_rate:
                    output.append(genome[i])
                elif chance < 1 - self.mutation_rate/2:
                    output.append(genome[i] - 1)
                else:
                    output.append(genome[i] + 1)
            elif genome[i] == 0:
                if chance < 1 - self.mutation_rate:
                    output.append(genome[i])
                else:
                    output.append(genome[i] + 1)
            elif genome[i] == 13:
                if chance < 1 - self.mutation_rate:
                    output.append(genome[i])
                else:
                    output.append(genome[i] - 1)
        return output

    def reproduce(self, father, mother):
        border = random.randint(1,self.nr_of_notes-1)
        output = father[0:border] + mother[border:self.nr_of_notes]
        return self.mutate(output)

    def evolve(self,sexual):
        # Form new populations out of mutated versions of individuals with the highest fitness
        fi_f = list(reversed(sorted(self.feasibles,key=self.fitness))) # Fittest feasibles
        fi_if = list(reversed(sorted(self.infeasibles, key=self.fitness))) # Fittest infeasibles
        if not sexual:
            # Asexual reproduction
            self.feasibles = [self.mutate(fi_f[i//self.env_pressure]) for i in range(len(self.feasibles))]
            self.infeasibles = [self.mutate(fi_if[i // self.env_pressure]) for i in range(len(self.infeasibles))]
        else:
            # Sexual reproduction
            self.feasibles = [self.reproduce(fi_f[i // self.env_pressure],fi_f[i // self.env_pressure+1]) for i in range(len(self.feasibles))]
            self.infeasibles = [self.reproduce(fi_if[i // self.env_pressure],fi_if[i // self.env_pressure+1]) for i in range(len(self.infeasibles))]

        # Interchange the right individuals between the feasible and infeasible populations
        population = self.feasibles + self.infeasibles
        self.feasibles = [x for x in population if self.is_feasible(x)]
        self.infeasibles = [x for x in population if not self.is_feasible(x)]

    # Taken from MetaCompose paper
    def is_feasible(self, melody):
        output = True
        leaps = [abs(melody[i] - melody[i+1]) for i in range(0, self.nr_of_notes-1)]
        # A melody not have leaps between notes bigger than a fifth (difference of 4)
        if [x for x in leaps if x > 4] is not []:
            output = False
        # A melody should contain at least 0.5 leaps of a second (difference of 1)
        if len([x for x in leaps if x == 1]) > 0.5 * self.nr_of_notes:
            output = False
        # Each note should be different than the preceding one
        if 0 in leaps:
            output = False
        return output

    def fitness(self,melody):
        score = 0
        exact_chords = [self.chords.get_chord(x) for x in self.chord_sequence]
        leaps = [melody[i + 1] - melody[i] for i in range(0, self.nr_of_notes - 1)]
        abs_leaps = [abs(melody[i] - melody[i + 1]) for i in range(0, self.nr_of_notes - 1)]

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
        big_leap_indices = [(i,i+1) for i in range(0,self.nr_of_notes-1)]
        for i in big_leap_indices:
            # Right now the implementation is such that a point is assigned if the first note of the leap belongs to its
            # chord, and the second note belongs to the chord of the first
            if melody[i[0]] in exact_chords[i[0]//self.notes_per_chord] and melody[i[1]] in exact_chords[i[0]//self.notes_per_chord]:
                score += 1/len(leaps)
        s2 = score-s1
        # The first note played on a chord should be part of the chord
        score += 1 * (sum([1 for i in range(self.nr_of_chords) if melody[i*self.notes_per_chord] in exact_chords[i]]) / self.nr_of_chords)
        s3 = score - s2
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
