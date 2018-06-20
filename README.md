# EvoMusic

Our evolutionary music generation algorithm can be run through the following steps. 

## Step 1. 
Clone the repository. If you want access to the 40 melodies used in the experiment as well, clone the repository recursively. 
```
git clone --recursive https://github.com/Jelmer-ja/EvoMusic.git. 
```

## Step 2
Open the `controller.py` file and edit the parameters that you want to run the system with. These are specified in the `main()` function at the top of the class. The standard parameters include the population size, number of chords and epochs. 
However, the `Population` class from `population.py` also takes the optional arguments `mutation_rate`, `mutation_dim` and `env_pressure`, which represent the mutation rate, mutation diminition rate per epoch and environmental pressure respectively. 

![alt text](https://i.imgur.com/NasqbJZ.png)

## Step 3 (optional)
Further parameters, including the number of notes per chord and the scale used by the algorithm can be altered in the `__init__()` function of the file `singlepopulation.py`.

![alt text](https://i.imgur.com/HLPAjgz.png)

## Step 4
Run `controller.py`. The algorithm should then run the algorithm and export the population of melodies to .mp3 files in the /output/single folder. 
However, a file is only generated for every unique melody, not for duplicates, so the final number of melodies may be less than 100. 
Besides this, the algorithm should print various statistics about the final population, including the highest and average fitness, the standard deviation for the fitness and the number of unique melodies generated. 

Example command line output:

![alt text](https://i.imgur.com/HLPAjgz.png)

Example output files:

![alt text](https://i.imgur.com/z0t0laz.png)
