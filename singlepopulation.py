import pysynth
import random
import xlrd
import os
import shutil
import numpy as np
import statistics
from classes import Chords, Keys


class Population:
    def __init__(self,population_size,nr_of_chords,epochs,mutation_rate=0.05,mutation_dim=1.0,env_pressure=2):
        # Get the parameters
        self.key = Keys().cmajor()
        self.chords = Chords(self.key, 4)
        self.mutation_rate = mutation_rate  # Chance for every note to switch up or down during mutation
        self.mutation_diminution = mutation_dim  # How much of the mutation rate remains each epoch
        self.env_pressure = env_pressure  # What part of the population procreates per generation
        self.population_size = population_size
        self.nr_of_chords = nr_of_chords
        self.notes_per_chord = 4
        self.nr_of_notes = self.notes_per_chord * self.nr_of_chords
        self.chord_sequence = self.chords.get_chord_sequence()

        # Create a population and sort them into feasible or infeasible melodies
        self.population = []
        for i in range(self.population_size):
            self.population.append(self.melody_from_chords(self.chord_sequence))

        # Start the evolution process
        for i in range(0,epochs):
            self.evolve(sexual=True, epoch=i)
            # print(i)

        # Print results
        results = self.population
        self.standard_deviation = len(set(tuple(x) for x in results))
        self.highest_fitness = np.max([self.fitness(x) for x in results])
        self.average_fitness = np.mean([self.fitness(x) for x in results])
        self.nr_of_uniques = np.std([self.fitness(x) for x in results])
        print('Nr of unique melodies = ' + str(self.nr_of_uniques))
        print('Highest fitness: ' + str(self.highest_fitness))
        print('Average fitness: ' + str(self.average_fitness))
        print('Standard deviation: ' + str(self.standard_deviation))
        #self.export_to_mp3()

    def get_results(self):
        return self.average_fitness,self.highest_fitness,self.standard_deviation,self.nr_of_uniques

    def random_melody(self, nr_of_notes):
        output = [random.choice(range(0,14)) for i in range(nr_of_notes)]

    def melody_from_chords(self, chords):
        output = []
        for chord in chords:
            for i in range(self.notes_per_chord):
                output += [random.choice(self.chords.get_chord(chord))]
        return output

    def mutate(self, genome, epoch):
        # TODO: mutate genome in a gaussian distribution
        output = []
        for i in range(0, len(genome)):
            chance = random.random()
            new_mutation = self.mutation_rate * self.mutation_diminution ** epoch
            if 0 < genome[i] < 13:
                if chance < 1 - new_mutation:
                    output.append(genome[i])
                elif chance < 1 - new_mutation/2:
                    output.append(genome[i] - 1)
                else:
                    output.append(genome[i] + 1)
            elif genome[i] == 0:
                if chance < 1 - new_mutation:
                    output.append(genome[i])
                else:
                    output.append(genome[i] + 1)
            elif genome[i] == 13:
                if chance < 1 - new_mutation:
                    output.append(genome[i])
                else:
                    output.append(genome[i] - 1)
        return output

    def reproduce(self, father, mother, epoch):
        border = random.randint(1,self.nr_of_notes-1)
        output = father[0:border] + mother[border:self.nr_of_notes]
        return self.mutate(output, epoch)

    def evolve(self,sexual, epoch):
        # Form new populations out of mutated versions of individuals with the highest fitness
        fi_p = list(reversed(sorted(self.population,key=self.fitness)))  # Individuals sorted by fitness
        if not sexual:
            # Asexual reproduction
            self.population = [self.mutate(fi_p[i//self.env_pressure], epoch) for i in range(len(self.population))]
        else:
            # Sexual reproduction
            self.population = [self.reproduce(fi_p[i // self.env_pressure], fi_p[i // self.env_pressure+1], epoch) for i in range(len(self.population))]

    def fitness(self, melody):
        score = 0
        exact_chords = [self.chords.get_chord(x) for x in self.chord_sequence]
        leaps = [melody[i + 1] - melody[i] for i in range(0, self.nr_of_notes - 1)]
        abs_leaps = [abs(melody[i] - melody[i + 1]) for i in range(0, self.nr_of_notes - 1)]
        median_notes = [int(mode([x[i] for x in self.population]), ) for i in range(0,self.nr_of_notes)]
        scores = [0,0,0,0,0,0,0,0]

        # Original score criteria
        # The melody should approach and follow  big leaps (larger than a second) in a counter step-wise motion
        for i in range(1, len(leaps)-1):
            if abs_leaps[i] > 1:
                if leaps[i] > 0:
                    if leaps[i-1] < 0 and leaps[i+1] < 0:
                        score += 1/len(leaps)
                        scores[0] += 1/(len(leaps)-2)
                if leaps[i] < 0:
                    if leaps[i-1] > 0 and leaps[i+1] > 0:
                        score += 1/len(leaps)
                        scores[0] += 1 / (len(leaps)-2)

        # Where the melody presents big leaps, notes should belong to the underlying chord
        big_leap_indices = [(i,i+1) for i in range(0,self.nr_of_notes-1)]
        for i in big_leap_indices:
            # Right now the implementation is such that a point is assigned if the first note of the leap belongs to its
            # chord, and the second note belongs to the chord of the first
            if melody[i[0]] in exact_chords[i[0]//self.notes_per_chord] and melody[i[1]] in exact_chords[i[0]//self.notes_per_chord]:
                score += 1/len(leaps)
                scores[1] += 1 / len(leaps)

        # The first note played on a chord should be part of the chord
        fn = 1 * (sum([1 for i in range(self.nr_of_chords) if melody[i*self.notes_per_chord] in exact_chords[i]]) / self.nr_of_chords)
        score += fn
        scores[2] += fn

        # Former feasibility criteria converted to score:
        # For every leap larger than a fifth, the score is decreased by 1 / leaps
        llf = 1 * sum([1 for x in abs_leaps if x > 4]) / len(leaps)
        score -= llf
        scores[3] -= llf

        # For every leap of a second, the score is increased by 1 / leaps
        ls = 1 * sum([1 for x in abs_leaps if x == 1]) / len(leaps)
        score += ls
        scores[4] += ls

        # For each note the same as the last one, the score is decreased by 1 / leaps
        sn = 1 * sum([1 for x in leaps if x == 0]) / len(leaps)
        score -= sn
        scores[5] -= sn

        # New custom criteria:
        # Increase the score for every note that is not the same as the average population note
        anti_incest = 3 * sum([1 for i in range(0,self.nr_of_notes) if melody[i] != median_notes[i]]) / self.nr_of_notes
        score += anti_incest
        scores[6] += anti_incest

        #print(scores)
        return score

    def export_to_mp3(self):
        # TODO: Add evolving rhythm or random rhythm to create variation in the music
        # Delete and recreate output folder
        if (os.path.isdir('output/single')):
            shutil.rmtree('output/single')
        try:
            os.makedirs('output/single')
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                raise

        # Write melodies to wav
        self.population = list(reversed(sorted(self.population, key=self.fitness)))  # Sort by fitness
        nr_of_notes = self.notes_per_chord * self.nr_of_chords
        rhythm = [3 for i in range(nr_of_notes)]
        for melody in self.population:
            # Convert melody from numerical notation to string notes
            melody2 = [(self.key[melody[i]], rhythm[i]) for i in range(nr_of_notes)]
            pysynth.make_wav(melody2, fn="output/single/" + str(self.population.index(melody)) + ".wav")


def mode(list):
    return max(set(list), key=list.count)
