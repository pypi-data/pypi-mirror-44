# Pyewacket
### Fast, fault-tolerant, drop-in replacement for the Python3 random module

Built atop the RNG Storm Engine for proven stability and performance. While Storm is a high quality random engine, Pyewacket is not appropriate for cryptography of any kind. Pyewacket is meant for games, data science, A.I. and experimental programming, not security.


**Recommended Installation:** `$ pip install Pyewacket`


### Pyewacket serves three main goals:
1. Provide a feature rich and familiar API for generating random numbers and values.
    - Faithful to the random module API, but not a slave to it.
2. Go fast!
    - The RNG Storm Engine is an order of magnitude faster on average.
3. Fix things. Random.random is NOT broken, however it's not fault tolerant or fast.
    - Exceptions that can be avoided with balance, symmetry and sound mathematics, will be avoided. New behavior will be implemented as needed, but new math will not be invented.
    - Do or do not, there is no try/except. Alright, sometimes `try:` is useful, but it's only needed in truly exceptional cases where lambda calculus fails.
    - All class methods will be implemented as free functions when possible.


## Random Integers
- `Pyewacket.randbelow(n: int) -> int`
    - While randrange(a, b, c) can be handy, it's more complex than needed most of the time. Mathematically, randbelow(n) is equivalent to randrange(n) and they have nearly the same performance characteristics in Pyewacket, 10x - 12x faster than the random module's internal randbelow().
    - @param n :: Pyewacket expands the acceptable input domain to include non-positive values of n.
    - @return :: random integer in range (n, 0] or [0, n) depending on the sign of n.
    - Analytic Continuation about zero is used to achieve full input domain coverage for any function that normally can only take positive, non-zero values as input.
    - Symmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n) if n < 0 else 0` (this is how it works now).
    - The lambda is not the actual implementation, but it represents the idea of AC pretty well. AC will invert the meaning of a function for negative input. Thus turning _randbelow_ into _randabove_ for all negative values of n.

_It is possible that an asymmetric AC would be a better match to how negative numbers work as reverse list indexes in python._

Asymmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n)-1 if n < 0 else None` (this is how it could work).

_This would allow_ `some_list[randbelow(-n)]` _to range over the last n items in a list of size n or larger. The interesting part is that you wouldn't need to know the exact size of the list. Let me know if you think this is a good idea._

```python
from Pyewacket import randbelow


""" Standard """
randbelow(10)       # -> [0, 10)

""" Extras """
randbelow(0)        # -> [0, 0) => 0
randbelow(-10)      # -> (-10, 0]
```

- `Pyewacket.randint(a: int, b: int) -> int`
    - @param a, b :: both are required,
    - @return :: random integer in range [a, b] or [b, a]
    - Inclusive on both sides
    - Removed the asymmetric requirement of a < b
    - When a == b returns a

```python
from Pyewacket import randint


""" Standard """
randint(1, 10)      # -> [1, 10]

""" Extras """
randint(10, 1)      # -> [1, 10]
randint(10, 10)     # -> [10, 10] => 10
```

- `Pyewacket.randrange(start: int, stop: int = 0, step: int = 1) -> int`
    - Fault tolerant and about 20x faster than random.randrange()
    - @param start :: required
    - @param stop :: optional, default=0
    - @parma step :: optional, default=1
    - @return :: random integer in range (stop, start] or [start, stop) by |step|
    - Removed the requirements of start < stop, and step > 0
    - Always returns start for start == stop or step == 0
    - Always inclusive on the lowest side exclusive on the higher side.
    - Ignores sign of step, but it could be a trigger for reversing the inclusivity rule.

```python
from Pyewacket import randrange


""" Standard """
randrange(10)           # -> [0, 10) by whole numbers
randrange(1, 10)        # -> [1, 10) by whole numbers
randrange(1, 10, 2)     # -> [1, 10) by 2, odd numbers

""" Extras """
randrange(0)            # -> [0, 0) -> 0
randrange(-10)          # -> [-10, 0) by 1
randrange(10, 1)        # -> [1, 10) by 1
randrange(10, 0, 2)     # -> [0, 10) by 2, even numbers
randrange(10, 10, 0)    # -> [10, 10) => 10
```

## Random Floating Point
- `Pyewacket.random() -> float`
    - random float in range [0.0, 1.0] or [0.0, 1.0) depending on rounding.
    - This is the only function that doesn't show a performance increase, as expected.
    - Roughly the same speed as random.random()
- `Pyewacket.uniform(a: float, b: float) -> float`
    - random float in [a, b] or [a, b) depending on rounding
    - 4x faster
- `Pyewacket.expovariate(lambd: float) -> float`
    - 5x faster
- `Pyewacket.gammavariate(alpha, beta) -> float`
    - 10x faster
- `Pyewacket.weibullvariate(alpha, beta) -> float`
    - 4x faster
- `Pyewacket.betavariate(alpha, beta) -> float`
    - 16x faster
- `Pyewacket.paretovariate(alpha) -> float`
    - 4x faster
- `Pyewacket.gauss(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.normalvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.lognormvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.vonmisesvariate(mu: float, kappa: float) -> float`
    - 4x faster
- `Pyewacket.triangular(low: float, high: float, mode: float = None)`
    - 10x faster

## Random Sequence Values
- `Pyewacket.choice(seq: List) -> Value`
    - An order of magnitude faster than random.choice().
    - @param seq :: any zero indexed object like a list or tuple.
    - @return :: random value from the list, can be any object type that can be put into a list.
- `Pyewacket.choices(population, weights=None, *, cum_weights=None, k=1)`
    - @param population :: data values
    - @param weights :: relative weights
    - @param cum_weights :: cumulative weights
    - @param k :: number of samples to be collected
    - Only seeing a 2x performance gain.
- `Pyewacket.cumulative_weighted_choice(table, k=1)`
    - 10x faster than choices, but radically different API and a bit less flexible.
    - Supports Cumulative Weights only. Convert relative weights to cumulative if needed: `cum_weights = tuple(itertools.accumulate(rel_weights))`
    - @param table :: two dimensional list or tuple of weighted value pairs. `[(1, "a"), (10, "b"), (100, "c")...]`
        - The table can be constructed as `tuple(zip(cum_weights, population))` weights always come first.
    - @param k :: number of samples to be collected. Returns a list of size k if k > 1, otherwise returns a single value - not a list of one.
- `Pyewacket.shuffle(array: list) -> None`
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 20 times faster than random.shuffle().
    - Implements Knuth B Shuffle Algorithm. Knuth B is twice as fast as Knuth A or Fisher-Yates for every test case. This is likely due to the combination of walking backward and rotating backward into the back side of the list. With this combination it can never modify the data it still needs to walk through. Fresh snow all the way home, aka very low probability for cache misses.
- `Pyewacket.knuth(array: list) -> None`, shuffle alternate.
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 10 times faster than random.shuffle().
    - Original Knuth Shuffle Algorithm.
    - Walks forward and rotates backward, but to the front side of the list.
- `Pyewacket.fisher_yates(array: list) -> None`, shuffle alternate.
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 10 times faster than random.shuffle().
    - Fisher-Yates Shuffle Algorithm. Used in random.shuffle().
    - Walks backward and rotates forward, into oncoming traffic.
- `Pyewacket.sample(population: List, k: int) -> list`
    - @param population :: list or tuple.
    - @param k :: number of unique samples to get.
    - @return :: size k list of unique random samples.
    - Performance gains range (5x to 20x) depending on len(population) and the ratio of k to len(population). Higher performance gains are seen when k ~= pop size.

## Seeding
- `set_seed(seed: int=0) -> None`
    - Hardware seeding is enabled by default.
    - This function is used to turn on/off software seeding and set or reset the engine seed.
    - @param seed :: any non-zero positive integer less than 2**63 enables software seeding.
    - Calling `set_seed()` or `set_seed(0)` will turn off software seeding and re-enable hardware seeding.
    - While you can toggle software seeding on and off and re-seed the engine at will without error, this function is **not intended or optimized to be used in a loop**. General rule: seed once, or better yet, not at all. Typically, software seeding is for research and development, hardware seeding for the real thing.
    - This setting affects all random functions in the module.

## Testing Suite
- `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - For the statistical analysis of a non-deterministic numeric output function.
    - @param func :: function, method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles=10000 :: Total number of samples to use for analysis.
    - @optional_kw post_processor=None :: Used to scale a large set of data into a smaller set of groupings for better visualization of the data, esp. useful for distributions of floats. For many functions in quick_test(), math.floor() is used, for others round() is more appropriate. For more complex post processing - lambdas work nicely. Post processing only affects the distribution, the statistics and performance results are unaffected.
- `quick_test()`
    - Runs a battery of tests for every random distribution function in the module.


## Development Log
##### Pyewacket 1.0.2
- added choices alternative `cumulative_weighted_choice`

##### Pyewacket 1.0.1
- minor typos

##### Pyewacket 1.0.0
- Storm 2 Rebuild.

##### Pyewacket 0.1.22
- Small bug fix.

##### Pyewacket 0.1.21
- Public Release

##### Pyewacket 0.0.2b1
- Added software seeding.

##### Pyewacket v0.0.1b8
- Fixed a small bug in the tests.

##### Pyewacket v0.0.1b7
- Engine Fine Tuning
- Fixed some typos.

##### Pyewacket v0.0.1b6
- Rearranged tests to be more consistent and match the documentation.

##### Pyewacket v0.0.1b5
- Documentation Upgrade
- Minor Performance Tweaks

##### Pyewacket v0.0.1b4
- Public Beta

##### Pyewacket v0.0.1b3
- quick_test()
- Extended Functionality
    - sample()
    - expovariate()
    - gammavariate()
    - weibullvariate()
    - betavariate()
    - paretovariate()
    - gauss()
    - normalvariate()
    - lognormvariate()
    - vonmisesvariate()
    - triangular()

##### Pyewacket v0.0.1b2
- Basic Functionality
    - random()
    - uniform()
    - randbelow()
    - randint()
    - randrange()
    - choice()
    - choices()
    - shuffle()

##### Pyewacket v0.0.1b1
- Initial Design & Planning


## Pywacket Distribution and Performance Test Suite
```
>>> from Pyewacket import quick_test
>>> quick_test()

Pyewacket Distribution & Performance Test Suite

Software seed test passed: True
Hardware seed test passed: True

Output Distribution: Random._randbelow(10)
Approximate Single Execution Time: Min: 656ns, Mid: 718ns, Max: 906ns
Raw Samples: 9, 3, 8, 8, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5216
 Std Deviation: 2.8611801892239366
Sample Distribution:
 0: 9.52%
 1: 10.08%
 2: 10.19%
 3: 9.68%
 4: 10.15%
 5: 10.39%
 6: 10.08%
 7: 9.93%
 8: 9.7%
 9: 10.28%

Output Distribution: randbelow(10)
Approximate Single Execution Time: Min: 62ns, Mid: 77ns, Max: 218ns
Raw Samples: 1, 3, 1, 6, 7
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: (4, 5)
 Maximum: 9
 Mean: 4.5171
 Std Deviation: 2.8819677589828068
Sample Distribution:
 0: 10.0%
 1: 10.08%
 2: 9.52%
 3: 10.16%
 4: 10.24%
 5: 9.97%
 6: 9.79%
 7: 9.77%
 8: 10.06%
 9: 10.41%

Output Distribution: Random.randint(1, 10)
Approximate Single Execution Time: Min: 1281ns, Mid: 1312ns, Max: 2500ns
Raw Samples: 1, 9, 8, 4, 10
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.5291
 Std Deviation: 2.8741223439381964
Sample Distribution:
 1: 9.92%
 2: 9.55%
 3: 10.38%
 4: 10.01%
 5: 9.48%
 6: 10.18%
 7: 10.12%
 8: 10.0%
 9: 10.21%
 10: 10.15%

Output Distribution: randint(1, 10)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 2, 1, 4, 2, 10
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4732
 Std Deviation: 2.877691760940893
Sample Distribution:
 1: 10.1%
 2: 10.28%
 3: 10.1%
 4: 10.16%
 5: 9.61%
 6: 10.1%
 7: 9.96%
 8: 9.75%
 9: 10.05%
 10: 9.89%

Output Distribution: Random.randrange(0, 10, 2)
Approximate Single Execution Time: Min: 1312ns, Mid: 1375ns, Max: 1593ns
Raw Samples: 0, 8, 8, 2, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 3.9476
 Std Deviation: 2.8475366699146565
Sample Distribution:
 0: 21.11%
 2: 19.43%
 4: 20.36%
 6: 19.17%
 8: 19.93%

Output Distribution: randrange(0, 10, 2)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 125ns
Raw Samples: 4, 2, 0, 2, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.0248
 Std Deviation: 2.838483866268383
Sample Distribution:
 0: 19.97%
 2: 19.93%
 4: 19.24%
 6: 20.61%
 8: 20.25%

Output Distribution: Random.random()
Approximate Single Execution Time: Min: 31ns, Mid: 31ns, Max: 93ns
Raw Samples: 0.31528056140407834, 0.744339737601912, 0.14308910472659087, 0.13225237713435556, 0.29029456374592133
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 2.2993301147522516e-06
 Median: (0.5017498777658539, 0.5018868812445354)
 Maximum: 0.9999859140274494
 Mean: 0.5015693669829079
 Std Deviation: 0.289246160009484
Post-processor Distribution using round method:
 0: 49.81%
 1: 50.19%

Output Distribution: random()
Approximate Single Execution Time: Min: 31ns, Mid: 31ns, Max: 93ns
Raw Samples: 0.7862459129229514, 0.29614802331132417, 0.5890078290204439, 0.2721487462379972, 0.7593073051158257
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 6.577797384189096e-05
 Median: (0.48919927733006946, 0.48929476102571107)
 Maximum: 0.9999783625053182
 Mean: 0.49438492826410696
 Std Deviation: 0.2902018723361404
Post-processor Distribution using round method:
 0: 51.09%
 1: 48.91%

Output Distribution: Random.uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 218ns, Mid: 218ns, Max: 343ns
Raw Samples: 2.8253405218545904, 2.65591902068103, 1.1379286037757064, 0.2616272197773184, 5.579598956970569
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00019217791808689988
 Median: (5.01337652173627, 5.014089755304411)
 Maximum: 9.999605788711936
 Mean: 5.011253880845686
 Std Deviation: 2.882648299724978
Post-processor Distribution using floor method:
 0: 9.76%
 1: 10.16%
 2: 10.02%
 3: 9.72%
 4: 10.18%
 5: 9.79%
 6: 9.79%
 7: 10.79%
 8: 9.81%
 9: 9.98%

Output Distribution: uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 312ns
Raw Samples: 7.833106241307898, 5.750098889970081, 5.205503206579142, 6.266278239954075, 6.893788136728646
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0007913968324131491
 Median: (4.950050751520916, 4.950855201146594)
 Maximum: 9.99996140462822
 Mean: 4.9668271092805405
 Std Deviation: 2.9013936191898932
Post-processor Distribution using floor method:
 0: 10.64%
 1: 10.06%
 2: 9.55%
 3: 10.2%
 4: 10.1%
 5: 9.91%
 6: 10.06%
 7: 9.57%
 8: 9.98%
 9: 9.93%

Output Distribution: Random.expovariate(1.0)
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 468ns
Raw Samples: 0.8100846184320697, 2.844124783061014, 0.7186770403644827, 0.5371306140592526, 0.39016029600706786
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 3.3680452109253656e-05
 Median: (0.6961056363869809, 0.6964335515694839)
 Maximum: 11.274504242442951
 Mean: 1.005983204034866
 Std Deviation: 1.0070364877901028
Post-processor Distribution using floor method:
 0: 62.55%
 1: 23.79%
 2: 8.65%
 3: 3.12%
 4: 1.24%
 5: 0.41%
 6: 0.13%
 7: 0.06%
 8: 0.02%
 9: 0.01%
 11: 0.02%

Output Distribution: expovariate(1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 125ns
Raw Samples: 0.39140460191181425, 0.60492422337449, 1.9491433406918877, 1.4592816509114233, 0.2618174750863953
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.5812866589580206e-06
 Median: (0.7051660546340411, 0.7054354158048711)
 Maximum: 8.041505519446739
 Mean: 1.0039571287630213
 Std Deviation: 0.990937141037189
Post-processor Distribution using floor method:
 0: 62.68%
 1: 23.77%
 2: 8.64%
 3: 3.22%
 4: 1.14%
 5: 0.31%
 6: 0.13%
 7: 0.09%
 8: 0.02%

Output Distribution: Random.gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 1031ns, Mid: 1218ns, Max: 1531ns
Raw Samples: 1.616004382949616, 0.5735885713320485, 2.7060903886676626, 0.726760037072414, 0.555242643924503
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.006560511040216764
 Median: (1.6995138663412561, 1.699897837637127)
 Maximum: 14.149138468435007
 Mean: 1.999902499449295
 Std Deviation: 1.3922521773655911
Post-processor Distribution using round method:
 0: 8.84%
 1: 34.55%
 2: 27.98%
 3: 15.33%
 4: 7.69%
 5: 3.22%
 6: 1.31%
 7: 0.64%
 8: 0.24%
 9: 0.1%
 10: 0.06%
 11: 0.02%
 13: 0.01%
 14: 0.01%

Output Distribution: gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 281ns
Raw Samples: 1.226212578955946, 2.8116221047588055, 1.46842036391775, 2.8342118492602295, 1.832181996186121
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00553721814500252
 Median: (1.6728097866304112, 1.673391257220827)
 Maximum: 13.493693397815974
 Mean: 2.0105219235382448
 Std Deviation: 1.4452096267514964
Post-processor Distribution using round method:
 0: 9.51%
 1: 34.33%
 2: 27.43%
 3: 14.68%
 4: 7.87%
 5: 3.44%
 6: 1.68%
 7: 0.49%
 8: 0.32%
 9: 0.09%
 10: 0.03%
 11: 0.08%
 12: 0.03%
 13: 0.02%

Output Distribution: Random.weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 406ns, Mid: 437ns, Max: 750ns
Raw Samples: 1.9444323085079667, 0.31481821317260433, 0.34974141238032874, 5.125286989527184, 1.393222847155887
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 6.0782117450054174e-05
 Median: (0.6950241523721332, 0.6956820866198715)
 Maximum: 9.391404011436286
 Mean: 1.0033108849541996
 Std Deviation: 1.0004529228245675
Post-processor Distribution using floor method:
 0: 63.54%
 1: 22.61%
 2: 9.01%
 3: 3.0%
 4: 1.13%
 5: 0.5%
 6: 0.11%
 7: 0.07%
 8: 0.02%
 9: 0.01%

Output Distribution: weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 281ns
Raw Samples: 0.39274175534583455, 0.19621474091513244, 0.950647394061098, 0.6732281365432452, 0.40686233023650875
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 8.65451575787426e-05
 Median: (0.6995721085817146, 0.6995726638584434)
 Maximum: 7.9587796554702415
 Mean: 1.0185987533011704
 Std Deviation: 1.005664594531231
Post-processor Distribution using floor method:
 0: 62.52%
 1: 22.94%
 2: 9.44%
 3: 3.3%
 4: 1.12%
 5: 0.45%
 6: 0.16%
 7: 0.07%

Output Distribution: Random.betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 2531ns, Mid: 2718ns, Max: 3187ns
Raw Samples: 0.3324837789751726, 0.5756131013754017, 0.5152344251561055, 0.5464435505616928, 0.7104967540990113
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.023466116335796136
 Median: (0.4980018876743779, 0.49813457848866954)
 Maximum: 0.9652492969474086
 Mean: 0.49985022835291437
 Std Deviation: 0.18719559884859643
Post-processor Distribution using round method:
 0: 50.28%
 1: 49.72%

Output Distribution: betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 281ns
Raw Samples: 0.7533633207918022, 0.2616057770093243, 0.7079812085995301, 0.6201105283974119, 0.623261049414648
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.01303677698207687
 Median: (0.49438910641698786, 0.49445854832832153)
 Maximum: 0.967714046157308
 Mean: 0.4963388530005871
 Std Deviation: 0.18896401006674032
Post-processor Distribution using round method:
 0: 50.99%
 1: 49.01%

Output Distribution: Random.paretovariate(4.0)
Approximate Single Execution Time: Min: 281ns, Mid: 281ns, Max: 500ns
Raw Samples: 1.3563578105195548, 1.0616403721373924, 1.187711304585734, 1.1790829426869378, 2.196627024069017
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000331814241858
 Median: (1.1933898906850828, 1.1934172758560422)
 Maximum: 14.602778847050033
 Mean: 1.340943123604167
 Std Deviation: 0.4949558794139725
Post-processor Distribution using floor method:
 1: 93.68%
 2: 4.92%
 3: 0.95%
 4: 0.29%
 5: 0.05%
 6: 0.06%
 7: 0.01%
 8: 0.01%
 10: 0.02%
 14: 0.01%

Output Distribution: paretovariate(4.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 656ns
Raw Samples: 1.0615315749881427, 1.3091901557971348, 1.1808465274177824, 1.4924707570187064, 2.158144566235785
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.000037713999518
 Median: (1.1895305240320464, 1.1895675309416607)
 Maximum: 12.769916098885531
 Mean: 1.329586891824582
 Std Deviation: 0.45434265637229904
Post-processor Distribution using floor method:
 1: 93.7%
 2: 5.15%
 3: 0.83%
 4: 0.23%
 5: 0.04%
 6: 0.02%
 9: 0.01%
 10: 0.01%
 12: 0.01%

Output Distribution: Random.gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 593ns, Mid: 593ns, Max: 843ns
Raw Samples: 1.1964333325561947, 1.0747219487610578, 3.325442517082133, 0.14059516957622398, 0.29212209876269934
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.7499207592428414
 Median: (0.9794973716555295, 0.9797406171303447)
 Maximum: 4.6334060487340665
 Mean: 0.9908316117136992
 Std Deviation: 1.0061001015383937
Post-processor Distribution using round method:
 -3: 0.01%
 -2: 0.6%
 -1: 6.22%
 0: 24.69%
 1: 38.27%
 2: 23.3%
 3: 6.3%
 4: 0.6%
 5: 0.01%

Output Distribution: gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 343ns
Raw Samples: 3.156954209763295, -0.9413372633301956, 1.0850140979275613, 0.1002817931164238, -0.5406757789697574
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.755080377593199
 Median: (1.0163583620423828, 1.0165031746316824)
 Maximum: 4.826204415294271
 Mean: 1.0182545100974172
 Std Deviation: 1.0024976677382196
Post-processor Distribution using round method:
 -3: 0.03%
 -2: 0.73%
 -1: 5.87%
 0: 23.19%
 1: 38.51%
 2: 24.79%
 3: 6.28%
 4: 0.57%
 5: 0.03%

Output Distribution: Random.normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 593ns, Mid: 750ns, Max: 1687ns
Raw Samples: -1.6892260153386678, -2.9064868915946533, -1.168935375125028, 1.5650947967504776, -4.809635870588835
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -11.679755802269945
 Median: (0.04981160392161433, 0.0513863167077832)
 Maximum: 12.264392460348775
 Mean: 0.02341436715129368
 Std Deviation: 2.7962063600593456
Post-processor Distribution using round method:
 -12: 0.01%
 -11: 0.02%
 -10: 0.01%
 -9: 0.08%
 -8: 0.31%
 -7: 0.77%
 -6: 1.39%
 -5: 2.67%
 -4: 4.94%
 -3: 8.17%
 -2: 10.79%
 -1: 12.83%
 0: 14.75%
 1: 13.26%
 2: 11.28%
 3: 8.44%
 4: 4.87%
 5: 3.02%
 6: 1.4%
 7: 0.62%
 8: 0.23%
 9: 0.07%
 10: 0.05%
 11: 0.01%
 12: 0.01%

Output Distribution: normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 187ns
Raw Samples: -0.500887622724255, 2.538707423900157, -0.24046587915642553, -2.617192410749793, 0.1860402668124976
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -10.248558331496726
 Median: (-0.07328451518856201, -0.07279223180013734)
 Maximum: 10.646195281405143
 Mean: -0.054657186584510666
 Std Deviation: 2.812280584434887
Post-processor Distribution using round method:
 -10: 0.02%
 -9: 0.12%
 -8: 0.25%
 -7: 0.64%
 -6: 1.71%
 -5: 2.83%
 -4: 5.18%
 -3: 8.41%
 -2: 11.41%
 -1: 13.62%
 0: 13.59%
 1: 13.13%
 2: 10.75%
 3: 8.08%
 4: 4.95%
 5: 2.88%
 6: 1.41%
 7: 0.61%
 8: 0.33%
 9: 0.06%
 10: 0.01%
 11: 0.01%

Output Distribution: Random.lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 781ns, Mid: 875ns, Max: 1312ns
Raw Samples: 2.3768849269838745, 1.1272529919924952, 1.6279028975608976, 0.6658979568051446, 1.5490988983423875
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.15973228647917964
 Median: (0.9961170399092433, 0.9961573129982354)
 Maximum: 6.972823159915241
 Mean: 1.1281333294455964
 Std Deviation: 0.5970281117872499
Post-processor Distribution using round method:
 0: 7.92%
 1: 71.72%
 2: 17.03%
 3: 2.74%
 4: 0.5%
 5: 0.07%
 6: 0.01%
 7: 0.01%

Output Distribution: lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 1500ns
Raw Samples: 0.4327642394180456, 0.6701903739640152, 0.42521053389180624, 0.6770413394835729, 1.5293519166631733
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.14558133399210837
 Median: (0.9937107546673942, 0.9941704422667589)
 Maximum: 5.823104508852624
 Mean: 1.1267698119156924
 Std Deviation: 0.6010459560638869
Post-processor Distribution using round method:
 0: 8.53%
 1: 70.78%
 2: 17.59%
 3: 2.45%
 4: 0.5%
 5: 0.12%
 6: 0.03%

Output Distribution: Random.vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 250ns, Mid: 250ns, Max: 375ns
Raw Samples: 3.424441892500175, 0.42513283987181866, 0.010891164578754435, 1.0382269353663451, 5.823749387633274
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00019875214514018666
 Median: (3.1103840729355605, 3.11084229154385)
 Maximum: 6.282188723984206
 Mean: 3.1426267391363183
 Std Deviation: 1.8059723757857922
Post-processor Distribution using floor method:
 0: 15.5%
 1: 15.97%
 2: 16.67%
 3: 15.55%
 4: 15.95%
 5: 16.0%
 6: 4.36%

Output Distribution: vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 343ns
Raw Samples: 3.86374178898162, 5.360552250407766, 5.26770676665571, 5.553784083810001, 3.079462436096574
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.000297288916636765
 Median: (3.1349113301176788, 3.134986358724474)
 Maximum: 6.282876333102897
 Mean: 3.1379556330120093
 Std Deviation: 1.8205639874699495
Post-processor Distribution using floor method:
 0: 16.5%
 1: 14.88%
 2: 16.45%
 3: 15.79%
 4: 16.11%
 5: 15.65%
 6: 4.62%

Output Distribution: Random.triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 468ns, Mid: 484ns, Max: 593ns
Raw Samples: 7.059414727498093, 4.548801195814587, 4.544657793393938, 0.9263903440623782, 1.9338554964753722
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00023432243818533038
 Median: (2.9880514718720494, 2.9891842606693455)
 Maximum: 9.91693872302925
 Mean: 3.3724559412813075
 Std Deviation: 2.36397683215762
Post-processor Distribution using floor method:
 0: 18.6%
 1: 16.82%
 2: 14.71%
 3: 13.1%
 4: 11.62%
 5: 8.63%
 6: 7.26%
 7: 5.13%
 8: 3.07%
 9: 1.06%

Output Distribution: triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 2.6450495127973106, 5.7176686496760025, 1.0090863481980472, 5.552808111008735, 0.10452504066469137
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 3.387312032976375e-05
 Median: (2.9287933054652617, 2.9291053413628876)
 Maximum: 9.992588067073637
 Mean: 3.3128576766858724
 Std Deviation: 2.3653457806263547
Post-processor Distribution using floor method:
 0: 19.42%
 1: 16.91%
 2: 14.75%
 3: 13.6%
 4: 10.69%
 5: 8.9%
 6: 6.82%
 7: 4.8%
 8: 2.97%
 9: 1.14%

Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 750ns, Mid: 812ns, Max: 5937ns
Raw Samples: 0, 6, 6, 1, 2
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4318
 Std Deviation: 2.867328184406471
Sample Distribution:
 0: 9.93%
 1: 10.73%
 2: 10.46%
 3: 9.92%
 4: 10.2%
 5: 9.82%
 6: 9.68%
 7: 9.71%
 8: 10.13%
 9: 9.42%

Output Distribution: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 187ns
Raw Samples: 0, 3, 0, 0, 7
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4499
 Std Deviation: 2.8986083183173097
Sample Distribution:
 0: 10.69%
 1: 10.1%
 2: 10.18%
 3: 9.69%
 4: 10.13%
 5: 10.19%
 6: 9.74%
 7: 9.29%
 8: 9.39%
 9: 10.6%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Approximate Single Execution Time: Min: 2250ns, Mid: 2250ns, Max: 2656ns
Raw Samples: [5], [4], [1], [4], [1]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9794
 Std Deviation: 2.4567008726985446
Sample Distribution:
 0: 18.75%
 1: 16.23%
 2: 14.5%
 3: 12.7%
 4: 10.93%
 5: 8.61%
 6: 7.43%
 7: 5.4%
 8: 3.59%
 9: 1.86%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Approximate Single Execution Time: Min: 1062ns, Mid: 1125ns, Max: 1968ns
Raw Samples: [1], [2], [8], [1], [5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0291
 Std Deviation: 2.4482345833799353
Sample Distribution:
 0: 17.58%
 1: 16.32%
 2: 14.72%
 3: 12.79%
 4: 11.0%
 5: 9.16%
 6: 7.56%
 7: 5.25%
 8: 3.71%
 9: 1.91%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Approximate Single Execution Time: Min: 1718ns, Mid: 1734ns, Max: 2031ns
Raw Samples: [4], [2], [4], [3], [0]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9693
 Std Deviation: 2.4549460658064572
Sample Distribution:
 0: 18.42%
 1: 17.12%
 2: 14.33%
 3: 12.4%
 4: 10.88%
 5: 8.89%
 6: 7.08%
 7: 5.45%
 8: 3.52%
 9: 1.91%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Approximate Single Execution Time: Min: 687ns, Mid: 750ns, Max: 875ns
Raw Samples: [1], [1], [2], [0], [3]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0223
 Std Deviation: 2.4735429148197827
Sample Distribution:
 0: 18.16%
 1: 16.36%
 2: 14.26%
 3: 12.78%
 4: 10.98%
 5: 9.11%
 6: 6.91%
 7: 5.46%
 8: 3.96%
 9: 2.02%

Output Distribution: cumulative_weighted_choice(((10, 0), (19, 1), (27, 2), (34, 3), (40, 4), (45, 5), (49, 6), (52, 7), (54, 8), (55, 9)), k=1)
Approximate Single Execution Time: Min: 156ns, Mid: 156ns, Max: 500ns
Raw Samples: 3, 2, 2, 2, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9959
 Std Deviation: 2.4491800746992514
Sample Distribution:
 0: 18.38%
 1: 16.05%
 2: 14.59%
 3: 12.85%
 4: 11.1%
 5: 8.93%
 6: 7.34%
 7: 5.33%
 8: 3.46%
 9: 1.97%

Timer only: _random.shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 6718ns, Mid: 6937ns, Max: 8968ns

Timer only: shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 375ns, Mid: 406ns, Max: 468ns

Timer only: knuth(some_list) of size 10:
Approximate Single Execution Time: Min: 843ns, Mid: 875ns, Max: 906ns

Timer only: fisher_yates(some_list) of size 10:
Approximate Single Execution Time: Min: 968ns, Mid: 1000ns, Max: 1062ns

Output Distribution: Random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 3968ns, Mid: 4140ns, Max: 5500ns
Raw Samples: [7, 5, 2], [7, 4, 9], [1, 5, 7], [5, 4, 2], [4, 5, 0]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5113
 Std Deviation: 2.8531187039157455
Sample Distribution:
 0: 10.06%
 1: 9.32%
 2: 9.78%
 3: 10.24%
 4: 10.61%
 5: 10.28%
 6: 10.08%
 7: 9.84%
 8: 9.78%
 9: 10.01%

Output Distribution: sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 750ns, Mid: 781ns, Max: 1062ns
Raw Samples: [1, 2, 3], [4, 8, 0], [9, 5, 1], [0, 6, 1], [0, 9, 1]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4864
 Std Deviation: 2.8547556818404445
Sample Distribution:
 0: 9.67%
 1: 10.01%
 2: 10.32%
 3: 10.2%
 4: 10.34%
 5: 10.01%
 6: 9.7%
 7: 9.71%
 8: 10.55%
 9: 9.49%


Total Test Time: 1.581 sec

```
