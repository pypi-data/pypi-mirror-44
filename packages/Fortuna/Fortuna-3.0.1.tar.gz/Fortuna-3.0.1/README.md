# Fortuna: Random Value Generator
Fortuna's main goal is to provide a quick and easy way to build custom random generators that don't suck.

The core functionality of Fortuna is based on the RNG Storm engine. While Storm is a high quality random engine, Fortuna is not appropriate for cryptography of any kind. Fortuna is meant for games, data science, A.I. and experimental programming, not security.

Suggested Installation: `$ pip install Fortuna`

Installation on platforms other than MacOS may require building from source files.

 
### Documentation Table of Contents:
- Random Value Generators
    - `TruffleShuffle(Sequence) -> Callable`
    - `QuantumMonty(Sequence) -> Callable`
    - `CumulativeWeightedChoice(Table) -> Callable`
    - `RelativeWeightedChoice(Table) -> Callable`
    - `FlexCat(Matrix) -> Callable`
- Random Integer Functions
    - `randbelow(number: int) -> int`
    - `randint(left_lmit: int, right_limit: int) -> int`
    - `randrange(start: int, stop: int, step: int) -> int`
    - `d(sides: int) -> int`
    - `dice(rolls: int, sides: int) -> int`
    - `plus_or_minus(number: int) -> int`
    - `plus_or_minus_linear(number: int) -> int`
    - `binomial(number_of_trials: int, probability: float) -> int`
    - `negative_binomial(trial_successes: int, probability: float) -> int`
    - `geometric(probability: float) -> int`
    - `poisson(mean: float) -> int`
    - `discrete(count: int, xmin: int, xmax: int) -> int`
- Random Float Functions
    - `random() -> float`
    - `uniform(a: float, b: float) -> float`
    - `expovariate(lambd: float) -> float`
    - `gammavariate(alpha, beta) -> float`
    - `weibullvariate(alpha, beta) -> float`
    - `betavariate(alpha, beta) -> float`
    - `paretovariate(alpha) -> float`
    - `gauss(mu: float, sigma: float) -> float`
    - `normalvariate(mu: float, sigma: float) -> float`
    - `lognormvariate(mu: float, sigma: float) -> float`
    - `vonmisesvariate(mu: float, kappa: float) -> float`
    - `triangular(low: float, high: float, mode: float = None)`
    - `extreme_value(location: float, scale: float) -> float`
    - `chi_squared(degrees_of_freedom: float) -> float`
    - `cauchy(location: float, scale: float) -> float`
    - `fisher_f(degrees_of_freedom_1: float, degrees_of_freedom_2: float) -> float`
    - `student_t(degrees_of_freedom: float) -> float`
- Random Bool Function
    - `percent_true(truth_factor: float) -> bool`
- Random Shuffle Functions
    - `shuffle(array: list) -> None`
    - `knuth(array: list) -> None`
    - `fisher_yates(array: list) -> None`
- Test Suite Functions
    - `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - `quick_test()`
- Test Suite Output
    - Distributions and performance data from the most recent build.
- Development Log
- Legal Information


##### Project Definitions:
- Integer: 64 bit signed long long int.
    - Input & Output Range: `(-2**63, 2**63)` or approximately +/- 9.2 billion billion.
    - Minimum: -9223372036854775807
    - Maximum:  9223372036854775807
- Float: 64 bit double precision real number.
    - Minimum: -1.7976931348623157e+308
    - Maximum:  1.7976931348623157e+308
    - Epsilon Below Zero: -5e-324
    - Epsilon Above Zero:  5e-324
- Value: Any python object that can be put inside a list: str, int, and lambda to name a few. Almost anything.
- Callable: Any function, method or lambda.
- Sequence: Any object that can be converted into a list.
    - List, Tuple, Set, etc...
    - Comprehensions and Generators that produce Sequences also qualify.
- Array: List or tuple.
    - Must be indexed like a list.
    - List comprehensions are ok, but sets and generators are not indexed.
    - All arrays are sequences but not all sequences are arrays.
    - Classes that wrap a list will take any Sequence or Array and copy it or convert it as needed.
    - Functions that operate on a list will require an Array.
- Pair: Sequence of two values.
- Table: Sequence of Pairs.
    - List of lists of two values each.
    - Tuple of tuples of two values each.
    - Generators that produce Tables also qualify.
    - The result of zip(list_1, list_2) also qualifies.
- Matrix: Dictionary of Sequences.
    - Generators that produce Matrices also qualify.


## Random Value Classes
### TruffleShuffle
`TruffleShuffle(list_of_values: Sequence) -> callable`
- The input Sequence can be any list like object (list, set, tuple or generator).
- The input Sequence must not be empty. Values can be any python object.
- The returned callable produces a random value from the list with a wide uniform distribution.

#### TruffleShuffle, Basic Use Case
```python
from Fortuna import TruffleShuffle


list_of_values = [1, 2, 3, 4, 5, 6]

truffle_shuffle = TruffleShuffle(list_of_values)

print(truffle_shuffle())  # prints a random value from the list_of_values.
```

**Wide Uniform Sequence**: *"Wide"* refers to the average distance between consecutive occurrences of the same item in the output sequence. The goal of this type of distribution is to keep the output sequence free of clumps while maintaining randomness and the uniform probability of each value.

This is not the same as a *flat uniform distribution*. The two distributions will be statistically similar, but the output sequences are very different. For a more general solution that offers several statistical distributions, please refer to QuantumMonty. For a more custom solution featuring discrete rarity refer to RelativeWeightedChoice and its counterpart CumulativeWeightedChoice.

**Micro-shuffle**: This is the hallmark of TruffleShuffle and how it creates a wide uniform distribution efficiently. While adjacent duplicates are forbidden, nearly consecutive occurrences of the same item are also required to be extremely rare with respect to the size of the set. This gives rise to output sequences that seem less mechanical than other random sequences. Somehow more and less random at the same time, almost human-like?

**Automatic Flattening**: TruffleShuffle and all higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error. A callable object can be any class, function, method or lambda. Mixing callable objects with un-callable objects is fully supported. Nested callable objects are fully supported. It's lambda all the way down.

To disable automatic flattening, pass the optional argument flat=False during instantiation.

Please review the code examples of each section. If higher-order functions and lambdas make your head spin, concentrate only on the first example of each section. Because `lambda(lambda) -> lambda` fixes everything for arbitrary values of 'because', 'fixes' and 'everything'.


#### Flattening
```python
from Fortuna import TruffleShuffle


flatted = TruffleShuffle([lambda: 1, lambda: 2])
print(flatted())  # will print the value 1 or 2

un_flat = TruffleShuffle([lambda: 1, lambda: 2], flat=False)
print(un_flat()())  # will print the value 1 or 2, mind the double-double parenthesis

auto_un_flat = TruffleShuffle([lambda x: x, lambda x: x + 1])
# flat=False is not required here because the lambdas can't be called without input x satisfied.
print(auto_un_flat()(1))  # will print the value 1 or 2, mind the double-double parenthesis

```


#### Mixing Static Objects with Callable Objects
```python
from Fortuna import TruffleShuffle


mixed_flat = TruffleShuffle([1, lambda: 2])
print(mixed_flat())  # will print 1 or 2

mixed_un_flat = TruffleShuffle([1, lambda: 2], flat=False) # not recommended.
print(mixed_flat())  # will print 1 or <lambda at some_address>
# This pattern is not recommended because you wont know the nature of what you get back.
# This is almost always not what you want, and always messy.
```


##### Dynamic Strings
To successfully express a dynamic string, at least one level of indirection is required.
Without an indirection the f-string would collapse into a static string too soon.

WARNING: The following example features a higher order function that takes a tuple of lambdas and returns a higher order function that returns a random lambda that returns a dynamic f-string.

```python
from Fortuna import TruffleShuffle, d


# d is a simple dice function.
brainiac = TruffleShuffle((
    lambda: f"A{d(2)}",
    lambda: f"B{d(4)}",
    lambda: f"C{d(6)}",
))

print(brainiac())  # prints a random dynamic string.
```


### QuantumMonty
`QuantumMonty(some_list: Sequence) -> callable`
- The input Sequence can be any list like object (list, set, tuple or generator).
- The input Sequence must not be empty. Values can be any python object.
- The returned callable will produce random values from the list using the selected distribution model or "monty".
- The default monty is the Quantum Monty Algorithm.

```python
from Fortuna import QuantumMonty


list_of_values = [1, 2, 3, 4, 5, 6]
quantum_monty = QuantumMonty(list_of_values)

print(quantum_monty())          # prints a random value from the list_of_values.
                                # uses the default Quantum Monty Algorithm.

print(quantum_monty.uniform())  # prints a random value from the list_of_values.
                                # uses the "uniform" monty: a flat uniform distribution.
                                # equivalent to random.choice(list_of_values) but better.
```
The QuantumMonty class represents a diverse collection of strategies for producing random values from a sequence where the output distribution is based on the method you choose. Generally speaking, each value in the sequence will have a probability that is based on its position in the sequence. For example: the "front" monty produces random values where the beginning of the sequence is geometrically more common than the back. Given enough samples the "front" monty will always converge to a 45 degree slope down for any list of unique values.

There are three primary method families: geometric, gaussian, and poisson. Each family has three base methods; 'front', 'middle', 'back', plus a 'quantum' method that incorporates all three base methods. The quantum algorithms for each family produce distributions by overlapping the probability waves of the other methods in their family. The Quantum Monty Algorithm incorporates all nine base methods.

In addition to the thirteen positional methods that are core to QuantumMonty, it also implements a uniform distribution as a simple base case.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.

```python
import Fortuna


quantum_monty = Fortuna.QuantumMonty(
    ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
)

""" Each of the following methods will return a random value from the sequence.
Each method has its own unique distribution model for the same data set. """

""" Flat Base Case """
quantum_monty.uniform()             # Flat Uniform Distribution

""" Geometric Positional """
quantum_monty.front()               # Geometric Descending, Triangle
quantum_monty.middle()              # Geometric Median Peak, Equilateral Triangle
quantum_monty.back()                # Geometric Ascending, Triangle
quantum_monty.quantum()             # Geometric Overlay, Saw Tooth

""" Gaussian Positional """
quantum_monty.front_gauss()         # Exponential Gamma
quantum_monty.middle_gauss()        # Scaled Gaussian
quantum_monty.back_gauss()          # Reversed Gamma
quantum_monty.quantum_gauss()       # Gaussian Overlay

""" Poisson Positional """
quantum_monty.front_poisson()       # 1/3 Mean Poisson
quantum_monty.middle_poisson()      # 1/2 Mean Poisson
quantum_monty.back_poisson()        # 2/3 Mean Poisson
quantum_monty.quantum_poisson()     # Poisson Overlay

""" Quantum Monty Algorithm """
quantum_monty.quantum_monty()       # Quantum Monty Algorithm

```

### Weighted Choice: Custom Rarity
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values.

Flatten: Both will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must contain a weight and a value.
- Weights must be positive integers.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some fraction of the length of the sequence.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.

The following examples produce equivalent distributions with comparable performance.
The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

#### Cumulative Weight Strategy
`CumulativeWeightedChoice(weighted_table: Table) -> callable`

_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice


cum_weighted_choice = CumulativeWeightedChoice([
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),  # same as rel weight 4 because 30 - 26 = 4
])

print(cum_weighted_choice())  # prints a weighted random value
```

#### Relative Weight Strategy
`RelativeWeightedChoice(weighted_table: Table) -> callable`

```python
from Fortuna import RelativeWeightedChoice


population = ["Apple", "Banana", "Cherry", "Grape", "Lime", "Orange"]
rel_weights = [7, 4, 2, 10, 3, 4]  # Alternate zip setup.
rel_weighted_choice = RelativeWeightedChoice(zip(rel_weights, population))

print(rel_weighted_choice())  # prints a weighted random value
```

### FlexCat
`FlexCat(dict_of_lists: Matrix) -> callable`

FlexCat is a 2d QuantumMonty.

Rather than taking a sequence, FlexCat takes a Matrix: a dictionary of sequences. When the the instance is called it returns a random value from a random sequence.

The constructor takes two optional keyword arguments to specify the algorithms to be used to make random selections. The algorithm specified for selecting a key need not be the same as the one for selecting values. An optional key may be provided at call time to bypass the random key selection and select a random value from that category. Keys passed in this way must match a key in the Matrix.

By default, FlexCat will use key_bias="front" and val_bias="truffle_shuffle", this will make the top of the data structure geometrically more common than the bottom and it will truffle shuffle the sequence values. This config is known as Top Cat, it produces a descending-step distribution. Many other combinations are available.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.


Algorithm Options: _See QuantumMonty & TruffleShuffle for more details._
- 'front', Geometric Descending
- 'middle', Geometric Median Peak
- 'back', Geometric Ascending
- 'quantum', Geometric Overlay
- 'front_gauss', Exponential Gamma
- 'middle_gauss', Scaled Gaussian
- 'back_gauss', Reversed Gamma
- 'quantum_gauss', Gaussian Overlay
- 'front_poisson', 1/3 Mean Poisson
- 'middle_poisson', 1/2 Mean Poisson
- 'back_poisson', 2/3 Mean Poisson
- 'quantum_poisson', Poisson Overlay
- 'quantum_monty', Quantum Monty Algorithm
- 'uniform', uniform flat distribution
- 'truffle_shuffle', TruffleShuffle, wide uniform distribution


```python
from Fortuna import FlexCat

matrix_data = {
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}
flex_cat = FlexCat(matrix_data, key_bias="front", val_bias="back")

flex_cat()          # returns a random "back" value from a random "front" category
flex_cat("Cat_B")   # returns a random "back" value specifically from "Cat_B"
```

## Fortuna Functions
### Random Numbers
- `Fortuna.randbelow(number: int) -> int`
    - Returns a random integer in the exclusive range:
        - [0, number) for positive values.
        - (number, 0] for negative values.
        - Always returns zero when the input is zero
    - Flat uniform distribution.


- `Fortuna.randint(left_limit: int, right_limit: int) -> int`
    - Fault-tolerant, efficient version of random.randint()
    - Returns a random integer in the range [left_limit, right_limit]
    - `randint(1, 10) -> [1, 10]`
    - `randint(10, 1) -> [1, 10]` same as above.
    - Flat uniform distribution.


- `Fortuna.randrange(start: int, stop: int = 0, step: int = 1) -> int`
    - Fault-tolerant, efficient version of random.randrange()
    - Returns a random integer in the range [A, B) by increments of C.
    - `randrange(2, 11, 2) -> [2, 10] by 2` even numbers from 2 to 10.
    - `randrange(10, 1, 0) -> [10]` a step size or range size of zero always returns the first parameter.
    - Flat uniform distribution.


- `Fortuna.d(sides: int) -> int`
    - Represents a single die roll of a given size die.
    - Returns a random integer in the range [1, sides].
    - Flat uniform distribution.


- `Fortuna.dice(rolls: int, sides: int) -> int`
    - Returns a random integer in range [X, Y] where X = rolls and Y = rolls * sides.
    - The return value represents the sum of multiple rolls of the same size die.
    - Geometric distribution based on the number and size of the dice rolled.
    - Complexity scales primarily with the number of rolls, not the size of the dice.


- `Fortuna.plus_or_minus(number: int) -> int`
    - Returns a random integer in range [-number, number].
    - Flat uniform distribution.


- `Fortuna.plus_or_minus_linear(number: int) -> int`
    - Returns a random integer in range [-number, number].
    - Linear geometric, triangle distribution.


- `binomial(number_of_trials: int, probability: float) -> int`
- `negative_binomial(trial_successes: int, probability: float) -> int`
- `geometric(probability: float) -> int`
- `poisson(mean: float) -> int`
- `discrete(count: int, xmin: int, xmax: int) -> int`

### Random Float Functions
- `random() -> float`
- `uniform(a: float, b: float) -> float`
- `expovariate(lambd: float) -> float`
- `gammavariate(alpha, beta) -> float`
- `weibullvariate(alpha, beta) -> float`
- `betavariate(alpha, beta) -> float`
- `paretovariate(alpha) -> float`
- `gauss(mu: float, sigma: float) -> float`
- `normalvariate(mu: float, sigma: float) -> float`
- `lognormvariate(mu: float, sigma: float) -> float`
- `vonmisesvariate(mu: float, kappa: float) -> float`
- `triangular(low: float, high: float, mode: float = None)`
- `extreme_value(location: float, scale: float) -> float`
- `chi_squared(degrees_of_freedom: float) -> float`
- `cauchy(location: float, scale: float) -> float`
- `fisher_f(degrees_of_freedom_1: float, degrees_of_freedom_2: float) -> float`
- `student_t(degrees_of_freedom: float) -> float`

### Random Truth
- `Fortuna.percent_true(truth_factor: float = 50.0) -> bool`
    - Always returns False if num is 0.0 or less
    - Always returns True if num is 100.0 or more.
    - Produces True or False based truth_factor: the probability of True as a percentage.

### Random Shuffle Functions
- `shuffle(array: list) -> None`
- `knuth(array: list) -> None`
- `fisher_yates(array: list) -> None`

### Test Suite Functions
- `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
- `quick_test()`


## Fortuna Distribution and Performance Test Suite
```
Fortuna Test Suite: RNG Storm Engine

TruffleShuffle
Output Analysis: TruffleShuffle([4, 8, 5, 3, 7, 9, 6, 2, 0, 1], flat=True)()
Approximate Single Execution Time: Min: 500ns, Mid: 531ns, Max: 968ns
Raw Samples: 8, 9, 2, 0, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4939
 Std Deviation: 2.8811096593651078
Sample Distribution:
 0: 9.98%
 1: 10.19%
 2: 9.84%
 3: 10.27%
 4: 10.17%
 5: 9.71%
 6: 9.92%
 7: 9.93%
 8: 9.46%
 9: 10.53%


QuantumMonty([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Output Distribution: QuantumMonty.uniform()
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 781ns
Raw Samples: 6, 6, 6, 1, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4613
 Std Deviation: 2.8578171778303436
Sample Distribution:
 0: 9.89%
 1: 10.39%
 2: 10.11%
 3: 10.13%
 4: 9.8%
 5: 10.28%
 6: 10.25%
 7: 9.72%
 8: 9.88%
 9: 9.55%

Output Distribution: QuantumMonty.front()
Approximate Single Execution Time: Min: 218ns, Mid: 281ns, Max: 687ns
Raw Samples: 1, 2, 0, 2, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9602
 Std Deviation: 2.455813319840535
Sample Distribution:
 0: 18.81%
 1: 16.63%
 2: 14.32%
 3: 13.04%
 4: 10.45%
 5: 8.98%
 6: 6.92%
 7: 5.23%
 8: 3.78%
 9: 1.84%

Output Distribution: QuantumMonty.back()
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 1687ns
Raw Samples: 9, 9, 8, 5, 8
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 6
 Maximum: 9
 Mean: 5.9674
 Std Deviation: 2.454045532166711
Sample Distribution:
 0: 1.73%
 1: 3.55%
 2: 5.9%
 3: 7.53%
 4: 9.26%
 5: 10.98%
 6: 12.7%
 7: 14.18%
 8: 16.13%
 9: 18.04%

Output Distribution: QuantumMonty.middle()
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 500ns
Raw Samples: 3, 1, 8, 6, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5167
 Std Deviation: 2.2352227477531645
Sample Distribution:
 0: 3.45%
 1: 6.82%
 2: 9.66%
 3: 13.18%
 4: 16.42%
 5: 16.8%
 6: 13.31%
 7: 9.97%
 8: 6.85%
 9: 3.54%

Output Distribution: QuantumMonty.quantum()
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 406ns
Raw Samples: 1, 4, 7, 1, 6
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4953
 Std Deviation: 2.6706349692748934
Sample Distribution:
 0: 7.69%
 1: 8.93%
 2: 10.17%
 3: 11.12%
 4: 12.4%
 5: 11.98%
 6: 10.79%
 7: 10.46%
 8: 8.7%
 9: 7.76%

Output Distribution: QuantumMonty.front_gauss()
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 593ns
Raw Samples: 0, 1, 0, 0, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 0
 Maximum: 9
 Mean: 0.5692
 Std Deviation: 0.9363220759455532
Sample Distribution:
 0: 63.66%
 1: 23.09%
 2: 8.48%
 3: 2.96%
 4: 1.31%
 5: 0.32%
 6: 0.13%
 7: 0.04%
 9: 0.01%

Output Distribution: QuantumMonty.back_gauss()
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 562ns
Raw Samples: 7, 9, 9, 9, 8
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 9
 Maximum: 9
 Mean: 8.4082
 Std Deviation: 0.9682285405061477
Sample Distribution:
 1: 0.01%
 2: 0.09%
 3: 0.17%
 4: 0.43%
 5: 1.25%
 6: 3.2%
 7: 8.67%
 8: 23.36%
 9: 62.82%

Output Distribution: QuantumMonty.middle_gauss()
Approximate Single Execution Time: Min: 218ns, Mid: 218ns, Max: 406ns
Raw Samples: 3, 5, 3, 5, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 4
 Maximum: 8
 Mean: 4.4935
 Std Deviation: 1.0363711480524975
Sample Distribution:
 1: 0.06%
 2: 2.14%
 3: 13.92%
 4: 34.14%
 5: 34.13%
 6: 13.36%
 7: 2.12%
 8: 0.13%

Output Distribution: QuantumMonty.quantum_gauss()
Approximate Single Execution Time: Min: 187ns, Mid: 218ns, Max: 437ns
Raw Samples: 3, 7, 2, 9, 9
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4704
 Std Deviation: 3.340005898788263
Sample Distribution:
 0: 21.04%
 1: 8.05%
 2: 3.49%
 3: 6.02%
 4: 11.86%
 5: 12.05%
 6: 5.41%
 7: 3.55%
 8: 7.82%
 9: 20.71%

Output Distribution: QuantumMonty.front_poisson()
Approximate Single Execution Time: Min: 218ns, Mid: 218ns, Max: 531ns
Raw Samples: 4, 3, 5, 2, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.1679
 Std Deviation: 1.7724626236892098
Sample Distribution:
 0: 4.26%
 1: 13.36%
 2: 20.74%
 3: 22.61%
 4: 17.65%
 5: 11.18%
 6: 5.92%
 7: 2.66%
 8: 1.1%
 9: 0.52%

Output Distribution: QuantumMonty.back_poisson()
Approximate Single Execution Time: Min: 218ns, Mid: 234ns, Max: 593ns
Raw Samples: 9, 7, 6, 8, 7
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 6
 Maximum: 9
 Mean: 5.8111
 Std Deviation: 1.768708461833746
Sample Distribution:
 0: 0.35%
 1: 1.11%
 2: 2.94%
 3: 6.28%
 4: 11.06%
 5: 18.05%
 6: 21.94%
 7: 21.07%
 8: 13.14%
 9: 4.06%

Output Distribution: QuantumMonty.middle_poisson()
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 406ns
Raw Samples: 3, 1, 6, 4, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5042
 Std Deviation: 2.2023776712318606
Sample Distribution:
 0: 2.09%
 1: 7.29%
 2: 11.68%
 3: 14.36%
 4: 14.68%
 5: 14.57%
 6: 14.18%
 7: 11.52%
 8: 7.27%
 9: 2.36%

Output Distribution: QuantumMonty.quantum_poisson()
Approximate Single Execution Time: Min: 281ns, Mid: 312ns, Max: 500ns
Raw Samples: 7, 5, 3, 6, 6
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5288
 Std Deviation: 2.222670597830152
Sample Distribution:
 0: 2.4%
 1: 6.96%
 2: 11.8%
 3: 13.94%
 4: 14.37%
 5: 14.69%
 6: 13.53%
 7: 12.4%
 8: 7.6%
 9: 2.31%

Output Distribution: QuantumMonty.quantum_monty()
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 1781ns
Raw Samples: 6, 4, 5, 5, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.502
 Std Deviation: 2.7757821414242265
Sample Distribution:
 0: 10.33%
 1: 7.72%
 2: 8.36%
 3: 10.59%
 4: 13.46%
 5: 12.71%
 6: 10.05%
 7: 8.45%
 8: 7.82%
 9: 10.51%


Weighted Choice
Base Case
Output Distribution: Random.choices([36, 30, 24, 18], cum_weights=[1, 10, 100, 1000])
Approximate Single Execution Time: Min: 2000ns, Mid: 2000ns, Max: 3312ns
Raw Samples: [18], [18], [18], [18], [18]
Test Samples: 10000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6168
 Std Deviation: 2.0244425397525303
Sample Distribution:
 18: 90.7%
 24: 8.42%
 30: 0.78%
 36: 0.1%

Output Analysis: CumulativeWeightedChoice([(1, 36), (10, 30), (100, 24), (1000, 18)], flat=True)()
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 750ns
Raw Samples: 18, 18, 24, 18, 18
Test Samples: 10000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6636
 Std Deviation: 2.1006847282809393
Sample Distribution:
 18: 90.0%
 24: 9.09%
 30: 0.76%
 36: 0.15%

Functional
Output Distribution: cumulative_weighted_choice([(1, 36), (10, 30), (100, 24), (1000, 18)])
Approximate Single Execution Time: Min: 187ns, Mid: 187ns, Max: 312ns
Raw Samples: 18, 18, 18, 18, 18
Test Samples: 10000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6486
 Std Deviation: 2.061296420773448
Sample Distribution:
 18: 90.2%
 24: 8.86%
 30: 0.87%
 36: 0.07%

Base Case
Output Distribution: Random.choices([36, 30, 24, 18], weights=[1, 9, 90, 900])
Approximate Single Execution Time: Min: 2093ns, Mid: 2125ns, Max: 5968ns
Raw Samples: [18], [18], [18], [18], [18]
Test Samples: 10000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6654
 Std Deviation: 2.1163389920031497
Sample Distribution:
 18: 90.08%
 24: 8.87%
 30: 0.93%
 36: 0.12%

Output Analysis: RelativeWeightedChoice([(1, 36), (9, 30), (90, 24), (900, 18)], flat=True)()
Approximate Single Execution Time: Min: 281ns, Mid: 312ns, Max: 1781ns
Raw Samples: 18, 18, 18, 18, 18
Test Samples: 10000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6396
 Std Deviation: 2.0806116250933155
Sample Distribution:
 18: 90.46%
 24: 8.55%
 30: 0.86%
 36: 0.13%


FlexCat
Output Analysis: FlexCat({1: [1, 2, 3], 2: [10, 20, 30], 3: [100, 200, 300]}, key_bias='front', val_bias='truffle_shuffle', flat=True)()
Approximate Single Execution Time: Min: 718ns, Mid: 781ns, Max: 1531ns
Raw Samples: 20, 30, 20, 30, 200
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 3
 Maximum: 300
 Mean: 41.5825
 Std Deviation: 79.82512510989181
Sample Distribution:
 1: 16.7%
 2: 16.74%
 3: 16.79%
 10: 11.13%
 20: 10.89%
 30: 10.72%
 100: 5.65%
 200: 5.72%
 300: 5.66%


Random Integers
Base Case
Output Distribution: Random.randrange(10)
Approximate Single Execution Time: Min: 812ns, Mid: 875ns, Max: 1218ns
Raw Samples: 5, 8, 4, 2, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5357
 Std Deviation: 2.852076251416569
Sample Distribution:
 0: 9.82%
 1: 9.65%
 2: 9.36%
 3: 10.46%
 4: 9.82%
 5: 10.72%
 6: 9.92%
 7: 10.5%
 8: 9.83%
 9: 9.92%

Output Distribution: randbelow(10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 93ns
Raw Samples: 5, 1, 8, 5, 8
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4839
 Std Deviation: 2.8594332350734444
Sample Distribution:
 0: 9.88%
 1: 9.99%
 2: 10.18%
 3: 10.18%
 4: 10.13%
 5: 9.75%
 6: 10.36%
 7: 9.97%
 8: 9.76%
 9: 9.8%

Base Case
Output Distribution: Random.randint(-5, 5)
Approximate Single Execution Time: Min: 1125ns, Mid: 1156ns, Max: 1437ns
Raw Samples: -5, 4, -4, -3, -3
Test Samples: 10000
Sample Statistics:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0156
 Std Deviation: 3.1433333731040123
Sample Distribution:
 -5: 8.68%
 -4: 9.38%
 -3: 8.8%
 -2: 9.13%
 -1: 8.92%
 0: 9.3%
 1: 9.52%
 2: 9.18%
 3: 9.1%
 4: 9.07%
 5: 8.92%

Output Distribution: randint(-5, 5)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 656ns
Raw Samples: 1, -1, -5, -1, 2
Test Samples: 10000
Sample Statistics:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0123
 Std Deviation: 3.151466624317703
Sample Distribution:
 -5: 8.51%
 -4: 9.37%
 -3: 9.49%
 -2: 9.16%
 -1: 8.9%
 0: 8.58%
 1: 9.36%
 2: 9.28%
 3: 9.36%
 4: 9.0%
 5: 8.99%

Base Case
Output Distribution: Random.randrange(1, 21, 2)
Approximate Single Execution Time: Min: 1250ns, Mid: 1312ns, Max: 3281ns
Raw Samples: 1, 1, 11, 19, 9
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 11
 Maximum: 19
 Mean: 10.068
 Std Deviation: 5.756482407596752
Sample Distribution:
 1: 9.8%
 3: 10.04%
 5: 9.86%
 7: 9.96%
 9: 9.86%
 11: 9.87%
 13: 9.84%
 15: 10.41%
 17: 10.18%
 19: 10.18%

Output Distribution: randrange(1, 21, 2)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 5, 3, 19, 3, 15
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 9.8712
 Std Deviation: 5.711415987936681
Sample Distribution:
 1: 9.97%
 3: 10.31%
 5: 10.39%
 7: 10.06%
 9: 10.53%
 11: 10.14%
 13: 9.61%
 15: 9.52%
 17: 10.06%
 19: 9.41%

Output Distribution: d(10)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 312ns
Raw Samples: 6, 2, 5, 6, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4737
 Std Deviation: 2.8614204659064475
Sample Distribution:
 1: 10.18%
 2: 9.88%
 3: 10.27%
 4: 9.9%
 5: 9.82%
 6: 10.23%
 7: 10.13%
 8: 10.14%
 9: 9.99%
 10: 9.46%

Output Distribution: dice(2, 6)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 5, 9, 5, 5, 7
Test Samples: 10000
Sample Statistics:
 Minimum: 2
 Median: 7
 Maximum: 12
 Mean: 6.9742
 Std Deviation: 2.4020223419304645
Sample Distribution:
 2: 2.87%
 3: 5.57%
 4: 8.5%
 5: 10.72%
 6: 14.18%
 7: 16.79%
 8: 14.15%
 9: 11.3%
 10: 7.91%
 11: 5.36%
 12: 2.65%

Output Distribution: plus_or_minus(5)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 93ns
Raw Samples: 4, -1, 0, 2, 1
Test Samples: 10000
Sample Statistics:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0055
 Std Deviation: 3.184820883253223
Sample Distribution:
 -5: 9.49%
 -4: 8.91%
 -3: 9.13%
 -2: 8.83%
 -1: 9.46%
 0: 9.12%
 1: 8.6%
 2: 9.01%
 3: 8.97%
 4: 8.88%
 5: 9.6%

Output Distribution: binomial(4, 0.5)
Approximate Single Execution Time: Min: 156ns, Mid: 156ns, Max: 906ns
Raw Samples: 3, 3, 1, 2, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 2
 Maximum: 4
 Mean: 1.9939
 Std Deviation: 1.014970840261265
Sample Distribution:
 0: 6.46%
 1: 25.89%
 2: 35.99%
 3: 25.12%
 4: 6.54%

Output Distribution: negative_binomial(5, 0.75)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 812ns
Raw Samples: 1, 1, 2, 2, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 1
 Maximum: 13
 Mean: 1.6736
 Std Deviation: 1.5198993550248452
Sample Distribution:
 0: 24.02%
 1: 29.67%
 2: 21.84%
 3: 12.68%
 4: 6.58%
 5: 3.03%
 6: 1.33%
 7: 0.5%
 8: 0.24%
 9: 0.05%
 10: 0.03%
 11: 0.02%
 13: 0.01%

Output Distribution: geometric(0.75)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 750ns
Raw Samples: 1, 0, 0, 0, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 0
 Maximum: 7
 Mean: 0.3354
 Std Deviation: 0.675538655627881
Sample Distribution:
 0: 74.94%
 1: 18.86%
 2: 4.56%
 3: 1.22%
 4: 0.24%
 5: 0.15%
 6: 0.02%
 7: 0.01%

Output Distribution: poisson(4.5)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 750ns
Raw Samples: 11, 8, 8, 6, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 13
 Mean: 4.495
 Std Deviation: 2.113391029167157
Sample Distribution:
 0: 1.21%
 1: 4.77%
 2: 11.68%
 3: 16.49%
 4: 18.99%
 5: 16.99%
 6: 13.03%
 7: 8.31%
 8: 4.6%
 9: 2.46%
 10: 0.76%
 11: 0.47%
 12: 0.19%
 13: 0.05%

Output Distribution: discrete(7, 1, 30, 1)
Approximate Single Execution Time: Min: 531ns, Mid: 562ns, Max: 812ns
Raw Samples: 5, 4, 6, 6, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 6
 Mean: 4.0303
 Std Deviation: 1.7127975004441571
Sample Distribution:
 0: 3.18%
 1: 7.25%
 2: 10.44%
 3: 13.65%
 4: 18.38%
 5: 22.17%
 6: 24.93%


Random Floats
Output Distribution: random()
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 343ns
Raw Samples: 0.846052538094602, 0.1973952371853305, 0.11818109437868737, 0.10555078554237902, 0.25965332182806466
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00021912941867433889
 Median: (0.5071392705577044, 0.5072020536726224)
 Maximum: 0.9999920114408419
 Mean: 0.5039749487024219
 Std Deviation: 0.2912749182043624
Post-processor Distribution using round method:
 0: 49.35%
 1: 50.65%

Output Distribution: uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 187ns
Raw Samples: 7.205276397768717, 7.430005633772588, 5.278774959797854, 4.433909772176701, 9.96538390218068
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0016360853183049076
 Median: (5.023451747405543, 5.0264854957925)
 Maximum: 9.997650583549555
 Mean: 4.995506871884992
 Std Deviation: 2.895722929817578
Post-processor Distribution using floor method:
 0: 9.97%
 1: 10.04%
 2: 10.22%
 3: 9.87%
 4: 9.66%
 5: 10.27%
 6: 10.3%
 7: 9.51%
 8: 10.06%
 9: 10.1%

Output Distribution: expovariate(1.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 156ns
Raw Samples: 0.45652830420824364, 1.3073083905345073, 0.8785815142320266, 1.7250542921345076, 4.595369131310768
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 6.361443680914207e-05
 Median: (0.6925384875839697, 0.6925541519235071)
 Maximum: 8.70372132935122
 Mean: 1.0065354273704155
 Std Deviation: 1.0161132692565442
Post-processor Distribution using floor method:
 0: 63.21%
 1: 23.33%
 2: 8.46%
 3: 3.03%
 4: 1.24%
 5: 0.4%
 6: 0.18%
 7: 0.1%
 8: 0.05%

Output Distribution: gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 531ns
Raw Samples: 0.31325702990266924, 1.7141429264902484, 3.301293407675033, 1.3550159991989856, 0.7341868612479718
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.01415920526772596
 Median: (1.6803212021245177, 1.6804318305342556)
 Maximum: 14.810589619507457
 Mean: 2.005059989567606
 Std Deviation: 1.4256492957730775
Post-processor Distribution using round method:
 0: 9.1%
 1: 34.91%
 2: 27.04%
 3: 15.35%
 4: 7.24%
 5: 3.8%
 6: 1.45%
 7: 0.55%
 8: 0.31%
 9: 0.14%
 10: 0.06%
 11: 0.03%
 13: 0.01%
 15: 0.01%

Output Distribution: weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 281ns
Raw Samples: 0.7207651682275718, 1.3155910266080326, 0.1709778522612998, 0.10393060517232103, 0.1595950664758277
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 7.31714479986909e-05
 Median: (0.6911228496932816, 0.6911721735821755)
 Maximum: 11.600235349344523
 Mean: 1.007771515265195
 Std Deviation: 1.017663261389587
Post-processor Distribution using floor method:
 0: 62.89%
 1: 23.5%
 2: 8.37%
 3: 3.27%
 4: 1.27%
 5: 0.42%
 6: 0.1%
 7: 0.12%
 8: 0.05%
 11: 0.01%

Output Distribution: betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 500ns
Raw Samples: 0.6356102628842194, 0.3084762901489647, 0.7432265001212126, 0.4513889255947116, 0.31115613005193404
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.02644454108517302
 Median: (0.4994505098217652, 0.4994966565246561)
 Maximum: 0.9868041986698074
 Mean: 0.5002487754098465
 Std Deviation: 0.19001650891387792
Post-processor Distribution using round method:
 0: 50.11%
 1: 49.89%

Output Distribution: paretovariate(4.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 187ns
Raw Samples: 1.4653886375858274, 1.0434835086955216, 1.498043325186626, 1.1593240459332987, 1.0146977034505187
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.000004446200614
 Median: (1.1855989563196707, 1.1856741476717931)
 Maximum: 16.297522081911545
 Mean: 1.3396668753537815
 Std Deviation: 0.5215651024529856
Post-processor Distribution using floor method:
 1: 93.63%
 2: 4.93%
 3: 0.95%
 4: 0.26%
 5: 0.12%
 6: 0.04%
 7: 0.02%
 8: 0.02%
 10: 0.01%
 14: 0.01%
 16: 0.01%

Output Distribution: gauss(0.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 187ns
Raw Samples: 0.34072087569144954, 0.3060798663007792, -1.011948663771513, -1.6130987503883516, 0.2450396638236827
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -3.8501600731510606
 Median: (0.005986894352830396, 0.0067157836973201525)
 Maximum: 3.9099392743347496
 Mean: -0.001784815300767508
 Std Deviation: 0.9925058391956377
Post-processor Distribution using round method:
 -4: 0.01%
 -3: 0.58%
 -2: 5.8%
 -1: 24.72%
 0: 37.97%
 1: 24.24%
 2: 6.14%
 3: 0.52%
 4: 0.02%

Output Distribution: normalvariate(0.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 218ns
Raw Samples: -0.8980666631282985, 0.12823615392258697, -0.7933598979714376, 0.9064422639617192, -0.1929079584372926
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -4.413544369329797
 Median: (0.007360447199560481, 0.0073991496369854234)
 Maximum: 3.679888763086155
 Mean: -0.0012324719750634707
 Std Deviation: 1.001989344343076
Post-processor Distribution using round method:
 -4: 0.03%
 -3: 0.68%
 -2: 5.93%
 -1: 24.37%
 0: 38.17%
 1: 24.26%
 2: 5.91%
 3: 0.64%
 4: 0.01%

Output Distribution: lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 593ns
Raw Samples: 0.9426938410966741, 0.7340928772124241, 0.7051356135472563, 0.7176319887889728, 2.521421540058662
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.15727203296308204
 Median: (0.9951105487438903, 0.9952892176300111)
 Maximum: 7.475626087118685
 Mean: 1.1334380390945635
 Std Deviation: 0.6134199657702992
Post-processor Distribution using round method:
 0: 8.66%
 1: 70.37%
 2: 17.5%
 3: 2.75%
 4: 0.58%
 5: 0.08%
 6: 0.05%
 7: 0.01%

Output Distribution: vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 218ns
Raw Samples: 4.101346673420255, 1.0175384152996878, 3.7764916929572188, 1.7279632047011049, 3.180704336768798
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0008216787582583983
 Median: (3.155458496319151, 3.1555781301804298)
 Maximum: 6.282265575002364
 Mean: 3.12754365075175
 Std Deviation: 1.80206269990304
Post-processor Distribution using floor method:
 0: 16.03%
 1: 15.98%
 2: 15.57%
 3: 16.35%
 4: 16.33%
 5: 15.48%
 6: 4.26%

Output Distribution: triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 1.2832425947899317, 2.102535476569576, 0.17179253594990063, 0.5515150752012565, 0.13263033026856275
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0002712246897884629
 Median: (2.94715874557495, 2.947529056506312)
 Maximum: 9.949665093094412
 Mean: 3.365842642579408
 Std Deviation: 2.364072021165404
Post-processor Distribution using floor method:
 0: 18.42%
 1: 17.11%
 2: 15.23%
 3: 12.93%
 4: 10.98%
 5: 8.97%
 6: 7.1%
 7: 5.09%
 8: 3.12%
 9: 1.05%

Output Distribution: extreme_value(0.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 562ns
Raw Samples: 0.7511523419666825, -0.8085270919017626, 2.1192457130369355, 1.2935017028940274, 1.2369792489633131
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.4136679472927014
 Median: (0.3764134899312145, 0.3769468253148001)
 Maximum: 9.415276272979652
 Mean: 0.580660752757572
 Std Deviation: 1.2811235981430573
Post-processor Distribution using round method:
 -2: 1.06%
 -1: 18.36%
 0: 34.86%
 1: 25.6%
 2: 11.92%
 3: 5.17%
 4: 2.02%
 5: 0.61%
 6: 0.29%
 7: 0.07%
 8: 0.03%
 9: 0.01%

Output Distribution: chi_squared(1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 468ns
Raw Samples: 2.5447181621001125, 0.06268837336462327, 2.3287851324316464, 0.003229599192547228, 0.9986413192464106
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.1419628774425173e-09
 Median: (0.4714970001567942, 0.4715309603811357)
 Maximum: 15.262759816044754
 Mean: 1.0008591525173434
 Std Deviation: 1.4122534839976337
Post-processor Distribution using <lambda> method:
 0: 68.35%
 1: 16.07%
 2: 7.32%
 3: 3.84%
 4: 2.11%
 5: 1.09%
 6: 0.72%
 7: 0.29%
 8: 0.14%
 9: 0.07%

Output Distribution: cauchy(0.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 0.28325871841507094, 4.435001742217056, 1.5995079008290123, 0.7642356401652745, 1.7306422302911426
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -15851.904013468971
 Median: (0.01484168885855716, 0.014910797560624309)
 Maximum: 2566.2027832650533
 Mean: -2.9203908988587064
 Std Deviation: 182.727032109775
Post-processor Distribution using <lambda> method:
 0: 26.48%
 1: 10.9%
 2: 6.1%
 3: 3.6%
 4: 3.14%
 5: 3.14%
 6: 3.83%
 7: 5.74%
 8: 11.11%
 9: 25.96%

Output Distribution: fisher_f(8.0, 8.0)
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 812ns
Raw Samples: 1.2021650621354558, 0.8289349316326107, 2.427739381291576, 1.6946898676790874, 0.7637404334289942
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.05011444717152427
 Median: (0.9916210250385926, 0.991645704259127)
 Maximum: 17.39794386420265
 Mean: 1.3176949497053467
 Std Deviation: 1.1781932041269314
Post-processor Distribution using <lambda> method:
 0: 50.52%
 1: 32.52%
 2: 10.21%
 3: 3.79%
 4: 1.64%
 5: 0.64%
 6: 0.33%
 7: 0.17%
 8: 0.11%
 9: 0.07%

Output Distribution: student_t(8.0)
Approximate Single Execution Time: Min: 156ns, Mid: 156ns, Max: 281ns
Raw Samples: -1.9998748921324494, -0.6190073286843416, -0.36706145339977186, 0.4880235734259967, -2.46849762144592
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -6.848262946239633
 Median: (-0.004397760380123028, -0.004140434507593371)
 Maximum: 6.002564963540911
 Mean: -0.016360109833868937
 Std Deviation: 1.1717095885156164
Post-processor Distribution using round method:
 -7: 0.01%
 -6: 0.01%
 -5: 0.07%
 -4: 0.32%
 -3: 1.79%
 -2: 6.79%
 -1: 23.72%
 0: 36.19%
 1: 22.41%
 2: 6.67%
 3: 1.59%
 4: 0.37%
 5: 0.05%
 6: 0.01%


Random Booleans
Output Distribution: percent_true(33.33)
Approximate Single Execution Time: Min: 31ns, Mid: 31ns, Max: 125ns
Raw Samples: False, False, False, False, False
Test Samples: 10000
Sample Statistics:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.3321
 Std Deviation: 0.47099020496961264
Sample Distribution:
 False: 66.79%
 True: 33.21%


Random Shuffles
Base Case
Timer only: random.shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 6812ns, Mid: 7000ns, Max: 11468ns

Timer only: shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 375ns, Mid: 406ns, Max: 1000ns

Timer only: knuth(some_list) of size 10:
Approximate Single Execution Time: Min: 843ns, Mid: 875ns, Max: 2812ns

Timer only: fisher_yates(some_list) of size 10:
Approximate Single Execution Time: Min: 937ns, Mid: 968ns, Max: 1031ns


Random Values
Base Case
Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 750ns, Mid: 812ns, Max: 2406ns
Raw Samples: 9, 2, 6, 4, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5445
 Std Deviation: 2.8593421155457026
Sample Distribution:
 0: 9.38%
 1: 9.88%
 2: 10.15%
 3: 9.91%
 4: 9.96%
 5: 10.5%
 6: 9.95%
 7: 9.98%
 8: 9.97%
 9: 10.32%

Output Distribution: random_value([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 656ns
Raw Samples: 6, 7, 1, 4, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5162
 Std Deviation: 2.861810013899519
Sample Distribution:
 0: 9.77%
 1: 10.12%
 2: 9.75%
 3: 10.2%
 4: 9.51%
 5: 10.33%
 6: 9.97%
 7: 10.67%
 8: 9.92%
 9: 9.76%


-------------------------------------------------------------------------
Total Test Time: 1.921 seconds

```


## Fortuna Development Log
##### Fortuna 3.0.1
- minor typos.

##### Fortuna 3.0.0
- Storm 2 Rebuild.

##### Fortuna 2.1.1
- Small bug fixes.
- Test updates.

##### Fortuna 2.1.0, Major Feature Update
- Fortuna now includes the best of RNG and Pyewacket.

##### Fortuna 2.0.3
- Bug fix.

##### Fortuna 2.0.2
- Clarified some documentation.

##### Fortuna 2.0.1
- Fixed some typos.

##### Fortuna 2.0.0b1-10
- Total rebuild. New RNG Storm Engine.

##### Fortuna 1.26.7.1
- README updated.

##### Fortuna 1.26.7
- Small bug fix.

##### Fortuna 1.26.6
- Updated README to reflect recent changes to the test script.

##### Fortuna 1.26.5
- Fixed small bug in test script.

##### Fortuna 1.26.4
- Updated documentation for clarity.
- Fixed a minor typo in the test script.

##### Fortuna 1.26.3
- Clean build.

##### Fortuna 1.26.2
- Fixed some minor typos.

##### Fortuna 1.26.1
- Release.

##### Fortuna 1.26.0 beta 2
- Moved README and LICENSE files into fortuna_extras folder.

##### Fortuna 1.26.0 beta 1
- Dynamic version scheme implemented.
- The Fortuna Extension now requires the fortuna_extras package, previously it was optional.

##### Fortuna 1.25.4
- Fixed some minor typos in the test script.

##### Fortuna 1.25.3
- Since version 1.24 Fortuna requires Python 3.7 or higher. This patch corrects an issue where the setup script incorrectly reported requiring Python 3.6 or higher.

##### Fortuna 1.25.2
- Updated test suite.
- Major performance update for TruffleShuffle.
- Minor performance update for QuantumMonty & FlexCat: cycle monty.

##### Fortuna 1.25.1
- Important bug fix for TruffleShuffle, QuantumMonty and FlexCat.

##### Fortuna 1.25
- Full 64bit support.
- The Distribution & Performance Tests have been redesigned.
- Bloat Control: Two experimental features have been removed.
    - RandomWalk
    - CatWalk
- Bloat Control: Several utility functions have been removed from the top level API. These function remain in the Fortuna namespace for now, but may change in the future without warning.
    - stretch_bell, internal only.
    - min_max, not used anymore.
    - analytic_continuation, internal only.
    - flatten, internal only.

##### Fortuna 1.24.3
- Low level refactoring, non-breaking patch.

##### Fortuna 1.24.2
- Setup config updated to improve installation.

##### Fortuna 1.24.1
- Low level patch to avoid potential ADL issue. All low level function calls are now qualified.

##### Fortuna 1.24
- Documentation updated for even more clarity.
- Bloat Control: Two naïve utility functions that are no longer used in the module have been removed.
    - n_samples -> use a list comprehension instead. `[f(x) for _ in range(n)]`
    - bind -> use a lambda instead. `lambda: f(x)`

##### Fortuna 1.23.7
- Documentation updated for clarity.
- Minor bug fixes.
- TruffleShuffle has been redesigned slightly, it now uses a random rotate instead of swap.
- Custom `__repr__` methods have been added to each class.

##### Fortuna 1.23.6
- New method for QuantumMonty: quantum_not_monty - produces the upside down quantum_monty.
- New bias option for FlexCat: not_monty.

##### Fortuna 1.23.5.1
- Fixed some small typos.

##### Fortuna 1.23.5
- Documentation updated for clarity.
- All sequence wrappers can now accept generators as input.
- Six new functions added:
    - random_float() -> float in range [0.0..1.0) exclusive, uniform flat distribution.
    - percent_true_float(num: float) -> bool, Like percent_true but with floating point precision.
    - plus_or_minus_linear_down(num: int) -> int in range [-num..num], upside down pyramid.
    - plus_or_minus_curve_down(num: int) -> int in range [-num..num], upside down bell curve.
    - mostly_not_middle(num: int) -> int in range [0..num], upside down pyramid.
    - mostly_not_center(num: int) -> int in range [0..num], upside down bell curve.
- Two new methods for QuantumMonty:
    - mostly_not_middle
    - mostly_not_center
- Two new bias options for FlexCat, either can be used to define x and/or y axis bias:
    - not_middle
    - not_center

##### Fortuna 1.23.4.2
- Fixed some minor typos in the README.md file.

##### Fortuna 1.23.4.1
- Fixed some minor typos in the test suite.

##### Fortuna 1.23.4
- Fortuna is now Production/Stable!
- Fortuna and Fortuna Pure now use the same test suite.

##### Fortuna 0.23.4, first release candidate.
- RandomCycle, BlockCycle and TruffleShuffle have been refactored and combined into one class: TruffleShuffle.
- QuantumMonty and FlexCat will now use the new TruffleShuffle for cycling.
- Minor refactoring across the module.

##### Fortuna 0.23.3, internal
- Function shuffle(arr: list) added.

##### Fortuna 0.23.2, internal
- Simplified the plus_or_minus_curve(num: int) function, output will now always be bounded to the range [-num..num].
- Function stretched_bell(num: int) added, this matches the previous behavior of an unbounded plus_or_minus_curve.

##### Fortuna 0.23.1, internal
- Small bug fixes and general clean up.

##### Fortuna 0.23.0
- The number of test cycles in the test suite has been reduced to 10,000 (down from 100,000). The performance of the pure python implementation and the c-extension are now directly comparable.
- Minor tweaks made to the examples in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.22.2, experimental features
- BlockCycle class added.
- RandomWalk class added.
- CatWalk class added.

##### Fortuna 0.22.1
- Fortuna classes no longer return lists of values, this behavior has been extracted to a free function called n_samples.

##### Fortuna 0.22.0, experimental features
- Function bind added.
- Function n_samples added.

##### Fortuna 0.21.3
- Flatten will no longer raise an error if passed a callable item that it can't call. It correctly returns such items in an uncalled state without error.
- Simplified `.../fortuna_extras/fortuna_examples.py` - removed unnecessary class structure.

##### Fortuna 0.21.2
- Fix some minor bugs.

##### Fortuna 0.21.1
- Fixed a bug in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.21.0
- Function flatten added.
- Flatten: The Fortuna classes will recursively unpack callable objects in the data set.

##### Fortuna 0.20.10
- Documentation updated.

##### Fortuna 0.20.9
- Minor bug fixes.

##### Fortuna 0.20.8, internal
- Testing cycle for potential new features.

##### Fortuna 0.20.7
- Documentation updated for clarity.

##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can optionally return a list of samples rather than just one value, control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.0, internal
- FlexCat now accepts a standard dict as input. The ordered(ness) of dict is now part of the standard in Python 3.7.1. Previously FlexCat required an OrderedDict, now it accepts either and treats them the same.

##### Fortuna 0.19.7
- Fixed bug in `.../fortuna_extras/fortuna_examples.py`.

##### Fortuna 0.19.6
- Updated documentation formatting.
- Small performance tweak for QuantumMonty and FlexCat.

##### Fortuna 0.19.5
- Minor documentation update.

##### Fortuna 0.19.4
- Minor update to all classes for better debugging.

##### Fortuna 0.19.3
- Updated plus_or_minus_curve to allow unbounded output.

##### Fortuna 0.19.2
- Internal development cycle.
- Minor update to FlexCat for better debugging.

##### Fortuna 0.19.1
- Internal development cycle.

##### Fortuna 0.19.0
- Updated documentation for clarity.
- MultiCat has been removed, it is replaced by FlexCat.
- Mostly has been removed, it is replaced by QuantumMonty.

##### Fortuna 0.18.7
- Fixed some more README typos.

##### Fortuna 0.18.6
- Fixed some README typos.

##### Fortuna 0.18.5
- Updated documentation.
- Fixed another minor test bug.

##### Fortuna 0.18.4
- Updated documentation to reflect recent changes.
- Fixed some small test bugs.
- Reduced default number of test cycles to 10,000 - down from 100,000.

##### Fortuna 0.18.3
- Fixed some minor README typos.

##### Fortuna 0.18.2
- Fixed a bug with Fortuna Pure.

##### Fortuna 0.18.1
- Fixed some minor typos.
- Added tests for `.../fortuna_extras/fortuna_pure.py`

##### Fortuna 0.18.0
- Introduced new test format, now includes average call time in nanoseconds.
- Reduced default number of test cycles to 100,000 - down from 1,000,000.
- Added pure Python implementation of Fortuna: `.../fortuna_extras/fortuna_pure.py`
- Promoted several low level functions to top level.
    - `zero_flat(num: int) -> int`
    - `zero_cool(num: int) -> int`
    - `zero_extreme(num: int) -> int`
    - `max_cool(num: int) -> int`
    - `max_extreme(num: int) -> int`
    - `analytic_continuation(func: staticmethod, num: int) -> int`
    - `min_max(num: int, lo: int, hi: int) -> int`

##### Fortuna 0.17.3
- Internal development cycle.

##### Fortuna 0.17.2
- User Requested: dice() and d() functions now support negative numbers as input.

##### Fortuna 0.17.1
- Fixed some minor typos.

##### Fortuna 0.17.0
- Added QuantumMonty to replace Mostly, same default behavior with more options.
- Mostly is depreciated and may be removed in a future release.
- Added FlexCat to replace MultiCat, same default behavior with more options.
- MultiCat is depreciated and may be removed in a future release.
- Expanded the Treasure Table example in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.16.2
- Minor refactoring for WeightedChoice.

##### Fortuna 0.16.1
- Redesigned fortuna_examples.py to feature a dynamic random magic item generator.
- Raised cumulative_weighted_choice function to top level.
- Added test for cumulative_weighted_choice as free function.
- Updated MultiCat documentation for clarity.

##### Fortuna 0.16.0
- Pushed distribution_timer to the .pyx layer.
- Changed default number of iterations of tests to 1 million, up form 1 hundred thousand.
- Reordered tests to better match documentation.
- Added Base Case Fortuna.fast_rand_below.
- Added Base Case Fortuna.fast_d.
- Added Base Case Fortuna.fast_dice.

##### Fortuna 0.15.10
- Internal Development Cycle

##### Fortuna 0.15.9
- Added Base Cases for random.choices()
- Added Base Case for randint_dice()

##### Fortuna 0.15.8
- Clarified MultiCat Test

##### Fortuna 0.15.7
- Fixed minor typos.

##### Fortuna 0.15.6
- Fixed minor typos.
- Simplified MultiCat example.

##### Fortuna 0.15.5
- Added MultiCat test.
- Fixed some minor typos in docs.

##### Fortuna 0.15.4
- Performance optimization for both WeightedChoice() variants.
- Cython update provides small performance enhancement across the board.
- Compilation now leverages Python3 all the way down.
- MultiCat pushed to the .pyx layer for better performance.

##### Fortuna 0.15.3
- Reworked the MultiCat example to include several randomizing strategies working in concert.
- Added Multi Dice 10d10 performance tests.
- Updated sudo code in documentation to be more pythonic.

##### Fortuna 0.15.2
- Fixed: Linux installation failure.
- Added: complete source files to the distribution (.cpp .hpp .pyx).

##### Fortuna 0.15.1
- Updated & simplified distribution_timer in `fortuna_tests.py`
- Readme updated, fixed some typos.
- Known issue preventing successful installation on some linux platforms.

##### Fortuna 0.15.0
- Performance tweaks.
- Readme updated, added some details.

##### Fortuna 0.14.1
- Readme updated, fixed some typos.

##### Fortuna 0.14.0
- Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms.

##### Fortuna 0.13.3
- Fixed Test Bug: percent sign was missing in output distributions.
- Readme updated: added update history, fixed some typos.

##### Fortuna 0.13.2
- Readme updated for even more clarity.

##### Fortuna 0.13.1
- Readme updated for clarity.

##### Fortuna 0.13.0
- Minor Bug Fixes.
- Readme updated for aesthetics.
- Added Tests: `.../fortuna_extras/fortuna_tests.py`

##### Fortuna 0.12.0
- Internal test for future update.

##### Fortuna 0.11.0
- Initial Release: Public Beta

##### Fortuna 0.10.0
- Module name changed from Dice to Fortuna

##### Dice 0.1.x - 0.9.x
- Experimental Phase


## Legal Information
Fortuna © 2019 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>
