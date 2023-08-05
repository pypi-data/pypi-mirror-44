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

_It is possible that an asymmetric AC would be a better match to how negative numbers work as reverse list indexes in python. Asymmetric Analytic Continuation:_ `lambda f, n: f(n) if n > 0 else -f(-n)-1 if n < 0 else None` (this is how it could work). _This would allow_ `some_list[randbelow(-n)]` _to range over the last n items in a list of size n or larger. The interesting part is that you wouldn't need to know the exact size of the list. Let me know if you think this is a good idea._

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
    - Always inclusive on the side closer to zero and exclusive on the other side. Because zero is always the most natural place to start no matter what direction you're going. This matches the symmetry of the analytic continuation of Pyewacket.randbelow(). Also, the unit vector, no matter what direction it's pointing, always includes and points away from zero.
    - Ignores sign of step, but it could be a trigger for reversing the inclusivity rule.

```python
from Pyewacket import randrange


""" Standard """
randrange(10)           # -> [0, 10) by whole numbers
randrange(1, 10)        # -> [1, 10) by whole numbers
randrange(1, 10, 2)     # -> [1, 10) by 2, odd numbers

""" Extras """
randrange(0)            # -> [0, 0) -> 0
randrange(-10)          # -> (-10, 0] by 1
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
    - Only seeing a 2x performance gain for this algorithm so far.
    - See Weighted Choice in Fortuna for another approach. https://pypi.org/project/Fortuna/
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
Approximate Single Execution Time: Min: 531ns, Mid: 593ns, Max: 1750ns
Raw Samples: 1, 3, 8, 3, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5359
 Std Deviation: 2.8864414673494494
Sample Distribution:
 0: 9.82%
 1: 10.15%
 2: 9.92%
 3: 9.87%
 4: 9.68%
 5: 9.7%
 6: 10.15%
 7: 10.2%
 8: 10.12%
 9: 10.39%

Output Distribution: randbelow(10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 687ns
Raw Samples: 5, 7, 7, 8, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5108
 Std Deviation: 2.8694087737147296
Sample Distribution:
 0: 9.86%
 1: 9.79%
 2: 10.41%
 3: 9.69%
 4: 10.29%
 5: 9.75%
 6: 10.01%
 7: 10.35%
 8: 9.67%
 9: 10.18%

Output Distribution: Random.randint(1, 10)
Approximate Single Execution Time: Min: 1156ns, Mid: 1234ns, Max: 2593ns
Raw Samples: 4, 2, 1, 10, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4609
 Std Deviation: 2.8704869202830294
Sample Distribution:
 1: 10.19%
 2: 10.12%
 3: 9.97%
 4: 10.34%
 5: 10.18%
 6: 9.65%
 7: 10.41%
 8: 9.56%
 9: 9.56%
 10: 10.02%

Output Distribution: randint(1, 10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 125ns
Raw Samples: 5, 5, 1, 3, 10
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.5325
 Std Deviation: 2.8860659534509545
Sample Distribution:
 1: 9.71%
 2: 10.59%
 3: 9.56%
 4: 9.65%
 5: 9.97%
 6: 10.02%
 7: 9.68%
 8: 10.53%
 9: 9.79%
 10: 10.5%

Output Distribution: Random.randrange(0, 10, 2)
Approximate Single Execution Time: Min: 1312ns, Mid: 1343ns, Max: 1593ns
Raw Samples: 0, 4, 8, 8, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.0432
 Std Deviation: 2.8324787825516644
Sample Distribution:
 0: 19.75%
 2: 19.52%
 4: 20.0%
 6: 20.28%
 8: 20.45%

Output Distribution: randrange(0, 10, 2)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 6, 2, 8, 6, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 3.9746
 Std Deviation: 2.8369983602338573
Sample Distribution:
 0: 20.63%
 2: 19.48%
 4: 20.29%
 6: 19.73%
 8: 19.87%

Output Distribution: Random.random()
Approximate Single Execution Time: Min: 31ns, Mid: 31ns, Max: 656ns
Raw Samples: 0.38535879309212584, 0.006935578722434554, 0.13303051927943, 0.9727472579946359, 0.5595839778730648
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.7307494785789856e-05
 Median: (0.49672499788770297, 0.49679922194917747)
 Maximum: 0.999915721071989
 Mean: 0.4973428828478637
 Std Deviation: 0.288807243967117
Post-processor Distribution using round method:
 0: 50.29%
 1: 49.71%

Output Distribution: random()
Approximate Single Execution Time: Min: 31ns, Mid: 46ns, Max: 187ns
Raw Samples: 0.2015796358015446, 0.8005405326891581, 0.9982815770816583, 0.05652070644604089, 0.338611003783271
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 4.198119076056291e-05
 Median: (0.49302999750361065, 0.49303961089110937)
 Maximum: 0.9999530190424643
 Mean: 0.4974028586003276
 Std Deviation: 0.2886464483302728
Post-processor Distribution using round method:
 0: 50.7%
 1: 49.3%

Output Distribution: Random.uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 218ns, Mid: 250ns, Max: 718ns
Raw Samples: 8.43432218155047, 9.190925348751342, 1.3577683286463649, 0.3406854862850417, 3.5997280373533993
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0010356579432602153
 Median: (5.038027055258352, 5.038967125142859)
 Maximum: 9.99980330015924
 Mean: 5.010171439727637
 Std Deviation: 2.881100858221537
Post-processor Distribution using floor method:
 0: 9.73%
 1: 10.48%
 2: 9.93%
 3: 9.33%
 4: 10.2%
 5: 10.36%
 6: 9.83%
 7: 10.11%
 8: 9.95%
 9: 10.08%

Output Distribution: uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 8.138723133403635, 7.010476485606748, 4.903732129784347, 4.4853921702948325, 9.806528534509297
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0007064599619784469
 Median: (5.017968029936096, 5.020557714037127)
 Maximum: 9.999451921099581
 Mean: 5.019433938586432
 Std Deviation: 2.878674440138677
Post-processor Distribution using floor method:
 0: 10.06%
 1: 9.59%
 2: 9.69%
 3: 9.99%
 4: 10.43%
 5: 10.12%
 6: 10.44%
 7: 9.32%
 8: 10.42%
 9: 9.94%

Output Distribution: Random.expovariate(1.0)
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 593ns
Raw Samples: 0.0508095093184102, 0.2551205138079458, 1.3785197686026371, 0.24989003359958575, 0.6062643964421751
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 5.0771677497127625e-05
 Median: (0.6956755444159768, 0.6958003597270009)
 Maximum: 10.330551793179374
 Mean: 1.0096042241148002
 Std Deviation: 1.041569176829521
Post-processor Distribution using floor method:
 0: 63.82%
 1: 22.4%
 2: 8.4%
 3: 3.17%
 4: 1.45%
 5: 0.36%
 6: 0.25%
 7: 0.08%
 8: 0.04%
 9: 0.02%
 10: 0.01%

Output Distribution: expovariate(1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 500ns
Raw Samples: 1.6357005217158198, 0.18965704130178523, 0.7291531175337636, 3.2020669379259097, 0.5764036397659476
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 4.339239319219056e-05
 Median: (0.6944032784431176, 0.6944612336469684)
 Maximum: 9.714034513829269
 Mean: 0.9953690488567053
 Std Deviation: 0.988541384309089
Post-processor Distribution using floor method:
 0: 63.28%
 1: 23.68%
 2: 8.06%
 3: 3.17%
 4: 1.19%
 5: 0.43%
 6: 0.08%
 7: 0.06%
 8: 0.03%
 9: 0.02%

Output Distribution: Random.gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 1156ns, Mid: 1281ns, Max: 1562ns
Raw Samples: 0.29422946491310603, 3.456976118806364, 0.4450518021827561, 0.7961833553748179, 4.64956337360505
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0066337889358191425
 Median: (1.6743843035053858, 1.6747491222427642)
 Maximum: 10.559790618998553
 Mean: 1.9971755436604701
 Std Deviation: 1.3995175910687918
Post-processor Distribution using round method:
 0: 9.16%
 1: 34.94%
 2: 27.49%
 3: 15.01%
 4: 7.05%
 5: 3.67%
 6: 1.65%
 7: 0.7%
 8: 0.21%
 9: 0.05%
 10: 0.06%
 11: 0.01%

Output Distribution: gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 281ns
Raw Samples: 1.601944937316535, 1.371954253350558, 3.3299088241306887, 1.9976885255723273, 0.535761702834404
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.008694286377845861
 Median: (1.6846976860443972, 1.6848539436069792)
 Maximum: 9.99168396567059
 Mean: 1.9893135992696815
 Std Deviation: 1.3919667611551416
Post-processor Distribution using round method:
 0: 8.8%
 1: 35.75%
 2: 26.64%
 3: 15.69%
 4: 7.28%
 5: 3.3%
 6: 1.51%
 7: 0.62%
 8: 0.25%
 9: 0.11%
 10: 0.05%

Output Distribution: Random.weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 406ns, Mid: 437ns, Max: 593ns
Raw Samples: 0.050311227250074496, 0.5736444924051997, 0.20686139000183792, 0.14093166993959738, 0.6948123258823661
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0001353987741106479
 Median: (0.7009811866470828, 0.7010494158226442)
 Maximum: 9.203646416618204
 Mean: 1.0071831148528956
 Std Deviation: 1.004694160075791
Post-processor Distribution using floor method:
 0: 62.69%
 1: 23.89%
 2: 8.37%
 3: 2.92%
 4: 1.5%
 5: 0.37%
 6: 0.18%
 7: 0.05%
 8: 0.02%
 9: 0.01%

Output Distribution: weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 875ns
Raw Samples: 0.25207574330561144, 0.1624692124611726, 2.5704535895840297, 1.774208561430924, 0.48229714223345865
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 2.9614039377826745e-05
 Median: (0.6793331260005409, 0.6793411481300994)
 Maximum: 9.533544477967295
 Mean: 0.9857763791627122
 Std Deviation: 0.9948322343171733
Post-processor Distribution using floor method:
 0: 64.04%
 1: 22.63%
 2: 8.43%
 3: 3.02%
 4: 1.25%
 5: 0.4%
 6: 0.15%
 7: 0.05%
 8: 0.02%
 9: 0.01%

Output Distribution: Random.betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 2437ns, Mid: 2593ns, Max: 4343ns
Raw Samples: 0.5873598795506763, 0.11345659910117567, 0.5034826803294432, 0.24813809232572526, 0.30087292717186015
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0061907106146835075
 Median: (0.5011994881260904, 0.50127658529137)
 Maximum: 0.9822821427603219
 Mean: 0.5006690859702995
 Std Deviation: 0.18933868921806124
Post-processor Distribution using round method:
 0: 49.77%
 1: 50.23%

Output Distribution: betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 812ns
Raw Samples: 0.4993181097383636, 0.2847903075974447, 0.7694149579133103, 0.21966311086592372, 0.42787774463133676
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.026069137405512647
 Median: (0.5007328269369267, 0.5007933954973143)
 Maximum: 0.989925445563623
 Mean: 0.4992746176447618
 Std Deviation: 0.18795714004311845
Post-processor Distribution using round method:
 0: 49.85%
 1: 50.15%

Output Distribution: Random.paretovariate(4.0)
Approximate Single Execution Time: Min: 281ns, Mid: 281ns, Max: 1437ns
Raw Samples: 1.3565885489795817, 1.5863169596425406, 1.361360192519912, 1.0444968219547663, 1.0287613488735559
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000087296401348
 Median: (1.1901218887081368, 1.1901337254165771)
 Maximum: 10.712503357635628
 Mean: 1.3374576042692483
 Std Deviation: 0.46668095467504045
Post-processor Distribution using floor method:
 1: 93.3%
 2: 5.45%
 3: 0.94%
 4: 0.15%
 5: 0.08%
 6: 0.02%
 7: 0.02%
 8: 0.03%
 10: 0.01%

Output Distribution: paretovariate(4.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 531ns
Raw Samples: 1.0622880100884795, 1.155982365346509, 1.47150124154689, 1.1222747847086134, 1.2078524988001302
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000297669416947
 Median: (1.1857041801644952, 1.1859058970894027)
 Maximum: 13.548753154695643
 Mean: 1.3329991801301504
 Std Deviation: 0.49208947185413854
Post-processor Distribution using floor method:
 1: 94.01%
 2: 4.66%
 3: 0.89%
 4: 0.26%
 5: 0.1%
 6: 0.03%
 7: 0.01%
 8: 0.01%
 11: 0.01%
 13: 0.02%

Output Distribution: Random.gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 593ns, Mid: 593ns, Max: 937ns
Raw Samples: 1.156942896046115, 0.317262153975307, 0.3296581876160305, 0.3256290696328802, -0.4899831168165434
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.705084915881008
 Median: (0.9922595243363026, 0.9926453423722021)
 Maximum: 5.237615883242283
 Mean: 0.9984664091121337
 Std Deviation: 0.9985598834964594
Post-processor Distribution using round method:
 -3: 0.01%
 -2: 0.56%
 -1: 5.88%
 0: 24.73%
 1: 38.31%
 2: 23.65%
 3: 6.28%
 4: 0.54%
 5: 0.04%

Output Distribution: gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 281ns
Raw Samples: 1.6330885028782303, 1.1344843786697567, 0.563138558885672, 1.0950514215902076, 0.47520306355880176
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.8516819879869835
 Median: (1.018321459057206, 1.0190412721739233)
 Maximum: 4.950499975369
 Mean: 1.0170007592642492
 Std Deviation: 0.9992548514607695
Post-processor Distribution using round method:
 -3: 0.01%
 -2: 0.6%
 -1: 5.54%
 0: 24.5%
 1: 38.03%
 2: 24.27%
 3: 6.45%
 4: 0.54%
 5: 0.06%

Output Distribution: Random.normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 656ns, Mid: 765ns, Max: 1937ns
Raw Samples: 2.2153543781466634, 3.0061836867269647, -3.572661829253527, 3.023787838575158, 0.3503685478212736
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -9.5955569939035
 Median: (0.03017543876751487, 0.030235038784155305)
 Maximum: 10.324233975516766
 Mean: 0.012226354286686652
 Std Deviation: 2.825649319580328
Post-processor Distribution using round method:
 -10: 0.01%
 -9: 0.12%
 -8: 0.3%
 -7: 0.69%
 -6: 1.55%
 -5: 2.89%
 -4: 5.23%
 -3: 7.78%
 -2: 10.81%
 -1: 13.26%
 0: 14.01%
 1: 13.5%
 2: 11.03%
 3: 7.81%
 4: 5.49%
 5: 2.94%
 6: 1.61%
 7: 0.63%
 8: 0.26%
 9: 0.05%
 10: 0.03%

Output Distribution: normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 187ns
Raw Samples: -4.536679964022295, -1.3461313761003149, -2.1769748177039787, 4.181003566960071, -1.2995681451747105
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -11.936606686508375
 Median: (0.03413362420801508, 0.034258167210337996)
 Maximum: 11.41086349008248
 Mean: 0.0009632836307509721
 Std Deviation: 2.8043668744661936
Post-processor Distribution using round method:
 -12: 0.01%
 -11: 0.02%
 -10: 0.02%
 -9: 0.08%
 -8: 0.24%
 -7: 0.62%
 -6: 1.49%
 -5: 2.8%
 -4: 5.26%
 -3: 8.41%
 -2: 10.85%
 -1: 13.16%
 0: 13.73%
 1: 13.47%
 2: 11.31%
 3: 7.89%
 4: 5.22%
 5: 2.99%
 6: 1.4%
 7: 0.63%
 8: 0.27%
 9: 0.11%
 11: 0.02%

Output Distribution: Random.lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 812ns, Mid: 875ns, Max: 2187ns
Raw Samples: 1.0504596451348278, 1.0402095659763089, 1.606615409995859, 0.5167641977552256, 0.4959321773476437
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.15366639117748726
 Median: (1.0019633353579314, 1.0020108941548809)
 Maximum: 7.201693610232157
 Mean: 1.1345095739280786
 Std Deviation: 0.6083278804290074
Post-processor Distribution using round method:
 0: 8.72%
 1: 70.52%
 2: 17.1%
 3: 3.03%
 4: 0.52%
 5: 0.09%
 6: 0.01%
 7: 0.01%

Output Distribution: lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 750ns
Raw Samples: 0.5957891509878049, 0.502547890176609, 0.854323681301625, 1.2816056188070206, 0.5508686657097338
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.16278023719758228
 Median: (1.007152802240199, 1.0072186272565062)
 Maximum: 7.580008078024966
 Mean: 1.1389999986676242
 Std Deviation: 0.6104564216753835
Post-processor Distribution using round method:
 0: 8.36%
 1: 70.77%
 2: 17.28%
 3: 2.92%
 4: 0.49%
 5: 0.15%
 6: 0.02%
 8: 0.01%

Output Distribution: Random.vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 437ns
Raw Samples: 4.593000718036387, 2.969921331756848, 2.4584819529671647, 0.7009223568919257, 5.062089287567497
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0008101722036527526
 Median: (3.105576471624022, 3.1063052900384776)
 Maximum: 6.283155758062235
 Mean: 3.135818026807751
 Std Deviation: 1.801987839388294
Post-processor Distribution using floor method:
 0: 15.67%
 1: 15.8%
 2: 16.72%
 3: 15.69%
 4: 16.05%
 5: 15.55%
 6: 4.52%

Output Distribution: vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 531ns
Raw Samples: 5.284487049917341, 1.6989668774662579, 1.8027276384466353, 0.17095092214255742, 1.86716914220569
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0031847246382218047
 Median: (3.126897322695558, 3.1271494534276365)
 Maximum: 6.281750073528779
 Mean: 3.12744121460462
 Std Deviation: 1.8196363647238358
Post-processor Distribution using floor method:
 0: 16.32%
 1: 15.96%
 2: 15.75%
 3: 15.36%
 4: 16.21%
 5: 15.86%
 6: 4.54%

Output Distribution: Random.triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 468ns, Mid: 500ns, Max: 1093ns
Raw Samples: 5.793292838528565, 5.751076753495103, 0.02119567817323542, 1.6237199943293579, 2.4262438714413594
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00035948694066867404
 Median: (2.944766673129937, 2.9454837820465416)
 Maximum: 9.969559978632168
 Mean: 3.338645086503229
 Std Deviation: 2.3652675634473113
Post-processor Distribution using floor method:
 0: 18.95%
 1: 16.98%
 2: 14.89%
 3: 13.49%
 4: 11.06%
 5: 8.54%
 6: 6.89%
 7: 4.97%
 8: 3.1%
 9: 1.13%

Output Distribution: triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 656ns
Raw Samples: 0.4466694949752781, 5.573379323683203, 0.7777659747050836, 0.06660210871049288, 1.6502516939547807
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 8.439844915497652e-05
 Median: (2.917655949662673, 2.9191836275954888)
 Maximum: 9.921553072086445
 Mean: 3.3092779793363776
 Std Deviation: 2.339018361248642
Post-processor Distribution using floor method:
 0: 19.3%
 1: 16.7%
 2: 15.04%
 3: 13.38%
 4: 11.36%
 5: 8.46%
 6: 7.07%
 7: 4.89%
 8: 2.84%
 9: 0.96%

Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 750ns, Mid: 812ns, Max: 1125ns
Raw Samples: 6, 9, 3, 6, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5232
 Std Deviation: 2.8657779098009026
Sample Distribution:
 0: 9.74%
 1: 10.2%
 2: 9.86%
 3: 9.85%
 4: 9.53%
 5: 10.34%
 6: 10.21%
 7: 9.82%
 8: 11.02%
 9: 9.43%

Output Distribution: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 125ns
Raw Samples: 2, 9, 7, 3, 3
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.4896
 Std Deviation: 2.8630947541353073
Sample Distribution:
 0: 10.12%
 1: 9.79%
 2: 10.09%
 3: 10.12%
 4: 9.81%
 5: 10.19%
 6: 9.89%
 7: 10.45%
 8: 9.91%
 9: 9.63%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 3062ns, Mid: 3125ns, Max: 6187ns
Raw Samples: [0, 8, 9], [0, 7, 2], [0, 1, 3], [4, 4, 3], [1, 0, 8]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0053
 Std Deviation: 2.4564354902035905
Sample Distribution:
 0: 17.81%
 1: 16.92%
 2: 14.35%
 3: 13.04%
 4: 10.63%
 5: 8.97%
 6: 7.05%
 7: 5.62%
 8: 3.71%
 9: 1.9%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 1875ns, Mid: 1937ns, Max: 4218ns
Raw Samples: [5, 6, 0], [0, 6, 9], [2, 9, 4], [0, 2, 8], [0, 1, 4]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0434
 Std Deviation: 2.4591301657531695
Sample Distribution:
 0: 18.04%
 1: 15.68%
 2: 14.08%
 3: 13.34%
 4: 11.27%
 5: 9.12%
 6: 7.09%
 7: 5.61%
 8: 3.94%
 9: 1.83%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 2500ns, Mid: 2531ns, Max: 4937ns
Raw Samples: [5, 4, 8], [5, 3, 7], [1, 3, 1], [2, 3, 2], [2, 8, 7]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0033
 Std Deviation: 2.4570089131462116
Sample Distribution:
 0: 17.88%
 1: 16.81%
 2: 14.51%
 3: 12.95%
 4: 10.73%
 5: 8.76%
 6: 7.06%
 7: 5.64%
 8: 3.85%
 9: 1.81%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 1468ns, Mid: 1515ns, Max: 2812ns
Raw Samples: [0, 3, 6], [1, 6, 5], [2, 3, 1], [1, 0, 4], [0, 1, 0]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9972
 Std Deviation: 2.4570705890527362
Sample Distribution:
 0: 18.49%
 1: 16.34%
 2: 14.34%
 3: 12.59%
 4: 10.73%
 5: 9.16%
 6: 7.51%
 7: 5.43%
 8: 3.55%
 9: 1.86%

Timer only: _random.shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 6781ns, Mid: 6937ns, Max: 9875ns

Timer only: shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 343ns, Mid: 375ns, Max: 781ns

Timer only: knuth(some_list) of size 10:
Approximate Single Execution Time: Min: 843ns, Mid: 875ns, Max: 1343ns

Timer only: fisher_yates(some_list) of size 10:
Approximate Single Execution Time: Min: 937ns, Mid: 968ns, Max: 1875ns

Output Distribution: Random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 4000ns, Mid: 4125ns, Max: 7156ns
Raw Samples: [3, 0, 4], [1, 4, 6], [3, 9, 6], [2, 6, 3], [9, 0, 5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.4998
 Std Deviation: 2.8981097053055804
Sample Distribution:
 0: 10.34%
 1: 10.16%
 2: 9.93%
 3: 9.65%
 4: 9.75%
 5: 10.23%
 6: 9.56%
 7: 9.93%
 8: 10.06%
 9: 10.39%

Output Distribution: sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 812ns, Mid: 843ns, Max: 2312ns
Raw Samples: [1, 8, 0], [0, 5, 2], [3, 9, 5], [7, 9, 2], [7, 6, 5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5263
 Std Deviation: 2.8852973510680675
Sample Distribution:
 0: 9.82%
 1: 9.87%
 2: 10.69%
 3: 9.68%
 4: 9.25%
 5: 10.03%
 6: 10.39%
 7: 9.8%
 8: 9.98%
 9: 10.49%


Total Test Time: 1.561 sec

```
