# Fortuna: Random Value Generator
Fortuna's main goal is to provide a quick and easy way to build custom random generators that don't suck.

The core functionality of Fortuna is based on the RNG Storm engine. While Storm is a high quality random engine, Fortuna is not appropriate for cryptography of any kind. Fortuna is meant for games, data science, A.I. and experimental programming, not security.

Suggested Installation: `$ pip install Fortuna`

Installation on platforms other than MacOS may require building from source files.


### Documentation Table of Contents:
- Project Definitions and Numeric Limits
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


##### Project Definitions:
- Integer: 64 bit signed long long int.
    - Input & Output Range: `(-2**63, 2**63)` or approximately +/- 9.2 billion billion.
    - Minimum: -9223372036854775807
    - Maximum:  9223372036854775807
- Float: 64 bit double precision floating point number.
    - Minimum: -1.7976931348623157e+308
    - Maximum:  1.7976931348623157e+308
    - Epsilon Below Zero: -5e-324
    - Epsilon Above Zero:  5e-324
- Value: Any python object that can be put inside a list: str, int, and lambda to name a few. Almost anything.
- Callable: Any callable object, function, method or lambda.
- Sequence: Any object that can be converted into a list.
    - List, Tuple, Set, etc...
    - Comprehensions and Generators that produce Sequences also qualify.
- Array: List or tuple.
    - Must be indexed like a list.
    - List comprehensions are ok, but sets and generators are not indexed.
    - All arrays are sequences but not all sequences are arrays.
    - Classes that wrap a list will take any Sequence or Array and copy it or convert it as needed.
    - Functions that operate on a list will require an Array.
- Pair: Array of two values.
- Table: Sequence of Pairs.
    - List of lists of two values each.
    - Tuple of tuples of two values each.
    - Generators that produce Tables also qualify.
    - The result of zip(list_1, list_2) also qualifies.
- Matrix: Dictionary of Sequences.
    - Generators that produce Matrices also qualify.
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

print(truffle_shuffle())  # prints a random value from the list_of_values.
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


##### Dynamic Strings
To successfully express a dynamic string, at least one level of indirection is required.
Without an indirection the f-string would collapse into a static string too soon.

WARNING: The following example features a higher order class that takes a tuple of lambdas and returns a higher order callable that returns the result of a random lambda.

```python
from Fortuna import TruffleShuffle, d


# d is a simple dice function, d(n) -> [1, n] flat uniform
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

print(monty())              # prints a random value from the list_of_values.
                            # uses the default Quantum Monty Algorithm.

print(monty.uniform())      # prints a random value from the list_of_values.
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
monty.uniform()             # Flat Uniform Distribution

""" Geometric Positional """
monty.front()               # Geometric Descending, Triangle
monty.middle()              # Geometric Median Peak, Equilateral Triangle
monty.back()                # Geometric Ascending, Triangle
monty.quantum()             # Geometric Overlay, Saw Tooth

""" Gaussian Positional """
monty.front_gauss()         # Exponential Gamma
monty.middle_gauss()        # Scaled Gaussian
monty.back_gauss()          # Reversed Gamma
monty.quantum_gauss()       # Gaussian Overlay

""" Poisson Positional """
monty.front_poisson()       # 1/3 Mean Poisson
monty.middle_poisson()      # 1/2 Mean Poisson
monty.back_poisson()        # -1/3 Mean Poisson
monty.quantum_poisson()     # Poisson Overlay

""" Quantum Monty Algorithm """
monty()                     # Quantum Monty Algorithm
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
    - @param start :: required starting point.
        - `randrange(10) -> [0, 10)` from 0 to 9.
        - `randrange(-10) -> [-10, 0)` from -10 to -1. Same as `Fortuna.randindex()`
    - @param stop :: optional stopping point. With at least two arguments, the order of the first two does not matter.
        - `randrange(0, 10) -> [0, 10)` from 0 to 9.
        - `randrange(10, 0) -> [0, 10)` same as above.
    - @param step :: optional step size.
        - `randrange(0, 10, 2) -> [0, 10) by 2` even numbers from 0 to 8.
        - The sign of the step parameter controls the phase of the output. Negative stepping will flip the inclusively.
        - `randrange(0, 10, -1) -> (0, 10]` from 10 to 1.
        - `randrange(10, 0, -1) -> (0, 10]` same as above.
    - `randrange(10, 10, 0) -> [10]` a step size or range size of zero always returns the first parameter.
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

If given the fact that an empty range is never an option, we could design a better solution than failure for input zero. Calculus might suggest that both infinity and negative infinity are equally viable output for an input limit of zero, but both are inappropriate for indexing a list. If we map infinity to the back of the list and minus infinity to the front of the list, then the following might hold: `randindex(0) -> [-1, 0]`. This "Top or Bottom" solution is not required for a method to be ZeroCool compatible, it's just an option. Other valid possibilities include: always return None or 0 or -1 or throw an exception or spawn nasal demons, however none of these seem terribly helpful or useful. At least the Top/Bottom solution always accurately reflects the "off by one" symmetry of the input->output domain mapping that defines ZeroCool methods in general.


```python
from Fortuna import randindex


some_list = [i for i in range(100)]

print(some_list[randindex(10)])  # prints one of the first 10 items of some_list, [0, 9]
print(some_list[randindex(-10)])  # prints one of the last 10 items of some_list, [90, 99]
```
### ZeroCool Methods
- `Fortuna.randindex(size: int) -> int` Flat uniform distribution
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
`lazy_cat(data: Array, range_to: int = 0, fn: staticmethod = randindex) -> Value`
- @param data :: Any list like object that supports python indexing.
- @param range_to :: Default zero. Must be equal to or less than the length of data, this represents the size of the output distribution. When range_to == 0, the total length of data is used instead. This arg is passed to the input function to get a valid index into the data. When range_to is negative the back of the data will be considered.
- @param fn :: This callable must follow the ZeroCool method specification. All built-in ZeroCool methods qualify. Default is randindex.
- @return :: Returns a random value from the data using the function and arg you provide.

The lazy_cat function is a general form of the QuantumMonty class.

### Random Float Functions
- `Fortuna.random() -> float` returns a random float in range [0.0, 1.0), flat uniform.
- `Fortuna.uniform(a: float, b: float) -> float` returns a random float in range [a, b), flat uniform.


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
- `Fortuna.quick_test() -> None`


## Fortuna Distribution and Performance Test Suite
```
Fortuna Test Suite: RNG Storm Engine

Output Analysis: TruffleShuffle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])()
Typical Timing: 437 nano seconds
Raw Samples: 8, 4, 7, 9, 4
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5013
 Std Deviation: 2.869080248467654
Distribution of 1000000 Samples:
 0: 9.9961%
 1: 9.9622%
 2: 10.0186%
 3: 9.9812%
 4: 10.0123%
 5: 10.0205%
 6: 9.995%
 7: 10.0029%
 8: 10.0242%
 9: 9.987%

Functional truffle_shuffle(some_list)
Output Distribution: truffle_shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 218 nano seconds
Raw Samples: 8, 2, 3, 4, 1
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.4894
 Std Deviation: 2.880437003604344
Distribution of 1000000 Samples:
 0: 10.0083%
 1: 10.0179%
 2: 10.0335%
 3: 10.0113%
 4: 9.9843%
 5: 9.97%
 6: 9.9889%
 7: 10.0006%
 8: 9.9866%
 9: 9.9986%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 234 nano seconds
Raw Samples: 0, 3, 0, 6, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4916
 Std Deviation: 2.894299075201744
Distribution of 1000000 Samples:
 0: 10.0062%
 1: 10.0446%
 2: 10.0384%
 3: 9.955%
 4: 9.9535%
 5: 9.9739%
 6: 10.0367%
 7: 10.004%
 8: 9.9903%
 9: 9.9974%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function front_geometric>)
Typical Timing: 312 nano seconds
Raw Samples: 1, 4, 2, 2, 2
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9877
 Std Deviation: 2.448948436542608
Distribution of 1000000 Samples:
 0: 18.1909%
 1: 16.3851%
 2: 14.586%
 3: 12.7059%
 4: 10.9219%
 5: 9.0602%
 6: 7.2414%
 7: 5.4128%
 8: 3.6549%
 9: 1.8409%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function back_geometric>)
Typical Timing: 312 nano seconds
Raw Samples: 2, 9, 8, 6, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 6
 Maximum: 9
 Mean: 5.9724
 Std Deviation: 2.4808171406551787
Distribution of 1000000 Samples:
 0: 1.8267%
 1: 3.6244%
 2: 5.4898%
 3: 7.243%
 4: 9.082%
 5: 10.9131%
 6: 12.7542%
 7: 14.5085%
 8: 16.3683%
 9: 18.19%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function middle_geometric>)
Typical Timing: 312 nano seconds
Raw Samples: 5, 1, 8, 7, 2
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5145
 Std Deviation: 2.21726890072851
Distribution of 1000000 Samples:
 0: 3.2926%
 1: 6.6787%
 2: 10.0014%
 3: 13.3425%
 4: 16.6647%
 5: 16.6562%
 6: 13.3162%
 7: 10.0231%
 8: 6.6879%
 9: 3.3367%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function front_gauss>)
Typical Timing: 250 nano seconds
Raw Samples: 1, 0, 1, 4, 0
Statistics of 10000 Samples:
 Minimum: 0
 Median: 0
 Maximum: 9
 Mean: 0.5816
 Std Deviation: 0.959183738052483
Distribution of 1000000 Samples:
 0: 63.1589%
 1: 23.2978%
 2: 8.5797%
 3: 3.1493%
 4: 1.1511%
 5: 0.4168%
 6: 0.1578%
 7: 0.0569%
 8: 0.0223%
 9: 0.0094%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function back_gauss>)
Typical Timing: 218 nano seconds
Raw Samples: 9, 9, 8, 9, 9
Statistics of 10000 Samples:
 Minimum: 0
 Median: 9
 Maximum: 9
 Mean: 8.4099
 Std Deviation: 0.9770247938229483
Distribution of 1000000 Samples:
 0: 0.0075%
 1: 0.0212%
 2: 0.0583%
 3: 0.1611%
 4: 0.43%
 5: 1.1726%
 6: 3.164%
 7: 8.5731%
 8: 23.2081%
 9: 63.2041%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function middle_gauss>)
Typical Timing: 250 nano seconds
Raw Samples: 4, 4, 4, 6, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 8
 Mean: 4.5102
 Std Deviation: 1.0507170697366934
Distribution of 1000000 Samples:
 0: 0.003%
 1: 0.1382%
 2: 2.1397%
 3: 13.5476%
 4: 34.163%
 5: 34.1092%
 6: 13.6415%
 7: 2.12%
 8: 0.1353%
 9: 0.0025%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function front_poisson>)
Typical Timing: 281 nano seconds
Raw Samples: 4, 6, 3, 2, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.1651
 Std Deviation: 1.7728384826679962
Distribution of 1000000 Samples:
 0: 4.1752%
 1: 13.1657%
 2: 21.002%
 3: 22.3104%
 4: 17.8501%
 5: 11.289%
 6: 6.0117%
 7: 2.7067%
 8: 1.0849%
 9: 0.4043%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function back_poisson>)
Typical Timing: 281 nano seconds
Raw Samples: 6, 6, 5, 4, 7
Statistics of 10000 Samples:
 Minimum: 0
 Median: 6
 Maximum: 9
 Mean: 5.8338
 Std Deviation: 1.7727074798682714
Distribution of 1000000 Samples:
 0: 0.3995%
 1: 1.1259%
 2: 2.7226%
 3: 6.0076%
 4: 11.3123%
 5: 17.7568%
 6: 22.2587%
 7: 21.0341%
 8: 13.2684%
 9: 4.1141%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function middle_poisson>)
Typical Timing: 312 nano seconds
Raw Samples: 7, 3, 5, 3, 5
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4563
 Std Deviation: 2.200539603700589
Distribution of 1000000 Samples:
 0: 2.2436%
 1: 7.1366%
 2: 11.8802%
 3: 14.1417%
 4: 14.5458%
 5: 14.5706%
 6: 14.1205%
 7: 11.917%
 8: 7.1596%
 9: 2.2844%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function quantum_geometric>)
Typical Timing: 343 nano seconds
Raw Samples: 1, 2, 3, 9, 2
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4753
 Std Deviation: 2.656255913790679
Distribution of 1000000 Samples:
 0: 7.7781%
 1: 8.8978%
 2: 9.9968%
 3: 11.1092%
 4: 12.2487%
 5: 12.1668%
 6: 11.1423%
 7: 9.996%
 8: 8.8833%
 9: 7.781%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function quantum_gauss>)
Typical Timing: 250 nano seconds
Raw Samples: 9, 9, 8, 3, 9
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4769
 Std Deviation: 3.352102332716724
Distribution of 1000000 Samples:
 0: 21.0884%
 1: 7.8164%
 2: 3.5657%
 3: 5.6685%
 4: 11.867%
 5: 11.9064%
 6: 5.624%
 7: 3.5755%
 8: 7.7828%
 9: 21.1053%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function quantum_poisson>)
Typical Timing: 312 nano seconds
Raw Samples: 6, 4, 2, 6, 4
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5276
 Std Deviation: 2.229604304251172
Distribution of 1000000 Samples:
 0: 2.2685%
 1: 7.1862%
 2: 11.8806%
 3: 14.1445%
 4: 14.5222%
 5: 14.5188%
 6: 14.1627%
 7: 11.8692%
 8: 7.1635%
 9: 2.2838%

Output Distribution: lazy_cat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fn=<built-in function quantum_monty>)
Typical Timing: 343 nano seconds
Raw Samples: 6, 0, 3, 6, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5251
 Std Deviation: 2.755272970671743
Distribution of 1000000 Samples:
 0: 10.3472%
 1: 7.9562%
 2: 8.4711%
 3: 10.3051%
 4: 12.8561%
 5: 12.9171%
 6: 10.3103%
 7: 8.4985%
 8: 7.9756%
 9: 10.3628%

Output Distribution: QuantumMonty.quantum_monty()
Typical Timing: 281 nano seconds
Raw Samples: 8, 4, 4, 9, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5079
 Std Deviation: 2.7882817363932486
Distribution of 1000000 Samples:
 0: 10.4349%
 1: 7.9485%
 2: 8.4664%
 3: 10.3206%
 4: 12.89%
 5: 12.8591%
 6: 10.3056%
 7: 8.497%
 8: 7.9262%
 9: 10.3517%


Weighted Choices
Base Case
Output Distribution: Random.choices([36, 30, 24, 18], cum_weights=[1, 10, 100, 1000])
Typical Timing: 1718 nano seconds
Raw Samples: [18], [18], [18], [18], [18]
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6294
 Std Deviation: 2.0602621454588737
Distribution of 1000000 Samples:
 18: 90.029%
 24: 8.9674%
 30: 0.9064%
 36: 0.0972%

Output Analysis: CumulativeWeightedChoice([(1, 36), (10, 30), (100, 24), (1000, 18)], flat=True)()
Typical Timing: 312 nano seconds
Raw Samples: 18, 18, 18, 18, 18
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.651
 Std Deviation: 2.098627986076235
Distribution of 1000000 Samples:
 18: 90.0104%
 24: 9.0022%
 30: 0.8892%
 36: 0.0982%

Functional Weighted Choice
Output Distribution: cumulative_weighted_choice([(1, 36), (10, 30), (100, 24), (1000, 18)])
Typical Timing: 312 nano seconds
Raw Samples: 18, 18, 24, 18, 24
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6552
 Std Deviation: 2.077485151440425
Distribution of 1000000 Samples:
 18: 90.0329%
 24: 8.9492%
 30: 0.9104%
 36: 0.1075%

Base Case
Output Distribution: Random.choices([36, 30, 24, 18], weights=[1, 9, 90, 900])
Typical Timing: 2187 nano seconds
Raw Samples: [18], [18], [18], [24], [18]
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.693
 Std Deviation: 2.1780324567228684
Distribution of 1000000 Samples:
 18: 89.9902%
 24: 8.9972%
 30: 0.9134%
 36: 0.0992%

Output Analysis: RelativeWeightedChoice([(1, 36), (9, 30), (90, 24), (900, 18)], flat=True)()
Typical Timing: 312 nano seconds
Raw Samples: 18, 18, 18, 24, 18
Statistics of 10000 Samples:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6582
 Std Deviation: 2.132141496884359
Distribution of 1000000 Samples:
 18: 89.943%
 24: 9.0435%
 30: 0.9166%
 36: 0.0969%


FlexCat(some_dict)
Output Analysis: FlexCat({1: [1, 2, 3], 2: [10, 20, 30], 3: [100, 200, 300]}, key_bias='front', val_bias='truffle_shuffle', flat=True)()
Typical Timing: 796 nano seconds
Raw Samples: 1, 10, 2, 20, 3
Statistics of 10000 Samples:
 Minimum: 1
 Median: 10
 Maximum: 300
 Mean: 41.011
 Std Deviation: 78.50183394541352
Distribution of 1000000 Samples:
 1: 16.6805%
 2: 16.6696%
 3: 16.7013%
 10: 11.1355%
 20: 11.0907%
 30: 11.1106%
 100: 5.5479%
 200: 5.5282%
 300: 5.5357%


Random Integers
Base Case
Output Distribution: Random.randrange(10)
Typical Timing: 906 nano seconds
Raw Samples: 3, 4, 9, 1, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4892
 Std Deviation: 2.8980205679603506
Distribution of 1000000 Samples:
 0: 9.9731%
 1: 10.078%
 2: 9.9804%
 3: 10.0329%
 4: 9.9834%
 5: 9.954%
 6: 10.0182%
 7: 9.9656%
 8: 10.0055%
 9: 10.0089%

Output Distribution: randbelow(10)
Typical Timing: 62 nano seconds
Raw Samples: 9, 1, 3, 4, 8
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4685
 Std Deviation: 2.8659778667870572
Distribution of 1000000 Samples:
 0: 10.0205%
 1: 10.0276%
 2: 10.0059%
 3: 9.9582%
 4: 10.0082%
 5: 9.994%
 6: 9.9627%
 7: 10.0485%
 8: 9.9976%
 9: 9.9768%

Output Distribution: randindex(10)
Typical Timing: 62 nano seconds
Raw Samples: 2, 2, 3, 3, 0
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5234
 Std Deviation: 2.869682203240415
Distribution of 1000000 Samples:
 0: 10.0514%
 1: 9.9903%
 2: 10.02%
 3: 10.0439%
 4: 10.0236%
 5: 10.0061%
 6: 9.9229%
 7: 9.9863%
 8: 9.9977%
 9: 9.9578%

Output Distribution: randindex(-10)
Typical Timing: 93 nano seconds
Raw Samples: -8, -2, -8, -9, -3
Statistics of 10000 Samples:
 Minimum: -10
 Median: -6
 Maximum: -1
 Mean: -5.5215
 Std Deviation: 2.871996271978539
Distribution of 1000000 Samples:
 -10: 10.0073%
 -9: 9.9962%
 -8: 9.9606%
 -7: 9.9944%
 -6: 10.0491%
 -5: 9.9687%
 -4: 10.0048%
 -3: 10.0187%
 -2: 9.9632%
 -1: 10.037%

Output Distribution: randindex(0)
Typical Timing: 62 nano seconds
Raw Samples: 0, -1, -1, -1, 0
Statistics of 10000 Samples:
 Minimum: -1
 Median: 0
 Maximum: 0
 Mean: -0.4987
 Std Deviation: 0.5000233117877937
Distribution of 1000000 Samples:
 -1: 49.9999%
 0: 50.0001%

Base Case
Output Distribution: Random.randint(-5, 5)
Typical Timing: 1218 nano seconds
Raw Samples: -3, 4, -3, -3, 5
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.0177
 Std Deviation: 3.1524245412140806
Distribution of 1000000 Samples:
 -5: 9.0815%
 -4: 9.081%
 -3: 9.0859%
 -2: 9.101%
 -1: 9.1022%
 0: 9.0543%
 1: 9.1417%
 2: 9.0733%
 3: 9.0765%
 4: 9.115%
 5: 9.0876%

Output Distribution: randint(-5, 5)
Typical Timing: 62 nano seconds
Raw Samples: 0, 3, -5, 5, -5
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0012
 Std Deviation: 3.1742725403808763
Distribution of 1000000 Samples:
 -5: 9.0496%
 -4: 9.098%
 -3: 9.0621%
 -2: 9.1004%
 -1: 9.119%
 0: 9.1216%
 1: 9.1152%
 2: 9.0799%
 3: 9.0591%
 4: 9.097%
 5: 9.0981%

Base Case
Output Distribution: Random.randrange(1, 21, 2)
Typical Timing: 1343 nano seconds
Raw Samples: 7, 5, 19, 9, 19
Statistics of 10000 Samples:
 Minimum: 1
 Median: 11
 Maximum: 19
 Mean: 10.025
 Std Deviation: 5.722189209116952
Distribution of 1000000 Samples:
 1: 10.0136%
 3: 9.9542%
 5: 9.9827%
 7: 10.0366%
 9: 10.0412%
 11: 10.0449%
 13: 10.0101%
 15: 9.9638%
 17: 9.942%
 19: 10.0109%

Output Distribution: randrange(1, 21, 2)
Typical Timing: 93 nano seconds
Raw Samples: 7, 1, 17, 3, 13
Statistics of 10000 Samples:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 10.0252
 Std Deviation: 5.741729853116621
Distribution of 1000000 Samples:
 1: 9.9895%
 3: 9.9606%
 5: 9.9554%
 7: 10.0269%
 9: 9.962%
 11: 10.0283%
 13: 10.017%
 15: 10.0403%
 17: 9.9899%
 19: 10.0301%

Output Distribution: d(10)
Typical Timing: 62 nano seconds
Raw Samples: 7, 10, 1, 9, 7
Statistics of 10000 Samples:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.5046
 Std Deviation: 2.875553115588731
Distribution of 1000000 Samples:
 1: 9.9949%
 2: 9.9565%
 3: 10.0126%
 4: 10.0307%
 5: 10.0056%
 6: 10.0258%
 7: 10.0291%
 8: 9.9537%
 9: 9.9338%
 10: 10.0573%

Output Distribution: dice(2, 6)
Typical Timing: 93 nano seconds
Raw Samples: 5, 8, 8, 5, 6
Statistics of 10000 Samples:
 Minimum: 2
 Median: 7
 Maximum: 12
 Mean: 6.9778
 Std Deviation: 2.379805350727394
Distribution of 1000000 Samples:
 2: 2.7541%
 3: 5.53%
 4: 8.3078%
 5: 11.1689%
 6: 13.8941%
 7: 16.6787%
 8: 13.9259%
 9: 11.1148%
 10: 8.3189%
 11: 5.5473%
 12: 2.7595%

Output Distribution: plus_or_minus(5)
Typical Timing: 62 nano seconds
Raw Samples: 0, 4, -2, -2, 0
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.0214
 Std Deviation: 3.1614461112205303
Distribution of 1000000 Samples:
 -5: 9.1072%
 -4: 9.0838%
 -3: 9.1048%
 -2: 9.0447%
 -1: 9.069%
 0: 9.0742%
 1: 9.1214%
 2: 9.1166%
 3: 9.0736%
 4: 9.0953%
 5: 9.1094%

Output Distribution: plus_or_minus_linear(5)
Typical Timing: 93 nano seconds
Raw Samples: 4, 0, -5, 3, 1
Statistics of 10000 Samples:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.011
 Std Deviation: 2.4122729750363265
Distribution of 1000000 Samples:
 -5: 2.7493%
 -4: 5.6004%
 -3: 8.2862%
 -2: 11.0492%
 -1: 13.9122%
 0: 16.6511%
 1: 13.8965%
 2: 11.1501%
 3: 8.3555%
 4: 5.5588%
 5: 2.7907%


Random Floats
Output Distribution: random()
Typical Timing: 31 nano seconds
Raw Samples: 0.30698251774319535, 0.04487132157019716, 0.7975210983087501, 0.5500140234801947, 0.883560689360766
Statistics of 10000 Samples:
 Minimum: 8.031455202919303e-05
 Median: (0.49739593042271063, 0.4974303265399958)
 Maximum: 0.9997773325536201
 Mean: 0.4972476993768504
 Std Deviation: 0.289827133725155
Post-processor Distribution of 1000000 Samples using round method:
 0: 50.0638%
 1: 49.9362%

Output Distribution: uniform(0.0, 10.0)
Typical Timing: 62 nano seconds
Raw Samples: 4.228820078000746, 0.04370043431147992, 7.296664970407205, 7.171220638915781, 2.2663695181842387
Statistics of 10000 Samples:
 Minimum: 0.0011960112686774673
 Median: (4.968240575884476, 4.968489812897711)
 Maximum: 9.998708487680071
 Mean: 4.98644657789379
 Std Deviation: 2.8691461071015945
Post-processor Distribution of 1000000 Samples using floor method:
 0: 10.0279%
 1: 9.9825%
 2: 10.0066%
 3: 9.9516%
 4: 10.0485%
 5: 9.9821%
 6: 9.9849%
 7: 10.0425%
 8: 9.9715%
 9: 10.0019%


Random Boolean
Output Distribution: percent_true(33.33)
Typical Timing: 62 nano seconds
Raw Samples: False, True, False, False, False
Statistics of 10000 Samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.3334
 Std Deviation: 0.4714516588863239
Distribution of 1000000 Samples:
 False: 66.6055%
 True: 33.3945%


Random Shuffle
Base Case
Timer only: random.shuffle(some_list) of size 10:
Typical Timing: 7125 nano seconds

Timer only: shuffle(some_list) of size 10:
Typical Timing: 406 nano seconds

Timer only: knuth(some_list) of size 10:
Typical Timing: 906 nano seconds

Timer only: fisher_yates(some_list) of size 10:
Typical Timing: 1000 nano seconds


Random Values
Base Case
Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 812 nano seconds
Raw Samples: 5, 8, 2, 0, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5476
 Std Deviation: 2.867360531157804
Distribution of 1000000 Samples:
 0: 10.0157%
 1: 9.9812%
 2: 9.9937%
 3: 9.9875%
 4: 10.0243%
 5: 10.0152%
 6: 9.98%
 7: 9.9693%
 8: 9.994%
 9: 10.0391%

Output Distribution: random_value([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 156 nano seconds
Raw Samples: 5, 3, 7, 7, 5
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4897
 Std Deviation: 2.87045603725021
Distribution of 1000000 Samples:
 0: 9.9605%
 1: 10.04%
 2: 9.9928%
 3: 9.9632%
 4: 9.9955%
 5: 9.9973%
 6: 10.0057%
 7: 10.0001%
 8: 10.0353%
 9: 10.0096%


-------------------------------------------------------------------------
Total Test Time: 24.995 seconds

```


## Fortuna Development Log
##### Fortuna 3.1.0
- `randindex()` added
- `lazy_cat()` added
- `ZeroCool methods` raised to top level API, for use with lazy_cat()
- `discrete()` has been removed, see RelativeWeightedChoice as a replacement

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
