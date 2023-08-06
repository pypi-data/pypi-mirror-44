# Fortuna: Random Value Generator
Fortuna's main goal is to provide a quick and easy way to build custom random generators that don't suck.

The core functionality of Fortuna is based on the RNG Storm engine. While Storm is a high quality random engine, Fortuna is not appropriate for cryptography of any kind. Fortuna is meant for games, data science, A.I. and experimental programming, not security.

Suggested Installation: `$ pip install Fortuna`

Installation on platforms other than MacOS may require building from source files.


### Documentation Table of Contents:
- Numeric Limits
- Project Definitions
- Random Value Generators
- Random Integer Generators
- Random Index Generators
- Random Float Generators
- Random Bool Generator
- Shuffle Algorithms
- Test Suite Functions
- Test Suite Output
- Development Log
- Legal Information


##### Numeric Limits:
- Integer Limits: 64 bit signed integer.
    - Input & Output Range: `(-2**63, 2**63)` or approximately +/- 9.2 billion billion.
    - Minimum: -9223372036854775807
    - Maximum:  9223372036854775807
- Float Limits: 64 bit double precision floating point.
    - Minimum: -1.7976931348623157e+308
    - Maximum:  1.7976931348623157e+308
    - Epsilon Below Zero: -5e-324
    - Epsilon Above Zero:  5e-324

##### Project Definitions:
- Value: Any python object that can be put inside a list: str, int, and lambda to name a few. Almost anything.
- Callable: Any callable object, function, method or lambda.
- Sequence: Any object that can be converted into a list via `list(some_object)`.
    - List, Tuple, Set, etc...
    - Comprehensions and Generators that produce Sequences also qualify.
    - Classes that wrap a collection will take any Sequence or Array.
- Array: List, tuple or any object that inherits from either.
    - Must be indexed like a list.
    - List comprehensions are Arrays, but sets and generators are not.
    - All Arrays are Sequences but not all Sequences are Arrays.
    - Functions that operate on a collection will require an Array.
- Pair: Array of two values.
- Table: Array of Pairs.
    - List of lists of two values each.
    - Tuple of tuples of two values each.
    - Generators that produce Tables also qualify.
    - The result of zip(list_1, list_2) also qualifies.
- Matrix: Dictionary of Arrays.
    - Generators or comprehensions that produces a Matrix also qualify.
- Inclusive Range.
    - `[1, 10] -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Exclusive Range.
    - `(0, 11) -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- Partial Ranges.
    - `[1, 11) -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
    - `(0, 10] -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`


## Random Value Classes
### TruffleShuffle
`Fortuna.TruffleShuffle(list_of_values: Sequence) -> Callable`
- The input Sequence can be any list like object (list, set, tuple or generator).
- The input Sequence must not be empty. Values can be any python object.
- The returned callable produces a random value from the list with a wide uniform distribution.

#### TruffleShuffle, Basic Use Case
```python
from Fortuna import TruffleShuffle


list_of_values = [1, 2, 3, 4, 5, 6]

truffle_shuffle = TruffleShuffle(list_of_values)

print(truffle_shuffle())
```

**Wide Uniform Distribution**: *"Wide"* refers to the average distance between consecutive occurrences of the same item in the output sequence. The goal of this type of distribution is to keep the output sequence free of clumps while maintaining randomness and uniformity.

This is not the same as a *flat uniform distribution*. The two distributions will be statistically similar, but the output sequences are very different. For a more general solution that offers several statistical distributions, please refer to QuantumMonty. For a more custom solution featuring discrete rarity refer to RelativeWeightedChoice and its counterpart CumulativeWeightedChoice.

**Micro-shuffle**: This is the hallmark of TruffleShuffle and how it creates a wide uniform distribution efficiently. While adjacent duplicates are forbidden, nearly consecutive occurrences of the same item are also required to be extremely rare with respect to the size of the set. This gives rise to output sequences that seem less mechanical than other random sequences. Somehow more and less random at the same time, almost human-like?

**Automatic Flattening**: TruffleShuffle and all higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error. A callable object can be any class, function, method or lambda. Mixing callable objects with un-callable objects is fully supported. Nested callable objects are fully supported. It's lambda all the way down.

To disable automatic flattening, pass the optional argument flat=False during instantiation.

Please review the code examples of each section. If higher-order functions and lambdas make your head spin, concentrate only on the first example. Because `lambda(lambda) -> lambda` fixes everything for arbitrary values of 'because', 'fixes' and 'everything'.


#### Flattening Callable Objects
```python
from Fortuna import TruffleShuffle


""" Note: The following examples feature lambdas, but any callable object will work the same way. """

flatted = TruffleShuffle([lambda: 1, lambda: 2, lambda: 3])
print(flatted())  # will print the value 1, 2 or 3.
# Note: the chosen lambda will not be called until call time and stays dynamic for the life of the object.

un_flat = TruffleShuffle([lambda: 1, lambda: 2, lambda: 3], flat=False)
print(un_flat()())  # will print the value 1, 2 or 3, mind the double-double parenthesis

auto_un_flat = TruffleShuffle([lambda x: x, lambda x: x + 1, lambda x:  x + 2], flat=False)
# Note: flat=False is not required here because these none of the lambdas can be called without input x satisfied.
# It is still recommended to specify flat=False if that is what you intend.
print(auto_un_flat()(1))  # will print the value 1, 2 or 3, mind the double-double parenthesis

```


#### Mixing Static Objects with Callable Objects
```python
from Fortuna import TruffleShuffle


mixed_flat = TruffleShuffle([1, lambda: 2])  # this is fine and works as intended.
print(mixed_flat())  # will print 1 or 2

mixed_un_flat = TruffleShuffle([1, lambda: 2], flat=False) # this pattern is not recommended.
print(mixed_flat())  # will print 1 or "Function <lambda at some_address>"
# This pattern is not recommended because you wont know the nature of what you get back.
# This is almost always not what you want, and it's messy.
```


#### Dynamic Strings
To successfully express a dynamic string, at least one level of indirection is required.
Without an indirection the f-string would collapse into a static string too soon.

WARNING: The following example features a higher order class that takes a tuple of lambdas and returns a higher order callable that returns the result of a random lambda.

```python
from Fortuna import TruffleShuffle, d


# d() is a simple dice function, d(n) -> [1, n] flat uniform
dynamic_strings = TruffleShuffle((
    # while the probability of all A == all B == all C, individual probabilities of each value will differ.
    lambda: f"A{d(2)}",  # -> A1 - A2, each are twice as likely as any particular B, and three times as likely as any C.
    lambda: f"B{d(4)}",  # -> B1 - B4, each are half as likely as any particular A, and 3/2 as likely as any C.
    lambda: f"C{d(6)}",  # -> C1 - C6, each are 1/3 as likely as any particular A and 2/3 as likely of any B.
))

print(dynamic_strings())  # prints a random dynamic string.

"""
Sample Distribution of 10,000 dynamic_strings():
    A1: 16.92%
    A2: 16.66%
    B1: 8.08%
    B2: 8.51%
    B3: 8.15%
    B4: 8.1%
    C1: 5.62%
    C2: 5.84%
    C3: 5.71%
    C4: 5.43%
    C5: 5.22%
    C6: 5.76%
"""
```


### QuantumMonty
`Fortuna.QuantumMonty(some_list: Sequence) -> Callable`
- The input Sequence can be any list like object (list, set, tuple or generator).
- The input Sequence must not be empty. Values can be any python object.
- The instance will produce random values from the list using the selected distribution model or "monty".
- The default monty is the Quantum Monty Algorithm.

```python
from Fortuna import QuantumMonty


list_of_values = [1, 2, 3, 4, 5, 6]
monty = QuantumMonty(list_of_values)

print(monty())               # prints a random value from the list_of_values.
                             # uses the default Quantum Monty Algorithm.

print(monty.flat_uniform())  # prints a random value from the list_of_values.
                             # uses the "uniform" monty: a flat uniform distribution.
                             # equivalent to random.choice(list_of_values).
```
The QuantumMonty class represents a diverse collection of strategies for producing random values from a sequence where the output distribution is based on the method you choose. Generally speaking, each value in the sequence will have a probability that is based on its position in the sequence. For example: the "front" monty produces random values where the beginning of the sequence is geometrically more common than the back. Given enough samples the "front" monty will always converge to a 45 degree slope down for any list of unique values.

There are three primary method families: geometric, gaussian, and poisson. Each family has three base methods; 'front', 'middle', 'back', plus a 'quantum' method that incorporates all three base methods. The quantum algorithms for each family produce distributions by overlapping the probability waves of the other methods in their family. The Quantum Monty Algorithm incorporates all nine base methods.

In addition to the thirteen positional methods that are core to QuantumMonty, it also implements a uniform distribution as a simple base case.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.

```python
import Fortuna


monty = Fortuna.QuantumMonty(
    ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
)

# Each of the following methods will return a random value from the sequence.
# Each method has its own unique distribution model for the same data set.

""" Flat Base Case """
monty.flat_uniform()             # Flat Uniform Distribution

""" Geometric Positional """
monty.front_linear()        # Linear Descending, Triangle
monty.middle_linear()       # Linear Median Peak, Equilateral Triangle
monty.back_linear()         # Linear Ascending, Triangle
monty.quantum_linear()      # Linear Overlay, 3-way monty.

""" Gaussian Positional """
monty.front_gauss()         # Front Gamma
monty.middle_gauss()        # Scaled Gaussian
monty.back_gauss()          # Reversed Gamma
monty.quantum_gauss()       # Gaussian Overlay, 3-way monty.

""" Poisson Positional """
monty.front_poisson()       # 1/3 Mean Poisson
monty.middle_poisson()      # 1/2 Mean Poisson
monty.back_poisson()        # -1/3 Mean Poisson
monty.quantum_poisson()     # Poisson Overlay, 3-way monty.

""" Quantum Monty Algorithm """
monty()                     # Quantum Monty Algorithm, 9-way monty.
monty.quantum_monty()
```

### Weighted Choice: Custom Rarity
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values.

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
`Fortuna.CumulativeWeightedChoice(weighted_table: Table) -> Callable`

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
`Fortuna.RelativeWeightedChoice(weighted_table: Table) -> Callable`

```python
from Fortuna import RelativeWeightedChoice


population = ["Apple", "Banana", "Cherry", "Grape", "Lime", "Orange"]
rel_weights = [7, 4, 2, 10, 3, 4]
rel_weighted_choice = RelativeWeightedChoice(zip(rel_weights, population))

print(rel_weighted_choice())  # prints a weighted random value
```

### FlexCat
`Fortuna.FlexCat(dict_of_lists: Matrix) -> Callable`

FlexCat is a 2d QuantumMonty.

Rather than taking a sequence, FlexCat takes a Matrix: a dictionary of sequences. When the the instance is called it returns a random value from a random sequence.

The constructor takes two optional keyword arguments to specify the algorithms to be used to make random selections. The algorithm specified for selecting a key need not be the same as the one for selecting values. An optional key may be provided at call time to bypass the random key selection and select a random value from that category. Keys passed in this way must match a key in the Matrix.

By default, FlexCat will use key_bias="front" and val_bias="truffle_shuffle", this will make the top of the data structure geometrically more common than the bottom and it will truffle shuffle the sequence values. This config is known as Top Cat, it produces a descending-step distribution. Many other combinations are available.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.


Algorithmic Options: _See QuantumMonty & TruffleShuffle for more details._
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
### Random Integer
- `Fortuna.random_below(number: int) -> int`
    - Returns a random integer in the exclusive range:
        - [0, number) for positive values.
        - (number, 0] for negative values.
        - Always returns zero when the input is zero
    - Flat uniform distribution.


- `Fortuna.random_int(left_limit: int, right_limit: int) -> int`
    - Fault-tolerant, efficient version of random.randint()
    - Returns a random integer in the range [left_limit, right_limit]
    - `random_int(1, 10) -> [1, 10]`
    - `random_int(10, 1) -> [1, 10]` same as above.
    - Flat uniform distribution.


- `Fortuna.random_range(start: int, stop: int = 0, step: int = 1) -> int`
    - Fault-tolerant, efficient version of `random.randrange()`
    - Returns a random integer in the range [A, B) by increments of C.
    - @param start :: required starting point.
        - `random_range(10) -> [0, 10)` from 0 to 9.
        - `random_range(-10) -> [-10, 0)` from -10 to -1. Same as `Fortuna.random_int()`
    - @param stop :: optional stopping point. With at least two arguments, the order of the first two does not matter.
        - `random_range(0, 10) -> [0, 10)` from 0 to 9.
        - `random_range(10, 0) -> [0, 10)` same as above.
    - @param step :: optional step size.
        - `random_range(0, 10, 2) -> [0, 10) by 2` even numbers from 0 to 8.
        - The sign of the step parameter controls the phase of the output. Negative stepping will flip the inclusively.
        - `random_range(0, 10, -1) -> (0, 10]` from 10 to 1.
        - `random_range(10, 0, -1) -> (0, 10]` same as above.
    - `random_range(10, 10, 0) -> [10]` a step size or range size of zero always returns the first parameter.
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
    - Linear geometric, 45 degree triangle distribution.


### Random Index, ZeroCool Specification
- Methods used by LazyCat via dependency injection to generate random indices of any distribution.
- Custom ZeroCool methods must have the following properties:
    - Any random distribution model is acceptable, so long as:
    - The method or function takes exactly one parameter N such that:
    - The method returns a random int in range `[0, N)` for positive values of N.
    - The method returns a random int in range `[N, 0)` for negative values of N.

This symmetry matches how python will naturally index a list from the back for negative index values or from the front for positive index values, see the example code.

ZeroCool functions often have an interesting limit as size goes to zero. ZeroCool compatibility does not make any requirements on the output of this limit. At a higher level of abstraction inside classes that employ ZeroCool methods-- zero is always a sentinel to indicate the full range of the list. In that case the length of the list is sent to the ZeroCool method, not zero. However for those who enjoy thinking a little deeper, consider the following:

If given the fact that an empty range is never an option, we could design a better solution than failure for input zero. Calculus might suggest that both infinity and negative infinity are equally viable output for an input limit of zero, but both are inappropriate for indexing a list. If we map infinity to the back of the list and minus infinity to the front of the list, then the following might hold: `random_index(0) -> [-1, 0]`. This "Top or Bottom" solution is not required for a method to be ZeroCool compatible, it's just an option. Other valid possibilities include: always return None or 0 or -1 or throw an exception or spawn nasal demons, however none of these seem terribly helpful or useful. At least the Top/Bottom solution always accurately reflects the "off by one" symmetry of the input->output domain mapping that defines ZeroCool methods in general.


```python
from Fortuna import random_index


some_list = [i for i in range(100)]

print(some_list[random_index(10)])  # prints one of the first 10 items of some_list, [0, 9]
print(some_list[random_index(-10)])  # prints one of the last 10 items of some_list, [90, 99]
```
### ZeroCool Methods
- `Fortuna.random_index(size: int) -> int` Flat uniform distribution
- `Fortuna.front_gauss(size: int) -> int` Gamma Distribution: Front Peak
- `Fortuna.middle_gauss(size: int) -> int` Normal Distribution: Median Peak
- `Fortuna.back_gauss(size: int) -> int` Gamma Distribution: Back Peak
- `Fortuna.quantum_gauss(size: int) -> int` Quantum Gaussian: Three-way Monty
- `Fortuna.front_poisson(size: int) -> int` Poisson Distribution: Front 1/3 Peak
- `Fortuna.middle_poisson(size: int) -> int` Poisson Distribution: Middle Peak
- `Fortuna.back_poisson(size: int) -> int` Poisson Distribution: Back 2/3 Peak
- `Fortuna.quantum_poisson(size: int) -> int` Quantum Poisson: Three-way Monty
- `Fortuna.front_geometric(size: int) -> int` Linear Geometric: 45 Degree Front Peak
- `Fortuna.middle_geometric(size: int) -> int` Linear Geometric: 45 Degree Middle Peak
- `Fortuna.back_geometric(size: int) -> int` Linear Geometric: 45 Degree Back Peak
- `Fortuna.quantum_geometric(size: int) -> int` Quantum Geometric: Three-way Monty
- `Fortuna.quantum_monty(size: int) -> int` Quantum Monty: Twelve-way Monty

### Generalized QuantumMonty: lazy_cat function
`Fortuna.lazy_cat(data: Array, range_to: int = 0, fn: staticmethod = random_index) -> Value`
- @param data :: Any list like object that supports python indexing.
- @param range_to :: Default zero. Must be equal to or less than the length of data, this represents the size of the output distribution. When range_to == 0, the total length of data is used instead. This arg is passed to the input function to get a valid index into the data. When range_to is negative the back of the data will be considered.
- @param fn :: This callable must follow the ZeroCool method specification. All built-in ZeroCool methods qualify. Default is random_index.
- @return :: Returns a random value from the data using the function and arg you provide.

The lazy_cat function is a general form of the QuantumMonty class.

### Random Float Functions
- `Fortuna.canonical() -> float` returns a random float in range [0.0, 1.0), flat uniform.
- `Fortuna.random_float(a: float, b: float) -> float` returns a random float in range [a, b), flat uniform.


### Random Truth
- `Fortuna.percent_true(truth_factor: float = 50.0) -> bool`
    - Always returns False if num is 0.0 or less
    - Always returns True if num is 100.0 or more.
    - Produces True or False based truth_factor: the probability of True as a percentage.

### Random Shuffle Functions
- `Fortuna.shuffle(array: list) -> None` Knuth B shuffle algorithm.
- `Fortuna.knuth(array: list) -> None` Knuth A shuffle algorithm.
- `Fortuna.fisher_yates(array: list) -> None` Fisher-Yates shuffle algorithm.

### Test Suite Functions
- `Fortuna.distribution_timer(func: staticmethod, *args, **kwargs) -> None`
- `Fortuna.quick_test(cycles=10000) -> None`


## Fortuna Distribution and Performance Test Suite
```
Fortuna Test Suite: RNG Storm Engine

Random Values:

Base Case
Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 1000 nano seconds
Raw Samples: 7, 8, 9, 3, 1
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5067
 Std Deviation: 2.851835971236895
Distribution of 100000 Samples:
 0: 10.041%
 1: 9.884%
 2: 9.977%
 3: 9.962%
 4: 10.112%
 5: 10.025%
 6: 10.169%
 7: 10.038%
 8: 9.901%
 9: 9.891%

Output Distribution: random_value([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 156 nano seconds
Raw Samples: 4, 6, 5, 8, 2
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5523
 Std Deviation: 2.8905190226016506
Distribution of 100000 Samples:
 0: 10.005%
 1: 9.926%
 2: 9.916%
 3: 10.127%
 4: 10.123%
 5: 10.132%
 6: 9.985%
 7: 9.998%
 8: 9.83%
 9: 9.958%

Output Analysis: TruffleShuffle(some_list)()
Typical Timing: 437 nano seconds
Raw Samples: 1, 3, 2, 4, 9
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.493
 Std Deviation: 2.8541488427483346
Distribution of 100000 Samples:
 0: 10.029%
 1: 9.976%
 2: 9.994%
 3: 9.975%
 4: 10.037%
 5: 10.014%
 6: 10.02%
 7: 9.981%
 8: 9.899%
 9: 10.075%

Output Distribution: truffle_shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 218 nano seconds
Raw Samples: 7, 0, 3, 2, 1
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5041
 Std Deviation: 2.881425593581263
Distribution of 100000 Samples:
 0: 9.937%
 1: 9.938%
 2: 10.112%
 3: 9.961%
 4: 9.98%
 5: 9.978%
 6: 10.002%
 7: 10.106%
 8: 10.02%
 9: 9.966%

Output Analysis: QuantumMonty(some_list)()
Typical Timing: 390 nano seconds
Raw Samples: 3, 4, 5, 5, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4588
 Std Deviation: 2.794151622286957
Distribution of 100000 Samples:
 0: 10.412%
 1: 8.049%
 2: 8.458%
 3: 10.342%
 4: 13.023%
 5: 12.694%
 6: 10.37%
 7: 8.394%
 8: 7.87%
 9: 10.388%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function quantum_monty>)
Typical Timing: 343 nano seconds
Raw Samples: 9, 9, 5, 2, 5
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5
 Std Deviation: 2.7700121473974932
Distribution of 100000 Samples:
 0: 10.332%
 1: 8.055%
 2: 8.27%
 3: 10.353%
 4: 12.955%
 5: 12.822%
 6: 10.209%
 7: 8.562%
 8: 8.03%
 9: 10.412%

Base Case
Output Distribution: Random.choices([36, 30, 24, 18], cum_weights=[1, 10, 100, 1000])
Typical Timing: 1718 nano seconds
Raw Samples: [18], [18], [18], [18], [18]
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6654
 Std Deviation: 2.104396751700795
Distribution of 100000 Samples:
 18: 90.014%
 24: 8.979%
 30: 0.913%
 36: 0.094%

Output Analysis: CumulativeWeightedChoice(list(zip(cum_weights, population)))()
Typical Timing: 250 nano seconds
Raw Samples: 18, 18, 24, 18, 18
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6468
 Std Deviation: 2.088752270759953
Distribution of 100000 Samples:
 18: 89.964%
 24: 9.018%
 30: 0.911%
 36: 0.107%

Base Case
Output Distribution: Random.choices([36, 30, 24, 18], weights=[1, 9, 90, 900])
Typical Timing: 2187 nano seconds
Raw Samples: [18], [18], [18], [18], [18]
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6402
 Std Deviation: 2.0569314662150684
Distribution of 100000 Samples:
 18: 90.145%
 24: 8.901%
 30: 0.846%
 36: 0.108%

Output Analysis: RelativeWeightedChoice(list(zip(rel_weights, population)))()
Typical Timing: 250 nano seconds
Raw Samples: 18, 18, 18, 18, 18
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.654
 Std Deviation: 2.0813258254581792
Distribution of 100000 Samples:
 18: 89.929%
 24: 9.107%
 30: 0.875%
 36: 0.089%

Output Analysis: FlexCat(some_matrix)()
Typical Timing: 812 nano seconds
Raw Samples: 300, 10, 2, 4, 40
Statistics of 10000 Samples:
 Minimum: 1
 Median: 10
 Maximum: 400
 Mean: 50.8697
 Std Deviation: 100.44759277254671
Distribution of 100000 Samples:
 1: 12.606%
 2: 12.44%
 3: 12.466%
 4: 12.576%
 10: 8.306%
 20: 8.238%
 30: 8.37%
 40: 8.38%
 100: 4.14%
 200: 4.148%
 300: 4.147%
 400: 4.183%


Random Integers:

Base Case
Output Distribution: Random.randrange(10)
Typical Timing: 875 nano seconds
Raw Samples: 1, 7, 6, 7, 0
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5164
 Std Deviation: 2.8714378899003816
Distribution of 100000 Samples:
 0: 9.891%
 1: 9.884%
 2: 10.123%
 3: 9.987%
 4: 10.021%
 5: 9.95%
 6: 10.042%
 7: 10.079%
 8: 10.03%
 9: 9.993%

Output Distribution: random_below(10)
Typical Timing: 62 nano seconds
Raw Samples: 1, 5, 3, 1, 9
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4193
 Std Deviation: 2.865782402918632
Distribution of 100000 Samples:
 0: 10.039%
 1: 10.104%
 2: 10.059%
 3: 10.064%
 4: 9.943%
 5: 9.905%
 6: 9.991%
 7: 9.943%
 8: 9.969%
 9: 9.983%

Output Distribution: random_index(10)
Typical Timing: 62 nano seconds
Raw Samples: 8, 4, 0, 7, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5012
 Std Deviation: 2.870718143995719
Distribution of 100000 Samples:
 0: 9.851%
 1: 9.976%
 2: 10.024%
 3: 9.968%
 4: 9.979%
 5: 10.157%
 6: 9.913%
 7: 9.987%
 8: 10.042%
 9: 10.103%

Output Distribution: random_range(10)
Typical Timing: 93 nano seconds
Raw Samples: 8, 6, 6, 3, 0
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4372
 Std Deviation: 2.8664050285643126
Distribution of 100000 Samples:
 0: 9.966%
 1: 10.264%
 2: 10.038%
 3: 10.06%
 4: 9.942%
 5: 9.948%
 6: 10.135%
 7: 9.843%
 8: 9.93%
 9: 9.874%

Output Distribution: random_below(-10)
Typical Timing: 77 nano seconds
Raw Samples: -8, -2, -4, -2, -2
Statistics of 10000 Samples:
 Minimum: -9
 Median: -4
 Maximum: 0
 Mean: -4.5008
 Std Deviation: 2.8750697317797806
Distribution of 100000 Samples:
 -9: 10.066%
 -8: 10.093%
 -7: 10.0%
 -6: 9.843%
 -5: 10.101%
 -4: 10.02%
 -3: 9.997%
 -2: 9.959%
 -1: 9.905%
 0: 10.016%

Output Distribution: random_index(-10)
Typical Timing: 93 nano seconds
Raw Samples: -5, -7, -3, -1, -8
Statistics of 10000 Samples:
 Minimum: -10
 Median: -5
 Maximum: -1
 Mean: -5.5245
 Std Deviation: 2.871031875894665
Distribution of 100000 Samples:
 -10: 9.968%
 -9: 10.072%
 -8: 10.107%
 -7: 9.961%
 -6: 10.005%
 -5: 10.148%
 -4: 9.993%
 -3: 9.863%
 -2: 9.976%
 -1: 9.907%

Output Distribution: random_range(-10)
Typical Timing: 93 nano seconds
Raw Samples: -5, -10, -2, -2, -6
Statistics of 10000 Samples:
 Minimum: -10
 Median: -6
 Maximum: -1
 Mean: -5.5368
 Std Deviation: 2.8902389361626852
Distribution of 100000 Samples:
 -10: 10.089%
 -9: 10.056%
 -8: 9.925%
 -7: 10.019%
 -6: 10.067%
 -5: 9.917%
 -4: 10.034%
 -3: 10.102%
 -2: 9.873%
 -1: 9.918%

Base Case
Output Distribution: Random.randrange(1, 10)
Typical Timing: 1125 nano seconds
Raw Samples: 2, 6, 6, 1, 4
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 4.995
 Std Deviation: 2.585158274522168
Distribution of 100000 Samples:
 1: 11.059%
 2: 11.319%
 3: 11.131%
 4: 11.191%
 5: 11.15%
 6: 11.003%
 7: 11.073%
 8: 11.046%
 9: 11.028%

Output Distribution: random_range(1, 10)
Typical Timing: 93 nano seconds
Raw Samples: 1, 1, 4, 7, 7
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 5.0003
 Std Deviation: 2.5863427512382593
Distribution of 100000 Samples:
 1: 11.249%
 2: 11.173%
 3: 11.288%
 4: 11.034%
 5: 11.073%
 6: 11.021%
 7: 11.056%
 8: 11.019%
 9: 11.087%

Output Distribution: random_range(10, 1)
Typical Timing: 93 nano seconds
Raw Samples: 5, 3, 5, 2, 2
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 9
 Mean: 4.9995
 Std Deviation: 2.56155341650151
Distribution of 100000 Samples:
 1: 11.059%
 2: 11.068%
 3: 11.246%
 4: 11.089%
 5: 11.334%
 6: 11.142%
 7: 11.014%
 8: 10.959%
 9: 11.089%

Base Case
Output Distribution: Random.randint(-5, 5)
Typical Timing: 1218 nano seconds
Raw Samples: -3, 3, 5, -1, -5
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0038
 Std Deviation: 3.15613397658715
Distribution of 100000 Samples:
 -5: 9.04%
 -4: 8.978%
 -3: 9.18%
 -2: 9.263%
 -1: 9.045%
 0: 9.037%
 1: 8.875%
 2: 9.243%
 3: 9.003%
 4: 9.153%
 5: 9.183%

Output Distribution: random_int(-5, 5)
Typical Timing: 62 nano seconds
Raw Samples: 3, -4, 5, 0, 1
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0699
 Std Deviation: 3.1635446561537814
Distribution of 100000 Samples:
 -5: 9.067%
 -4: 9.2%
 -3: 9.037%
 -2: 9.052%
 -1: 9.136%
 0: 8.988%
 1: 9.18%
 2: 9.052%
 3: 9.196%
 4: 9.049%
 5: 9.043%

Base Case
Output Distribution: Random.randrange(1, 20, 2)
Typical Timing: 1375 nano seconds
Raw Samples: 17, 19, 1, 9, 7
Statistics of 10000 Samples:
 Minimum: 1
 Median: 11
 Maximum: 19
 Mean: 9.9988
 Std Deviation: 5.748956741041024
Distribution of 100000 Samples:
 1: 9.936%
 3: 10.004%
 5: 9.75%
 7: 10.079%
 9: 9.982%
 11: 10.123%
 13: 10.143%
 15: 10.098%
 17: 9.872%
 19: 10.013%

Output Distribution: random_range(1, 20, 2)
Typical Timing: 93 nano seconds
Raw Samples: 7, 5, 15, 3, 1
Statistics of 10000 Samples:
 Minimum: 1
 Median: 11
 Maximum: 19
 Mean: 10.025
 Std Deviation: 5.726871284171712
Distribution of 100000 Samples:
 1: 9.864%
 3: 10.014%
 5: 9.997%
 7: 10.103%
 9: 9.887%
 11: 10.085%
 13: 10.012%
 15: 10.037%
 17: 9.889%
 19: 10.112%

Output Distribution: random_range(1, 20, -2)
Typical Timing: 93 nano seconds
Raw Samples: 16, 2, 16, 14, 16
Statistics of 10000 Samples:
 Minimum: 2
 Median: 12
 Maximum: 20
 Mean: 10.9756
 Std Deviation: 5.77203051565282
Distribution of 100000 Samples:
 2: 10.088%
 4: 9.912%
 6: 9.884%
 8: 9.983%
 10: 10.009%
 12: 10.033%
 14: 9.888%
 16: 10.157%
 18: 10.035%
 20: 10.011%

Output Distribution: d(10)
Typical Timing: 62 nano seconds
Raw Samples: 7, 3, 5, 10, 3
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4929
 Std Deviation: 2.8786417366224617
Distribution of 100000 Samples:
 1: 10.028%
 2: 10.054%
 3: 10.056%
 4: 9.904%
 5: 10.029%
 6: 9.835%
 7: 10.189%
 8: 10.001%
 9: 9.996%
 10: 9.908%

Output Distribution: dice(3, 6)
Typical Timing: 125 nano seconds
Raw Samples: 15, 9, 10, 11, 10
Statistics of 10000 Samples:
 Minimum: 3
 Median: 10
 Maximum: 18
 Mean: 10.4413
 Std Deviation: 2.9818858922412566
Distribution of 100000 Samples:
 3: 0.473%
 4: 1.39%
 5: 2.793%
 6: 4.751%
 7: 6.927%
 8: 9.729%
 9: 11.45%
 10: 12.55%
 11: 12.62%
 12: 11.521%
 13: 9.635%
 14: 6.893%
 15: 4.672%
 16: 2.737%
 17: 1.432%
 18: 0.427%

Output Distribution: plus_or_minus(5)
Typical Timing: 62 nano seconds
Raw Samples: -5, 3, -1, 3, 0
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0011
 Std Deviation: 3.15903414664577
Distribution of 100000 Samples:
 -5: 9.189%
 -4: 9.107%
 -3: 9.296%
 -2: 9.071%
 -1: 9.231%
 0: 8.958%
 1: 9.091%
 2: 8.965%
 3: 8.934%
 4: 9.188%
 5: 8.97%

Output Distribution: plus_or_minus_linear(5)
Typical Timing: 93 nano seconds
Raw Samples: -2, 0, 2, -1, -4
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0293
 Std Deviation: 2.3856258363505174
Distribution of 100000 Samples:
 -5: 2.816%
 -4: 5.511%
 -3: 8.468%
 -2: 10.942%
 -1: 13.891%
 0: 16.821%
 1: 13.828%
 2: 11.069%
 3: 8.346%
 4: 5.539%
 5: 2.769%


Random Floats:

Output Distribution: canonical()
Typical Timing: 62 nano seconds
Raw Samples: 0.6666510232716625, 0.06053835652020657, 0.6055713145963085, 0.2278378473915638, 0.15297941637087825
Statistics of 10000 Samples:
 Minimum: 3.729954411610869e-05
 Median: (0.49476228547895046, 0.49481991341215253)
 Maximum: 0.9999330011097578
 Mean: 0.49748991256019337
 Std Deviation: 0.2891336240069496
Post-processor Distribution of 100000 Samples using round method:
 0: 49.908%
 1: 50.092%

Output Distribution: random_float(0.0, 10.0)
Typical Timing: 62 nano seconds
Raw Samples: 2.7614073803819768, 2.030316134308384, 9.058116399579959, 7.711370932666717, 0.8999478615065654
Statistics of 10000 Samples:
 Minimum: 0.00045032987979724695
 Median: (5.064132212754977, 5.064187717785503)
 Maximum: 9.997555957280781
 Mean: 5.052270831185045
 Std Deviation: 2.876947132841438
Post-processor Distribution of 100000 Samples using floor method:
 0: 10.056%
 1: 9.905%
 2: 9.953%
 3: 10.043%
 4: 10.028%
 5: 9.968%
 6: 10.059%
 7: 10.058%
 8: 9.971%
 9: 9.959%


Random Booleans:

Output Distribution: percent_true(33.33)
Typical Timing: 62 nano seconds
Raw Samples: False, False, False, False, True
Statistics of 10000 Samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.3385
 Std Deviation: 0.47322314399699583
Distribution of 100000 Samples:
 False: 66.606%
 True: 33.394%


Shuffle Performance Tests:

Base Case: random.shuffle(some_list_100)
Typical Timing: 69328 nano seconds

fisher_yates(some_list_100)
Typical Timing: 7452 nano seconds

knuth(some_list_100)
Typical Timing: 7375 nano seconds

shuffle(some_list_100)
Typical Timing: 4281 nano seconds

-------------------------------------------------------------------------
Total Test Time: 3.048 seconds
```


## Fortuna Development Log
##### Fortuna 3.2.1
- Small Typos.

##### Fortuna 3.2.0
- API updates:
    - QunatumMonty.uniform -> QunatumMonty.flat_uniform
    - QunatumMonty.front -> QunatumMonty.front_linear
    - QunatumMonty.middle -> QunatumMonty.middle_linear
    - QunatumMonty.back -> QunatumMonty.back_linear
    - QunatumMonty.quantum -> QunatumMonty.quantum_linear
    - randindex -> random_index
    - randbelow -> random_below
    - randrange -> random_range
    - randint   -> random_int

##### Fortuna 3.1.0
- `discrete()` has been removed, see Weighted Choice.
- `lazy_cat()` added.
- All ZeroCool methods have been raised to top level API, for use with lazy_cat()

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
- Added Base Cases for random_value()
- Added Base Case for randint()

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
