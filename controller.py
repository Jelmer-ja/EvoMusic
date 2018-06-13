import pysynth
import matplotlib.pyplot as plt
import itertools
import numpy as np
from random import shuffle
# from population import Population
from singlepopulation import Population


# TODO: Decide which version of pysynth to use. Many different instrument-like sounds are possible
def main():
    #pop = Population(population_size=100, nr_of_chords=4, epochs=100)
    #statistics_mutation()
    #statistics_dims()
    #statistics_env()
    #grid_search()
    print_random_list()


def print_random_list():
    # Final order: ['second34', 'full4', 'second35', 'second33', 'full6', 'full3', 'nofit7', 'nofit8', 'full1',
    # 'first31', 'third6', 'first33', 'nofit1', 'full5', 'first37', 'third1', 'third7', 'first32', 'full2', 'first38',
    # 'second36', 'third8', 'second31', 'first35', 'nofit2', 'nofit3', 'third2', 'first36', 'second32', 'full8',
    #  'nofit6', 'second38', 'third3', 'first34', 'nofit5', 'nofit4', 'full7', 'third4', 'second37', 'third5']
    x = ['full' + str(x) for x in range(1,9)]
    x += ['first3' + str(x) for x in range(1,9)]
    x += ['second3' + str(x) for x in range(1, 9)]
    x += ['third' + str(x) for x in range(1, 9)]
    x += ['nofit' + str(x) for x in range(1, 9)]
    shuffle(x)
    print(x)

def grid_search():
    mutation_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
    env_pressures = [2, 3, 4, 5, 10, 15]
    results = []
    hiresults = []

    grid = list(itertools.product(mutation_rates, env_pressures))

    for combination in grid:
        #print('mutation rate: ', combination[0], '   env pressure', combination[1])
        pop = Population(population_size=100, nr_of_chords=4, epochs=100, mutation_rate=combination[0],
                         env_pressure=int(combination[1]))
        avg, highest, std, uniques = pop.get_results()
        #print("Average: ", avg, "highest: ", highest)
        results.append(avg)
        hiresults.append(highest)

    print('\n\nBest combination = ' + str(grid[results.index(np.max(results))]) )
    print('Best combination by highest = ' + str(grid[hiresults.index(np.max(hiresults))]) )



def statistics_mutation():
    mutation_rates = [0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15]
    avgs = []; highs = []; stds = []; uns = []
    for i in range(0, len(mutation_rates)):
        pop = Population(population_size=100, nr_of_chords=4, epochs=100, mutation_rate=mutation_rates[i])
        avg, highest, std, uniques = pop.get_results()
        avgs.append(avg)
        highs.append(highest)
        stds.append(std)
        uns.append(uniques)

    plt.plot(mutation_rates, avgs)
    plt.plot(mutation_rates, highs)
    plt.legend(['Average fitness', 'Highest fitness'])
    plt.xlabel('Mutation rate')
    plt.ylabel('Average score')
    plt.show()

    plt.clf()
    plt.plot(mutation_rates, uns)
    plt.xlabel('Mutation rate')
    plt.ylabel('Nr of unique individual in population')
    plt.show()

    plt.clf()
    plt.plot(mutation_rates, stds)
    plt.xlabel('Mutation rate')
    plt.ylabel('Standard deviation')
    plt.show()


def statistics_dims():
    mutation_dims = [1, 0.99, 0.95, 0.9, 0.8]
    avgs = []; highs = []; stds = []; uns = []
    for i in range(0, len(mutation_rates)):
        pop = Population(population_size=100, nr_of_chords=4, epochs=100, mutation_dim=mutation_dims[i])
        avg, highest, std, uniques = pop.get_results()
        avgs.append(avg)
        highs.append(highest)
        stds.append(std)
        uns.append(uniques)

    plt.plot(mutation_rates, avgs)
    plt.plot(mutation_rates, highs)
    plt.legend(['Average fitness', 'Highest fitness'])
    plt.xlabel('Mutation rate decay')
    plt.ylabel('Average score')
    plt.show()

    plt.clf()
    plt.plot(mutation_rates, uns)
    plt.xlabel('Mutation rate decay')
    plt.ylabel('Nr of unique individual in population')
    plt.show()

    plt.clf()
    plt.plot(mutation_rates, stds)
    plt.xlabel('Mutation rate decay')
    plt.ylabel('Standard deviation')
    plt.show()


def statistics_env():
    env_pressures = [1, 2, 3, 4, 5, 10, 15]
    avgs = []; highs = []; stds = []; uns = []
    for i in range(0, len(mutation_rates)):
        pop = Population(population_size=100, nr_of_chords=4, epochs=100, env_pressure=env_pressures[i])
        avg, highest, std, uniques = pop.get_results()
        avgs.append(avg)
        highs.append(highest)
        stds.append(std)
        uns.append(uniques)

    plt.plot(mutation_rates, avgs)
    plt.plot(mutation_rates, highs)
    plt.legend(['Average fitness', 'Highest fitness'])
    plt.xlabel('Environmental pressure')
    plt.ylabel('Average score')
    plt.show()

    plt.clf()
    plt.plot(mutation_rates, uns)
    plt.xlabel('Environmental pressure')
    plt.ylabel('Nr of unique individual in population')
    plt.show()

    plt.clf()
    plt.plot(mutation_rates, stds)
    plt.xlabel('Environmental pressure')
    plt.ylabel('Standard deviation')
    plt.show()

def test():
    kat = [['bb4', 2], ['a#4', 2], ['a4', 2], ['d4', 1]]
    rue = (('db4', 2), ('f4', 2), ('eb4', 2), ('gb4', 1))
    pysynth.make_wav(kat, fn="test/kat.wav")
    pysynth.make_wav(rue, fn="test/rue.wav")


if __name__ == '__main__':
    main()
