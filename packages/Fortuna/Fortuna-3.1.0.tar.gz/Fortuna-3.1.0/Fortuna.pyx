#!python3
#distutils: language = c++
import time as _time
import math as _math
import statistics as _statistics


__all__ = (
    "TruffleShuffle", "QuantumMonty", "CumulativeWeightedChoice", "RelativeWeightedChoice", "FlexCat",
    "randbelow", "randindex", "randint", "randrange", "d", "dice", "ability_dice",
    "percent_true", "plus_or_minus", "plus_or_minus_linear",
    "binomial", "negative_binomial", "geometric", "poisson",
    "random", "uniform", "normalvariate", "lognormvariate",
    "expovariate", "vonmisesvariate", "gammavariate", "triangular",
    "gauss", "betavariate", "paretovariate", "weibullvariate",
    "extreme_value", "chi_squared", "cauchy", "fisher_f", "student_t",
    "shuffle", "knuth", "fisher_yates", "truffle_shuffle", "random_value",
    "smart_clamp", "cumulative_weighted_choice", "flatten", "lazy_cat",
    "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss", "front_poisson",
    "middle_poisson", "back_poisson", "quantum_poisson", "front_geometric",
    "middle_geometric", "back_geometric", "quantum_geometric", "quantum_monty",
    "distribution_timer", "timer",
)


cdef extern from "Fortuna.hpp":
    int       _percent_true             "Fortuna::percent_true"(double)
    long long _smart_clamp              "Fortuna::smart_clamp"(long long, long long, long long)
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
    long long _binomial                 "Fortuna::binomial"(long long, double)
    long long _negative_binomial        "Fortuna::negative_binomial"(long long, double)
    long long _geometric                "Fortuna::geometric"(double)
    long long _poisson                  "Fortuna::poisson"(double)
    double _extreme_value               "Fortuna::extreme_value"(double, double)
    double _chi_squared                 "Fortuna::chi_squared"(double)
    double _cauchy                      "Fortuna::cauchy"(double, double)
    double _fisher_f                    "Fortuna::fisher_f"(double, double)
    double _student_t                   "Fortuna::student_t"(double)
    double _random                      "Fortuna::generate_canonical"()
    double _uniform                     "Fortuna::uniform"(double, double)
    double _expovariate                 "Fortuna::expovariate"(double)
    double _gammavariate                "Fortuna::gammavariate"(double, double)
    double _weibullvariate              "Fortuna::weibullvariate"(double, double)
    double _normalvariate               "Fortuna::normalvariate"(double, double)
    double _lognormvariate              "Fortuna::lognormvariate"(double, double)
    double _betavariate                 "Fortuna::betavariate"(double, double)
    double _paretovariate               "Fortuna::paretovariate"(double)
    double _vonmisesvariate             "Fortuna::vonmisesvariate"(double, double)
    double _triangular                  "Fortuna::triangular"(double, double, double)


# Random Integer #
def randbelow(number):
    return _randbelow(number)

def randindex(size):
    return _randindex(size)

def randint(left_limit, right_limit):
    return _randint(left_limit, right_limit)

def randrange(start, stop=0, step=1):
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

def binomial(number_of_trials, probability) -> int:
    return _binomial(number_of_trials, probability)

def negative_binomial(number_of_trials, probability) -> int:
    return _negative_binomial(number_of_trials, probability)

def geometric(probability=0.5) -> int:
    return _geometric(probability)

def poisson(mean=_math.pi) -> int:
    return _poisson(mean)


# Random Bool #
def percent_true(truth_factor=50.0) -> bool:
    return _percent_true(truth_factor) == 1


# Random Floats #
def random() -> float:
    return _random()

def uniform(a, b) -> float:
    return _uniform(a, b)

def expovariate(lambd=1.0) -> float:
    return _expovariate(lambd)

def gammavariate(alpha, beta) -> float:
    return _gammavariate(alpha, beta)

def weibullvariate(alpha, beta) -> float:
    return _weibullvariate(alpha, beta)

def betavariate(alpha, beta) -> float:
    return _betavariate(alpha, beta)

def paretovariate(alpha=4.0) -> float:
    return _paretovariate(alpha)

def gauss(mu, sigma) -> float:
    return _normalvariate(mu, sigma)

def normalvariate(mu, sigma) -> float:
    return _normalvariate(mu, sigma)

def lognormvariate(mu, sigma) -> float:
    return _lognormvariate(mu, sigma)

def vonmisesvariate(mu, kappa) -> float:
    return _vonmisesvariate(mu, kappa)

def triangular(low=0.0, high=1.0, mode=0.5) -> float:
    return _triangular(low, high, mode)

def extreme_value(location, scale) -> float:
    return _extreme_value(location, scale)

def chi_squared(degrees_of_freedom=1.0) -> float:
    return _chi_squared(degrees_of_freedom)

def cauchy(location, scale) -> float:
    return _cauchy(location, scale)

def fisher_f(degrees_of_freedom_1, degrees_of_freedom_2) -> float:
    return _fisher_f(degrees_of_freedom_1, degrees_of_freedom_2)

def student_t(degrees_of_freedom=1.0) -> float:
    return _student_t(degrees_of_freedom)


# Utilities #
def smart_clamp(target, lo, hi):
    return _smart_clamp(target, lo, hi)

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

def front_geometric(size):
    return _front_geometric(size)

def middle_geometric(size):
    return _middle_geometric(size)

def back_geometric(size):
    return _back_geometric(size)

def quantum_geometric(size):
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
    __slots__ = ("arr", "data", "flat", "size")

    def __init__(self, arr, flat=True):
        self.arr = arr
        self.data = list(arr)
        self.size = len(self.data)
        assert self.size > 0, "Input Error, Empty Container"
        self.flat = flat
        shuffle(self.data)

    def __call__(self):
        return flatten(self.poisson_rotate(), self.flat)

    def __str__(self):
        return f"TruffleShuffle({self.arr})" if self.flat else f"TruffleShuffle({self.arr}, flat={self.flat})"

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
        self.truffle_shuffle = TruffleShuffle(self.data, flat)

    def __call__(self):
        return self.quantum_monty()

    def __repr__(self):
        return f"QuantumMonty({self.data})" if self.flat else f"QuantumMonty({self.data}, flat={self.flat})"

    def dispatch(self, monty):
        return {
            "uniform": self.uniform,
            "truffle_shuffle": self.truffle_shuffle,
            "front": self.front,
            "middle": self.middle,
            "back": self.back,
            "quantum": self.quantum,
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

    def uniform(self):
        return flatten(self.data[_randbelow(self.size)], self.flat)

    def front(self):
        return flatten(self.data[_front_geometric(self.size)], self.flat)

    def middle(self):
        return flatten(self.data[_middle_geometric(self.size)], self.flat)

    def back(self):
        return flatten(self.data[_back_geometric(self.size)], self.flat)

    def quantum(self):
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

    def __init__(self, data, key_bias="front", val_bias="truffle_shuffle", flat=True):
        self.data = data
        self.flat = flat
        self.key_bias = key_bias
        self.val_bias = val_bias
        self.random_cat = QuantumMonty(tuple(data.keys())).dispatch(key_bias)
        self.random_selection = {
            key: QuantumMonty(sequence, flat).dispatch(val_bias) for key, sequence in data.items()
        }

    def __call__(self, cat_key=None):
        return self.random_selection[cat_key if cat_key else self.random_cat()]()

    def __repr__(self):
        return f"FlexCat({self.data}, key_bias='{self.key_bias}', val_bias='{self.val_bias}', flat={self.flat})"


class RelativeWeightedChoice:
    __slots__ = ("weighted_table", "flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.weighted_table = weighted_table
        self.flat = flat
        optimized_data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __call__(self):
        result = self.weighted_choice()
        return flatten(result, self.flat)

    def __repr__(self):
        return f"RelativeWeightedChoice({self.weighted_table}, flat={self.flat})"

    def weighted_choice(self):
        rand = _randbelow(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value


class CumulativeWeightedChoice:
    __slots__ = ("weighted_table", "flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.weighted_table = weighted_table
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

    def __call__(self):
        result = self.weighted_choice()
        return flatten(result, self.flat)

    def __repr__(self):
        return f"CumulativeWeightedChoice({self.weighted_table}, flat={self.flat})"

    def weighted_choice(self):
        rand = _randbelow(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value


def timer(func: staticmethod, *args, **kwargs):
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


def distribution(func: staticmethod, *args, num_cycles, post_processor: staticmethod = None, **kwargs):
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
