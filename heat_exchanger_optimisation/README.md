# ga_heat_Xchanger_optimisation

## What is it
This python script uses a genetic algorithm to optimise a shell and tube heat exchanger

## How does it work
The core of the optimisaiton process lies in the genetic algorithm it utilises. THis algorithm, works simmilarly to natural selection: it takes an initial population of variables. Then they are cressed between each other - where a small probability of a reandom mutation exists. Afterwards, the resulting offpring is tested against the objjective function. THe fittest ones will be chosen to live on and cross amonst themselves and thus the cycle ocntinues.. Form there, it constantly tests those guesses to see which ones are the fittest. This is done to be able to generate an optimum solution for the design of a shell and tube heat exchanger.

## Requirements
To be able to execute this script, python 3.X will be required. Furtmernore, the following libraries are also needed:
- numpy
- scipy
- math
