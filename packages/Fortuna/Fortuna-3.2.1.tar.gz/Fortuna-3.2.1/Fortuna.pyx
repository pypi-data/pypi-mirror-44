#!python3
#distutils: language = c++


__all__ = (
    "TruffleShuffle", "QuantumMonty", "CumulativeWeightedChoice", "RelativeWeightedChoice", "FlexCat",
    "random_below", "random_index", "random_int", "random_range", "d", "dice", "ability_dice",
    "percent_true", "plus_or_minus", "plus_or_minus_linear",
    "shuffle", "knuth", "fisher_yates", "truffle_shuffle", "random_value",
    "cumulative_weighted_choice", "lazy_cat", "canonical", "random_float",
    "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss", "front_poisson",
    "middle_poisson", "back_poisson", "quantum_poisson", "front_linear",
    "middle_linear", "back_linear", "quantum_linear", "quantum_monty",
    "quick_test", "distribution_timer", "timer", "fuzzy_clamp", "smart_clamp", "flatten",
)


cdef extern from "Fortuna.hpp":
    int       _percent_true             "Fortuna::percent_true"(double)
    long long _smart_clamp              "Fortuna::smart_clamp"(long long, long long, long long)
    long long _fuzzy_clamp              "Fortuna::fuzzy_clamp"(long long, long long)
    long long _randrange                "Fortuna::randrange"(long long, long long, long long)
    long long _randbelow                "Fortuna::randbelow"(long long)
    long long _randindex                "Fortuna::randindex"(long long)
    long long _randint                  "Fortuna::randint"(long long, long long)
    long long _d                        "Fortuna::d"(long long)
    long long _dice                     "Fortuna::dice"(long long, long long)
    long long _ability_dice             "Fortuna::ability_dice"(long long)
    long long _plus_or_minus            "Fortuna::plus_or_minus"(long long)
    long long _plus_or_minus_linear     "Fortuna::plus_or_minus_linear"(long long)
    long long _front_gauss              "Fortuna::front_gauss"(long long)
    long long _middle_gauss             "Fortuna::middle_gauss"(long long)
    long long _back_gauss               "Fortuna::back_gauss"(long long)
    long long _quantum_gauss            "Fortuna::quantum_gauss"(long long)
    long long _front_poisson            "Fortuna::front_poisson"(long long)
    long long _middle_poisson           "Fortuna::middle_poisson"(long long)
    long long _back_poisson             "Fortuna::back_poisson"(long long)
    long long _quantum_poisson          "Fortuna::quantum_poisson"(long long)
    long long _front_geometric          "Fortuna::front_geometric"(long long)
    long long _middle_geometric         "Fortuna::middle_geometric"(long long)
    long long _back_geometric           "Fortuna::back_geometric"(long long)
    long long _quantum_geometric        "Fortuna::quantum_geometric"(long long)
    long long _quantum_monty            "Fortuna::quantum_monty"(long long)
    double _canonical                   "Fortuna::generate_canonical"()
    double _random_float                "Fortuna::uniform"(double, double)


# Random Integer #
def random_below(number):
    return _randbelow(number)

def random_index(size):
    return _randindex(size)

def random_int(left_limit, right_limit):
    return _randint(left_limit, right_limit)

def random_range(start, stop=0, step=1):
    return _randrange(start, stop, step)

def d(sides=20):
    return _d(sides)

def dice(rolls=1, sides=20):
    return _dice(rolls, sides)

def ability_dice(rolls=4):
    return _ability_dice(rolls)

def plus_or_minus(number=3):
    return _plus_or_minus(number)

def plus_or_minus_linear(number=3):
    return _plus_or_minus_linear(number)


# Random Bool #
def percent_true(truth_factor=50.0) -> bool:
    return _percent_true(truth_factor) == 1


# Random Floats #
def canonical() -> float:
    return _canonical()

def random_float(a, b) -> float:
    return _random_float(a, b)


# Utilities #
def smart_clamp(target, lo, hi):
    return _smart_clamp(target, lo, hi)

def fuzzy_clamp(target, upper_bound):
    return _fuzzy_clamp(target, upper_bound)

def flatten(itm, flat=True):
    if flat is False or not callable(itm):
        return itm
    else:
        try:
            return flatten(itm())
        except TypeError:
            return itm


# Shuffle #
def shuffle(array):
    for i in reversed(range(len(array) - 1)):
        j = _randrange(i, len(array), 1)
        array[i], array[j] = array[j], array[i]

def fisher_yates(array):
    for i in reversed(range(1, len(array))):
        j = _randbelow(i + 1)
        array[i], array[j] = array[j], array[i]

def knuth(array):
    for i in range(1, len(array)):
        j = _randbelow(i + 1)
        array[i], array[j] = array[j], array[i]


# QuantumMonty Methods #
def front_gauss(size):
    return _front_gauss(size)

def middle_gauss(size):
    return _middle_gauss(size)

def back_gauss(size):
    return _back_gauss(size)

def quantum_gauss(size):
    return _quantum_gauss(size)

def front_poisson(size):
    return _front_poisson(size)

def middle_poisson(size):
    return _middle_poisson(size)

def back_poisson(size):
    return _back_poisson(size)

def quantum_poisson(size):
    return _quantum_poisson(size)

def front_linear(size):
    return _front_geometric(size)

def middle_linear(size):
    return _middle_geometric(size)

def back_linear(size):
    return _back_geometric(size)

def quantum_linear(size):
    return _quantum_geometric(size)

def quantum_monty(size):
    return _quantum_monty(size)


# Functional Value Generators #
def random_value(arr, flat=True):
    return flatten(arr[_randbelow(len(arr))], flat=flat)

def cumulative_weighted_choice(table, flat=True):
    max_weight = table[-1][0]
    rand = _randbelow(max_weight)
    for weight, value in table:
        if weight > rand:
            return flatten(value, flat=flat)

def lazy_cat(data, range_to: int = 0, fn: staticmethod = _randindex, flat=True):
    return flatten(data[fn(range_to or len(data))], flat=flat)

def truffle_shuffle(data: list, flat=True):
    result = data.pop()
    data.insert(_front_poisson(len(data)), result)
    return flatten(result, flat=flat)


# Fortuna Classes #
class TruffleShuffle:
    __slots__ = ("flat", "size", "data")

    def __init__(self, data, flat=True):
        self.flat = flat
        self.data = list(data)
        self.size = len(self.data)
        assert self.size > 0, "Input Error, Empty Container"
        shuffle(self.data)

    def __call__(self):
        return flatten(self.poisson_rotate(), self.flat)

    def poisson_rotate(self):
        result = self.data.pop()
        self.data.insert(_front_poisson(self.size), result)
        return result


class QuantumMonty:
    __slots__ = ("flat", "size", "data", "truffle_shuffle")

    def __init__(self, arr, flat=True):
        self.flat = flat
        self.data = tuple(arr)
        self.size = len(self.data)
        assert self.size > 0, "Input Error, Empty Container"
        self.truffle_shuffle = TruffleShuffle(arr, flat)

    def __call__(self):
        return self.quantum_monty()

    def dispatch(self, monty):
        return {
            "flat_uniform": self.flat_uniform,
            "truffle_shuffle": self.truffle_shuffle,
            "front_linear": self.front_linear,
            "middle_linear": self.middle_linear,
            "back_linear": self.back_linear,
            "quantum_linear": self.quantum_linear,
            "front_gauss": self.front_gauss,
            "middle_gauss": self.middle_gauss,
            "back_gauss": self.back_gauss,
            "quantum_gauss": self.quantum_gauss,
            "front_poisson": self.front_poisson,
            "middle_poisson": self.middle_poisson,
            "back_poisson": self.back_poisson,
            "quantum_poisson": self.quantum_poisson,
            "quantum_monty": self.quantum_monty,
        }[monty]

    def flat_uniform(self):
        return flatten(self.data[_randindex(self.size)], self.flat)

    def front_linear(self):
        return flatten(self.data[_front_geometric(self.size)], self.flat)

    def middle_linear(self):
        return flatten(self.data[_middle_geometric(self.size)], self.flat)

    def back_linear(self):
        return flatten(self.data[_back_geometric(self.size)], self.flat)

    def quantum_linear(self):
        return flatten(self.data[_quantum_geometric(self.size)], self.flat)

    def front_gauss(self):
        return flatten(self.data[_front_gauss(self.size)], self.flat)

    def middle_gauss(self):
        return flatten(self.data[_middle_gauss(self.size)], self.flat)

    def back_gauss(self):
        return flatten(self.data[_back_gauss(self.size)], self.flat)

    def quantum_gauss(self):
        return flatten(self.data[_quantum_gauss(self.size)], self.flat)

    def front_poisson(self):
        return flatten(self.data[_front_poisson(self.size)], self.flat)

    def middle_poisson(self):
        return flatten(self.data[_middle_poisson(self.size)], self.flat)

    def back_poisson(self):
        return flatten(self.data[_back_poisson(self.size)], self.flat)

    def quantum_poisson(self):
        return flatten(self.data[_quantum_poisson(self.size)], self.flat)

    def quantum_monty(self):
        return flatten(self.data[_quantum_monty(self.size)], self.flat)


class FlexCat:
    __slots__ = ("data", "flat", "key_bias", "val_bias", "random_cat", "random_selection")

    def __init__(self, data: dict, key_bias="front_linear", val_bias="truffle_shuffle", flat=True):
        self.data = data
        self.flat = flat
        self.key_bias = key_bias
        self.val_bias = val_bias
        self.random_cat = QuantumMonty(data.keys()).dispatch(key_bias)
        self.random_selection = {
            key: QuantumMonty(seq, flat).dispatch(val_bias) for key, seq in data.items()
        }

    def __call__(self, cat_key=None):
        return self.random_selection[cat_key if cat_key else self.random_cat()]()


class WeightedChoice:
    __slots__ = ("flat", "max_weight", "data")

    def __call__(self):
        rand = _randbelow(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return flatten(value, self.flat)


class RelativeWeightedChoice(WeightedChoice):
    __slots__ = ("flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.flat = flat
        optimized_data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)


class CumulativeWeightedChoice(WeightedChoice):
    __slots__ = ("flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.flat = flat
        data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
        prev_weight = 0
        for w_pair in data:
            w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
        optimized_data = sorted(data, key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)


def timer(func: staticmethod, *args, **kwargs):
    import time as _time
    import statistics as _statistics
    results = []
    outer_cycles = 32
    inner_cycles = 32
    for _ in range(outer_cycles):
        start = _time.time_ns()
        for _ in range(inner_cycles):
            func(*args, **kwargs)
        end = _time.time_ns()
        results.append((end - start) // inner_cycles)
    print(f"Typical Timing: {int(_statistics.median(results))} nano seconds")


def distribution(func: staticmethod, *args, num_cycles=10000, post_processor: staticmethod = None, **kwargs):
    import statistics as _statistics
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    try:
        stat_samples = results[:min(10000, num_cycles)]
        if type(stat_samples[0]) == type(""):
            stat_samples = list(map(float, stat_samples))
        ave = _statistics.mean(stat_samples)
        median_lo = _statistics.median_low(stat_samples)
        median_hi = _statistics.median_high(stat_samples)
        median = median_lo if median_lo == median_hi else (median_lo, median_hi)
        std_dev = _statistics.stdev(stat_samples, ave)
        output = (
            f" Minimum: {min(stat_samples)}",
            f" Median: {median}",
            f" Maximum: {max(stat_samples)}",
            f" Mean: {ave}",
            f" Std Deviation: {std_dev}",
        )
        print(f"Statistics of {len(stat_samples)} Samples:")
        print("\n".join(output))
    except:
        print(f"No stats available.")
    if post_processor is None:
        processed_results = results
        print(f"Distribution of {num_cycles} Samples:")
        unique_results = list(set(results))
    else:
        processed_results = list(map(post_processor, results))
        unique_results = list(set(processed_results))
        print(f"Post-processor Distribution of {num_cycles} Samples using {post_processor.__name__} method:")
    try:
        unique_results.sort()
    except TypeError:
        pass
    result_obj = {
        key: f"{processed_results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f" {key}: {val}")


def distribution_timer(func: staticmethod, *args, num_cycles=100000, label="", post_processor=None, **kwargs):
    def samples(func, *args, **kwargs):
        return f', '.join(str(func(*args, **kwargs)) for _ in range(5))

    arguments = ', '.join([str(v) for v in args] + [f'{k}={v}' for k, v in kwargs.items()])
    if label:
        print(f"Output Analysis: {label}({arguments})")
    elif hasattr(func, "__qualname__"):
        print(f"Output Distribution: {func.__qualname__}({arguments})")
    elif hasattr(func, "__name__"):
        print(f"Output Distribution: {func.__name__}({arguments})")
    else:
        print(f"Output Analysis: {func}({arguments})")
    timer(func, *args, **kwargs)
    print(f"Raw Samples: {samples(func, *args, **kwargs)}")
    distribution(func, *args, num_cycles=num_cycles, post_processor=post_processor, **kwargs)
    print("")


def quick_test(cycles=10000):
    import time as _time
    import math as _math
    import random as _random
    start_test = _time.time()
    print("\nFortuna Test Suite: RNG Storm Engine")
    value_list = [i for i in range(10)]
    print("\nRandom Values:\n")
    print("Base Case")
    distribution_timer(_random.choice, value_list, num_cycles=cycles)
    distribution_timer(random_value, value_list, num_cycles=cycles)
    truffle = TruffleShuffle(value_list)
    distribution_timer(truffle, num_cycles=cycles, label="TruffleShuffle(some_list)")
    distribution_timer(truffle_shuffle, value_list, num_cycles=cycles)  # destructive
    value_list = [i for i in range(10)]
    monty = QuantumMonty(value_list)
    distribution_timer(monty, num_cycles=cycles, label="QuantumMonty(some_list)")
    distribution_timer(lazy_cat, value_list, fn=quantum_monty)
    population = [36, 30, 24, 18]
    cum_weights = [1, 10, 100, 1000]
    rel_weights = [1, 9, 90, 900]
    print("Base Case")
    distribution_timer(_random.choices, population, cum_weights=cum_weights, num_cycles=cycles)
    cum_weighted_choice = CumulativeWeightedChoice(list(zip(cum_weights, population)))
    distribution_timer(
        cum_weighted_choice,
        num_cycles=cycles,
        label="CumulativeWeightedChoice(list(zip(cum_weights, population)))"
    )
    print("Base Case")
    distribution_timer(_random.choices, population, weights=rel_weights, num_cycles=cycles)
    rel_weighted_choice = RelativeWeightedChoice(list(zip(rel_weights, population)))
    distribution_timer(
        rel_weighted_choice,
        num_cycles=cycles,
        label="RelativeWeightedChoice(list(zip(rel_weights, population)))"
    )
    some_matrix = {"A": [1, 2, 3, 4], "B": [10, 20, 30, 40], "C": [100, 200, 300, 400]}
    flex_cat = FlexCat(some_matrix)
    distribution_timer(flex_cat, num_cycles=cycles, label="FlexCat(some_matrix)")
    print("\nRandom Integers:\n")
    print("Base Case")
    distribution_timer(_random.randrange, 10, num_cycles=cycles)
    distribution_timer(random_below, 10, num_cycles=cycles)
    distribution_timer(random_index, 10, num_cycles=cycles)
    distribution_timer(random_range, 10, num_cycles=cycles)
    distribution_timer(random_below, -10, num_cycles=cycles)
    distribution_timer(random_index, -10, num_cycles=cycles)
    distribution_timer(random_range, -10, num_cycles=cycles)
    print("Base Case")
    distribution_timer(_random.randrange, 1, 10, num_cycles=cycles)
    distribution_timer(random_range, 1, 10, num_cycles=cycles)
    distribution_timer(random_range, 10, 1, num_cycles=cycles)
    print("Base Case")
    distribution_timer(_random.randint, -5, 5, num_cycles=cycles)
    distribution_timer(random_int, -5, 5, num_cycles=cycles)
    print("Base Case")
    distribution_timer(_random.randrange, 1, 20, 2, num_cycles=cycles)
    distribution_timer(random_range, 1, 20, 2, num_cycles=cycles)
    distribution_timer(random_range, 1, 20, -2, num_cycles=cycles)
    distribution_timer(d, 10, num_cycles=cycles)
    distribution_timer(dice, 3, 6, num_cycles=cycles)
    distribution_timer(plus_or_minus, 5, num_cycles=cycles)
    distribution_timer(plus_or_minus_linear, 5, num_cycles=cycles)
    print("\nRandom Floats:\n")
    distribution_timer(canonical, post_processor=round, num_cycles=cycles)
    distribution_timer(random_float, 0.0, 10.0, post_processor=_math.floor, num_cycles=cycles)
    print("\nRandom Booleans:\n")
    distribution_timer(percent_true, 33.33, num_cycles=cycles)
    print("\nShuffle Performance Tests:")
    some_list_100 = [i for i in range(100)]
    print(f"\nBase Case: random.shuffle(some_list_{len(some_list_100)})")
    timer(_random.shuffle, some_list_100)  # destructive
    some_list_100.sort()
    print(f"\nfisher_yates(some_list_{len(some_list_100)})")
    timer(fisher_yates, some_list_100)  # destructive
    some_list_100.sort()
    print(f"\nknuth(some_list_{len(some_list_100)})")
    timer(knuth, some_list_100)  # destructive
    some_list_100.sort()
    print(f"\nshuffle(some_list_{len(some_list_100)})")
    timer(shuffle, some_list_100)  # destructive
    print()
    print("-" * 73)
    stop_test = _time.time()
    print(f"Total Test Time: {round(stop_test - start_test, 3)} seconds")
