import pysynth
# from population import Population
from singlepopulation import Population


# TODO: Decide which version of pysynth to use. Many different instrument-like sounds are possible
def main():
    pop = Population(population_size=30,nr_of_chords=4,epochs=300)


def test():
    kat = [['g4', 2], ['a#4', 2], ['a4', 2], ['d4', 1]]
    rue = (('db4', 2), ('f4', 2), ('eb4', 2), ('gb4', 1))
    pysynth.make_wav(kat, fn="test/kat.wav")
    pysynth.make_wav(rue, fn="test/rue.wav")


if(__name__ == '__main__'):
    main()
