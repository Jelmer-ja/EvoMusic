import pysynth
import matplotlib.pyplot as plt
# from population import Population
from singlepopulation import Population


# TODO: Decide which version of pysynth to use. Many different instrument-like sounds are possible
def main():
    mutation_rates = [0.001,0.005,0.01,0.05,0.1,0.15,0.2,0.3,0.5]
    mutation_dims = [1,0.99,0.95,0.9,0.8]
    env_pressures = [1,2,3,4,5,10,15]
    results = []
    for i in range(0,len(mutation_rates)):
        pop = Population(population_size=100, nr_of_chords=4, epochs=100,mutation_rate=mutation_rates[i])
        avg,highest,std,uniques = pop.get_results()
        results.append(avg)

    plt.plot(mutation_rates,results)
    plt.xlabel('Mutation rate')
    plt.ylabel('Average score')
    plt.show()






def test():
    kat = [['bb4', 2], ['a#4', 2], ['a4', 2], ['d4', 1]]
    rue = (('db4', 2), ('f4', 2), ('eb4', 2), ('gb4', 1))
    pysynth.make_wav(kat, fn="test/kat.wav")
    pysynth.make_wav(rue, fn="test/rue.wav")


if __name__ == '__main__':
    main()
