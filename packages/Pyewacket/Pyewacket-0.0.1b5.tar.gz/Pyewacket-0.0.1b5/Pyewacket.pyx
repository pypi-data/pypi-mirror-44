#!python3
#distutils: language = c++
import time as _time
import math as _math
import statistics as _statistics 
import itertools as _itertools


__all__ = (
    "random", "uniform", "randbelow", "randint", "choice", "sample",
    "randrange", "shuffle", "normalvariate", "lognormvariate",
    "expovariate", "vonmisesvariate", "gammavariate", "triangular",
    "gauss", "betavariate", "paretovariate", "weibullvariate",
    "choices", "distribution_timer", "timer", "quick_test",
    "knuth", "fisher_yates"
)


cdef extern from "Pyewacket.hpp":
    double _generate_canonical          "Pyewacket::generate_canonical"()
    long long _random_below             "Pyewacket::random_below"(long long)
    long long _random_int               "Pyewacket::random_int"(long long, long long)
    long long _randrange                "Pyewacket::randrange"(long long, long long, int)
    double _random_float                "Pyewacket::random_float"(double, double)
    double _random_exponential          "Pyewacket::random_exponential"(double)
    double _random_gamma                "Pyewacket::random_gamma"(double, double)
    double _random_weibull              "Pyewacket::random_weibull"(double, double)
    double _random_normal               "Pyewacket::random_normal"(double, double)
    double _random_log_normal           "Pyewacket::random_log_normal"(double, double)
    double _betavariate                 "Pyewacket::betavariate"(double, double)
    double _paretovariate               "Pyewacket::paretovariate"(double)
    double _vonmisesvariate             "Pyewacket::vonmisesvariate"(double, double)
    double _triangular                  "Pyewacket::triangular"(double, double, double)


# RANDOM VALUE #
def choice(seq):
    if len(seq) == 0:
        return None
    return seq[_random_below(len(seq))]

def fisher_yates(array):
    for i in reversed(range(1, len(array))):
        j = _random_below(i + 1)
        array[i], array[j] = array[j], array[i]

def knuth(array):
    for i in range(1, len(array)):
        j = _random_below(i + 1)
        array[i], array[j] = array[j], array[i]

def shuffle(array):
    for i in reversed(range(len(array) - 1)):
        j = _randrange(i, len(array), 1)
        array[i], array[j] = array[j], array[i]

def _cumulative_weighted_choice(pop, weights):
    max_weight = weights[-1]
    rand = _random_below(max_weight)
    for weight, value in zip(weights, pop):
        if weight > rand:
            return value

def choices(population, weights=None, *, cum_weights=None, k=1):
    if not weights and not cum_weights:
        return [choice(population) for _ in range(k)]
    if not cum_weights:
        cum_weights = list(_itertools.accumulate(weights))
    assert len(cum_weights) == len(population), "The number of weights does not match the population"
    return [_cumulative_weighted_choice(population, cum_weights) for _ in range(k)]

def sample(population, k):
    n = len(population)
    assert 0 < k <= n, "Sample larger than population or is negative"
    if k == 1:
        return [choice(population)]
    elif k == n or k >= n // 2:
        result = list(population)
        shuffle(result)
        return result[:k]
    else:
        result = [None] * k
        selected = set()
        selected_add = selected.add
        for i in range(k):
            j = randbelow(n)
            while j in selected:
                j = randbelow(n)
            selected_add(j)
            result[i] = population[j]
        return result


# RANDOM INTEGER #
def randbelow(a) -> int:
    return _random_below(a)

def randint(a, b) -> int:
    return _random_int(a, b)

def randrange(start, stop=0, step=1) -> int:
    return _randrange(start, stop, step)


# RANDOM FLOATING POINT #
def random() -> float:
    return _generate_canonical()

def uniform(a, b) -> float:
    return _random_float(a, b)

def expovariate(lambd) -> float:
    return _random_exponential(lambd)

def gammavariate(alpha, beta) -> float:
    return _random_gamma(alpha, beta)

def weibullvariate(alpha, beta) -> float:
    return _random_weibull(alpha, beta)

def betavariate(alpha, beta) -> float:
    return _betavariate(alpha, beta)

def paretovariate(alpha) -> float:
    return _paretovariate(alpha)

def gauss(mu, sigma) -> float:
    return _random_normal(mu, sigma)

def normalvariate(mu, sigma) -> float:
    return _random_normal(mu, sigma)

def lognormvariate(mu, sigma) -> float:
    return _random_log_normal(mu, sigma)

def vonmisesvariate(mu, kappa) -> float:
    return _vonmisesvariate(mu, kappa)

def triangular(low=0.0, high=1.0, mode=0.5) -> float:
    return _triangular(low, high, mode)


# DISTRIBUTION & PERFORMANCE TEST SUITE #
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
    output = (
        f"Min: {min(results)}ns",
        f"Mid: {int(_statistics.median(results))}ns",
        f"Max: {max(results)}ns",
    )
    print(f"Approximate Single Execution Time: {', '.join(output)}")


def distribution(func: staticmethod, *args, num_cycles, post_processor=None, **kwargs):
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    print(f"Test Samples: {num_cycles}")
    ave = _statistics.mean(results)
    median_lo = _statistics.median_low(results)
    median_hi = _statistics.median_high(results)
    median = median_lo if median_lo == median_hi else (median_lo, median_hi)
    std_dev = _statistics.stdev(results, ave)
    output = (
        f" Minimum: {min(results)}",
        f" Median: {median}",
        f" Maximum: {max(results)}",
        f" Mean: {ave}",
        f" Std Deviation: {std_dev}",
    )
    if post_processor is None:
        print("Sample Statistics:")
        print("\n".join(output))
        processed_results = results
        unique_results = list(set(results))
        print(f"Sample Distribution:")
    else:
        print("Pre-processor Statistics:")
        print("\n".join(output))
        processed_results = list(map(post_processor, results))
        unique_results = list(set(processed_results))
        print(f"Post-processor Distribution using {post_processor.__name__} method:")
    unique_results.sort()
    result_obj = {
        key: f"{processed_results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f" {key}: {val}")


def distribution_timer(func: staticmethod, *args, num_cycles=10000, label="", post_processor=None, **kwargs):
    def _samples(func, *args, **kwargs):
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
    print(f"Raw Samples: {_samples(func, *args, **kwargs)}")
    distribution(func, *args, num_cycles=num_cycles, post_processor=post_processor, **kwargs)
    print("")


def quick_test():
    import random as _random
    R = _random.Random()
    print("\nPyewacket Distribution & Performance Test Suite\n")
    start_test = _time.time()

    distribution_timer(R._randbelow, 10)
    distribution_timer(randbelow, 10)
    distribution_timer(_random.randint, 1, 10)
    distribution_timer(randint, 1, 10)
    distribution_timer(_random.randrange, 0, 10, 2)
    distribution_timer(randrange, 0, 10, 2)
    distribution_timer(_random.random, post_processor=_math.floor)
    distribution_timer(random, post_processor=_math.floor)
    distribution_timer(_random.uniform, 0.0, 10.0, post_processor=_math.floor)
    distribution_timer(uniform, 0.0, 10.0, post_processor=_math.floor)
    distribution_timer(_random.expovariate, 1.0, post_processor=_math.floor)
    distribution_timer(expovariate, 1.0, post_processor=_math.floor)
    distribution_timer(_random.gammavariate, 2.0, 1.0, post_processor=round)
    distribution_timer(gammavariate, 2.0, 1.0, post_processor=round)
    distribution_timer(_random.weibullvariate, 1.0, 1.0, post_processor=_math.floor)
    distribution_timer(weibullvariate, 1.0, 1.0, post_processor=_math.floor)
    distribution_timer(_random.betavariate, 3.0, 3.0, post_processor=round)
    distribution_timer(betavariate, 3.0, 3.0, post_processor=round)
    distribution_timer(_random.paretovariate, 4.0, post_processor=_math.floor)
    distribution_timer(paretovariate, 4.0, post_processor=_math.floor)
    distribution_timer(_random.gauss, 1.0, 1.0, post_processor=round)
    distribution_timer(gauss, 1.0, 1.0, post_processor=round)
    distribution_timer(_random.normalvariate, 0.0, 2.8, post_processor=round)
    distribution_timer(normalvariate, 0.0, 2.8, post_processor=round)
    distribution_timer(_random.lognormvariate, 0.0, 0.5, post_processor=round)
    distribution_timer(lognormvariate, 0.0, 0.5, post_processor=round)
    distribution_timer(_random.vonmisesvariate, 0, 0, post_processor=_math.floor)
    distribution_timer(vonmisesvariate, 0, 0, post_processor=_math.floor)
    distribution_timer(_random.triangular, 0.0, 10.0, 0.0, post_processor=_math.floor)
    distribution_timer(triangular, 0.0, 10.0, 0.0, post_processor=_math.floor)
    some_list = [i for i in range(10)]
    distribution_timer(_random.choice, some_list)
    distribution_timer(choice, some_list)
    weights = [i for i in reversed(range(1, 11))]
    distribution_timer(_random.choices, some_list, weights, k=3)
    distribution_timer(choices, some_list, weights, k=3)
    cum_weights = list(_itertools.accumulate(weights))
    distribution_timer(_random.choices, some_list, cum_weights=cum_weights, k=3)
    distribution_timer(choices, some_list, cum_weights=cum_weights, k=3)
    print(f"Timer only: _random.shuffle(some_list) of size {len(some_list)}:")
    timer(_random.shuffle, some_list)
    print()
    print(f"Timer only: shuffle(some_list) of size {len(some_list)}:")
    timer(shuffle, some_list)
    print()
    print(f"Timer only: knuth(some_list) of size {len(some_list)}:")
    timer(knuth, some_list)
    print()
    print(f"Timer only: fisher_yates(some_list) of size {len(some_list)}:")
    timer(fisher_yates, some_list)
    print()
    some_list.sort()
    distribution_timer(_random.sample, some_list, k=3)
    distribution_timer(sample, some_list, k=3)

    stop_test = _time.time()
    print(f"\nTotal Test Time: {round(stop_test - start_test, 4)} sec")
