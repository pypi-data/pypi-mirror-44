# Pyewacket
### Fast, fault-tolerant, drop-in replacement for the Python3 random module

Built atop the RNG Storm Engine for proven stability and performance. While Storm is a high quality random engine, Pyewacket is not appropriate for cryptography of any kind. Pyewacket is meant for games, data science, A.I. and experimental programming, not security.


**Recommended Installation:** `$ pip install Pyewacket`


### Pyewacket serves three main goals:
1. Provide a feature rich and familiar API for generating random numbers and values.
    - Faithful to the random module API, but not a slave to it.
2. Go fast!
    - The RNG Storm Engine is an order of magnitude faster on average.
3. Fix things. Random.random is NOT broken, however it is not fault tolerant either.
    - Exceptions that can be avoided with balance, symmetry and sound mathematics, will be avoided. New behavior will be implemented as needed, but new math will not be invented.
    - Do or do not, there is no try/except. Alright, sometimes `try:` is useful, but it's only needed in truly exceptional cases where lambda calculus fails.
    - All class methods will be implemented as free functions when possible.


## Random Integers
- `Pyewacket.randbelow(n: int) -> int`
    - Back by popular demand. While randrange(a, b, c) is handy when you need it, it's more complex than needed most of the time. Mathematically, randbelow(n) is equivalent to randrange(n).
    - Pyewacket.randbelow is 10x - 12x faster than `Random._randbelow()`.
    - @param n :: expanded acceptable input domain to include non-positive values of n.
    - @return :: random integer in range (n, 0] or [0, n)
    - Analytic Continuation about zero to achieve full input domain coverage for a function that normally only takes positive, non-zero values as input. I think this lambda is beautiful in every sense of the word. Let it wash over you like poetry.
    - `lambda f, n: f(n) if n > 0 else -f(-n) if n < 0 else 0`
    - This lambda is not part of the actual implementation, but it represents the idea of AC pretty well. AC will invert the meaning of a function for negative input. Thus turning randbelow into randabove for all negative input n.

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
    - Implements Knuth 2 Shuffle Algorithm. Knuth 2 is twice as fast as Knuth 1 or Fisher-Yates for every test case. This is likely due to the combination of walking backward and rotating backward into the back side of the list. With this combination it can never modify the data it still needs to walk through. Fresh snow all the way home, aka very low probability for cache misses.
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


## Testing Suite
- `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - For the statistical analysis of a non-deterministic numeric output function.
    - @param func :: function, method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles=10000 :: Total number of samples to use for analysis.
    - @optional_kw post_processor=None :: Used to scale a large set of data into a smaller set of groupings for better visualization of the data, esp. useful for distributions of floats. For many functions in quick_test(), math.floor() is used, for others round() is more appropriate. For more complex post processing - lambdas work nicely. Post processing only affects the distribution, the statistics and performance results are unaffected.
- `quick_test()`
    - Runs a battery of tests for every random distribution function in the module.


## Development Log
- ToDo:
    - seed()
    - getrandbits()

##### Pyewacket v0.0.1b8
- Fixed a small bug in the tests.

##### Pyewacket v0.0.1b7
- Engine Fine Tuning
- Fixed some typos.

##### Pyewacket v0.0.1b6
- Rearranged tests to be more consistant and match the documentation.

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


Output Distribution: Random._randbelow(10)
Approximate Single Execution Time: Min: 531ns, Mid: 593ns, Max: 1656ns
Raw Samples: 0, 7, 8, 0, 6
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4852
 Std Deviation: 2.8896394172277207
Sample Distribution:
 0: 10.3%
 1: 9.89%
 2: 10.48%
 3: 9.56%
 4: 10.14%
 5: 9.84%
 6: 9.88%
 7: 9.61%
 8: 10.02%
 9: 10.28%

Output Distribution: randbelow(10)
Approximate Single Execution Time: Min: 31ns, Mid: 77ns, Max: 500ns
Raw Samples: 2, 8, 2, 1, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5042
 Std Deviation: 2.8765273857518023
Sample Distribution:
 0: 9.81%
 1: 10.14%
 2: 9.96%
 3: 10.45%
 4: 9.66%
 5: 10.06%
 6: 9.96%
 7: 9.67%
 8: 9.99%
 9: 10.3%

Output Distribution: Random.randint(1, 10)
Approximate Single Execution Time: Min: 1156ns, Mid: 1218ns, Max: 2687ns
Raw Samples: 1, 1, 7, 3, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.5307
 Std Deviation: 2.8689511320445673
Sample Distribution:
 1: 9.65%
 2: 10.01%
 3: 9.83%
 4: 10.03%
 5: 10.09%
 6: 10.26%
 7: 9.97%
 8: 9.84%
 9: 9.93%
 10: 10.39%

Output Distribution: randint(1, 10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 656ns
Raw Samples: 3, 5, 7, 9, 6
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4684
 Std Deviation: 2.8646504258296894
Sample Distribution:
 1: 10.13%
 2: 9.95%
 3: 10.38%
 4: 9.8%
 5: 10.14%
 6: 10.04%
 7: 10.29%
 8: 9.69%
 9: 9.82%
 10: 9.76%

Output Distribution: Random.randrange(0, 10, 2)
Approximate Single Execution Time: Min: 1281ns, Mid: 1312ns, Max: 3062ns
Raw Samples: 4, 0, 8, 0, 4
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.0624
 Std Deviation: 2.8273142044281276
Sample Distribution:
 0: 19.37%
 2: 19.75%
 4: 19.81%
 6: 20.53%
 8: 20.54%

Output Distribution: randrange(0, 10, 2)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 125ns
Raw Samples: 2, 4, 0, 8, 2
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 3.9914
 Std Deviation: 2.8192766575998194
Sample Distribution:
 0: 19.93%
 2: 19.89%
 4: 20.74%
 6: 19.56%
 8: 19.88%

Output Distribution: Random.random()
Approximate Single Execution Time: Min: 31ns, Mid: 31ns, Max: 62ns
Raw Samples: 0.6593360186815826, 0.285235027879155, 0.8671592767940003, 0.11568019401052199, 0.44928001762929637
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00014059717762493484
 Median: (0.5025481401789799, 0.5025985887623043)
 Maximum: 0.9999975700037487
 Mean: 0.5007751279947313
 Std Deviation: 0.2898488928116845
Post-processor Distribution using round method:
 0: 49.74%
 1: 50.26%

Output Distribution: random()
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 906ns
Raw Samples: 0.06520791010807962, 0.15313320206078948, 0.8966446732477615, 0.7878288369964539, 0.526894559310951
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 7.976996689652925e-05
 Median: (0.49937655056575125, 0.49939098642449303)
 Maximum: 0.9999632728271979
 Mean: 0.5007639852878765
 Std Deviation: 0.2902323315007569
Post-processor Distribution using round method:
 0: 50.06%
 1: 49.94%

Output Distribution: Random.uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 218ns, Mid: 250ns, Max: 406ns
Raw Samples: 1.1287521196859496, 7.3567499277801796, 9.445861059074565, 9.817498100026192, 9.349118871271596
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0005144513233790171
 Median: (5.008769778290646, 5.008947149318982)
 Maximum: 9.998425563047965
 Mean: 4.992367147626723
 Std Deviation: 2.885304169552057
Post-processor Distribution using floor method:
 0: 10.47%
 1: 9.45%
 2: 9.85%
 3: 10.14%
 4: 9.98%
 5: 10.2%
 6: 10.3%
 7: 9.7%
 8: 9.98%
 9: 9.93%

Output Distribution: uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 156ns
Raw Samples: 6.424057121390754, 0.9282551966602655, 4.852927766225886, 0.5950502996996582, 9.239423229242421
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.003644954700034532
 Median: (4.9713945309537735, 4.973287047123843)
 Maximum: 9.999180622140726
 Mean: 4.988970128602078
 Std Deviation: 2.892473502454241
Post-processor Distribution using floor method:
 0: 10.21%
 1: 9.96%
 2: 9.77%
 3: 10.05%
 4: 10.3%
 5: 10.02%
 6: 9.68%
 7: 10.03%
 8: 10.02%
 9: 9.96%

Output Distribution: Random.expovariate(1.0)
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 968ns
Raw Samples: 0.8976882044528854, 1.458543769314171, 1.452144938876796, 0.45737034789010367, 0.3231905030298167
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 9.531692113499263e-05
 Median: (0.7104041736008866, 0.7109162721308501)
 Maximum: 9.032148751888395
 Mean: 1.0023346295851647
 Std Deviation: 0.9945129108708807
Post-processor Distribution using floor method:
 0: 62.71%
 1: 24.12%
 2: 8.15%
 3: 3.23%
 4: 1.11%
 5: 0.41%
 6: 0.16%
 7: 0.08%
 8: 0.02%
 9: 0.01%

Output Distribution: expovariate(1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 156ns
Raw Samples: 0.3683935389032551, 1.2815758233658576, 0.37217456763695783, 0.5854221500444202, 2.9206569026931772
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 4.5141768050555684e-05
 Median: (0.6711052942018784, 0.6712459303656784)
 Maximum: 10.150550699370331
 Mean: 0.9709875646507249
 Std Deviation: 0.9620344212076951
Post-processor Distribution using floor method:
 0: 64.4%
 1: 22.91%
 2: 8.28%
 3: 2.86%
 4: 1.09%
 5: 0.29%
 6: 0.09%
 7: 0.03%
 8: 0.03%
 9: 0.01%
 10: 0.01%

Output Distribution: Random.gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 1125ns, Mid: 1281ns, Max: 1500ns
Raw Samples: 0.7310465370456404, 0.28385297761807066, 0.981951905763987, 1.2460901691294175, 0.5400896964843788
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.012031468392824608
 Median: (1.68774820529325, 1.687994021020246)
 Maximum: 11.008771084099308
 Mean: 2.0073207729699942
 Std Deviation: 1.4108017303460547
Post-processor Distribution using round method:
 0: 8.61%
 1: 35.18%
 2: 27.07%
 3: 15.45%
 4: 7.67%
 5: 3.31%
 6: 1.46%
 7: 0.69%
 8: 0.41%
 9: 0.1%
 10: 0.03%
 11: 0.02%

Output Distribution: gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 218ns
Raw Samples: 2.5355735309495953, 3.1839098655173963, 1.0924080927996074, 1.208512416112714, 1.5714300772630354
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.03312241055812559
 Median: (1.6661896887445324, 1.6667280266310465)
 Maximum: 11.06602996031152
 Mean: 2.0026588419904456
 Std Deviation: 1.4082916816900415
Post-processor Distribution using round method:
 0: 8.79%
 1: 35.46%
 2: 27.15%
 3: 14.88%
 4: 7.56%
 5: 3.54%
 6: 1.56%
 7: 0.65%
 8: 0.22%
 9: 0.11%
 10: 0.05%
 11: 0.03%

Output Distribution: Random.weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 406ns, Mid: 437ns, Max: 812ns
Raw Samples: 0.04781154564732262, 1.06834586796707, 0.48303498668587275, 0.27509589646604893, 0.6878355480177504
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 4.136058881743425e-05
 Median: (0.6830914395378591, 0.6833376790883753)
 Maximum: 7.888163979042827
 Mean: 0.9836026886515956
 Std Deviation: 0.9661050670017435
Post-processor Distribution using floor method:
 0: 63.75%
 1: 23.33%
 2: 8.31%
 3: 2.93%
 4: 1.07%
 5: 0.47%
 6: 0.11%
 7: 0.03%

Output Distribution: weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 218ns
Raw Samples: 1.1306300609067412, 3.9209853064275006, 0.7357610799328026, 0.5047615365090363, 0.12992625533137261
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00011262277077129895
 Median: (0.7131271682351112, 0.713468182909572)
 Maximum: 9.33169202328762
 Mean: 1.0074770511252362
 Std Deviation: 0.9897757215391743
Post-processor Distribution using floor method:
 0: 62.31%
 1: 24.19%
 2: 8.59%
 3: 3.19%
 4: 1.11%
 5: 0.38%
 6: 0.13%
 7: 0.08%
 8: 0.01%
 9: 0.01%

Output Distribution: Random.betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 2531ns, Mid: 2702ns, Max: 3781ns
Raw Samples: 0.5369674184257875, 0.5215116171220677, 0.8672118444368013, 0.5369177914124822, 0.24537471352330187
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.021708257177248676
 Median: (0.4998613209454744, 0.4998681466096839)
 Maximum: 0.9894252932518328
 Mean: 0.4996082667636314
 Std Deviation: 0.18873738280161942
Post-processor Distribution using round method:
 0: 50.05%
 1: 49.95%

Output Distribution: betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 250ns
Raw Samples: 0.13275389957781805, 0.6253349593560116, 0.46808326068511347, 0.6305926393769528, 0.5802100294850571
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.023962024259662595
 Median: (0.49886860794269766, 0.49898135761560847)
 Maximum: 0.9598858876884495
 Mean: 0.49967802216006557
 Std Deviation: 0.19009801999290402
Post-processor Distribution using round method:
 0: 50.2%
 1: 49.8%

Output Distribution: Random.paretovariate(4.0)
Approximate Single Execution Time: Min: 281ns, Mid: 312ns, Max: 687ns
Raw Samples: 2.021237708437411, 1.1494037128273398, 1.1100030013967608, 1.0623577819339312, 1.001980271957715
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000195687040845
 Median: (1.1856779319885589, 1.1857294353338905)
 Maximum: 9.802694717614573
 Mean: 1.3353247849408063
 Std Deviation: 0.46310495988703826
Post-processor Distribution using floor method:
 1: 93.26%
 2: 5.51%
 3: 0.86%
 4: 0.23%
 5: 0.04%
 6: 0.07%
 7: 0.01%
 8: 0.01%
 9: 0.01%

Output Distribution: paretovariate(4.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 218ns
Raw Samples: 1.6922667079309122, 1.277389198228928, 1.0300503200644455, 2.4118091443281124, 1.0135408180881216
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000392715264679
 Median: (1.1891373206315052, 1.1891790100090236)
 Maximum: 13.502675530685359
 Mean: 1.3290883257416697
 Std Deviation: 0.4628625192093174
Post-processor Distribution using floor method:
 1: 93.75%
 2: 4.99%
 3: 0.86%
 4: 0.25%
 5: 0.09%
 6: 0.03%
 8: 0.01%
 9: 0.01%
 13: 0.01%

Output Distribution: Random.gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 562ns, Mid: 593ns, Max: 1687ns
Raw Samples: 0.014251953113130655, 2.2916359187268345, 1.97388200594882, 0.4951707253099209, 0.06240472589576451
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.879107898701512
 Median: (1.022713390834662, 1.022870354946728)
 Maximum: 5.145933786838998
 Mean: 1.0146496831926684
 Std Deviation: 0.9921795504213352
Post-processor Distribution using round method:
 -3: 0.02%
 -2: 0.6%
 -1: 5.96%
 0: 23.54%
 1: 38.12%
 2: 25.3%
 3: 5.81%
 4: 0.61%
 5: 0.04%

Output Distribution: gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 187ns
Raw Samples: 1.0102374382064956, 0.6531741123125455, -0.01949691473801433, 0.5033171469264376, 1.2215753867436405
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.7464108790251545
 Median: (1.0112858688991146, 1.0120374533308023)
 Maximum: 5.10604252317355
 Mean: 1.011595099795983
 Std Deviation: 1.0007143879377516
Post-processor Distribution using round method:
 -3: 0.02%
 -2: 0.57%
 -1: 6.11%
 0: 23.51%
 1: 38.7%
 2: 24.2%
 3: 6.31%
 4: 0.55%
 5: 0.03%

Output Distribution: Random.normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 656ns, Mid: 750ns, Max: 1312ns
Raw Samples: -6.605149652748213, -1.5822738563909715, 2.645709482120173, -3.172394906264029, -3.601616817669597
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -12.097844491985327
 Median: (-0.026603985146149922, -0.02560570474218634)
 Maximum: 11.773626067507772
 Mean: -0.03880432768221441
 Std Deviation: 2.8228009237952016
Post-processor Distribution using round method:
 -12: 0.01%
 -11: 0.03%
 -10: 0.01%
 -9: 0.09%
 -8: 0.34%
 -7: 0.75%
 -6: 1.65%
 -5: 2.99%
 -4: 4.98%
 -3: 8.16%
 -2: 10.76%
 -1: 13.53%
 0: 14.33%
 1: 13.71%
 2: 10.04%
 3: 8.4%
 4: 4.82%
 5: 2.96%
 6: 1.46%
 7: 0.55%
 8: 0.27%
 9: 0.12%
 10: 0.03%
 12: 0.01%

Output Distribution: normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 187ns
Raw Samples: -3.793855287737242, 0.9960074183329938, 4.646827400499933, 0.7522746841927623, 1.5745895766690858
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -11.113860638493062
 Median: (-0.005866695095333692, -0.0052394904243084585)
 Maximum: 11.53804154676824
 Mean: -0.008461925431601593
 Std Deviation: 2.8051746502040737
Post-processor Distribution using round method:
 -11: 0.02%
 -9: 0.07%
 -8: 0.35%
 -7: 0.74%
 -6: 1.59%
 -5: 3.05%
 -4: 4.96%
 -3: 7.17%
 -2: 11.49%
 -1: 13.52%
 0: 14.22%
 1: 12.99%
 2: 11.62%
 3: 7.89%
 4: 4.95%
 5: 3.01%
 6: 1.49%
 7: 0.47%
 8: 0.21%
 9: 0.12%
 10: 0.03%
 11: 0.03%
 12: 0.01%

Output Distribution: Random.lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 781ns, Mid: 875ns, Max: 1812ns
Raw Samples: 1.4607982840927791, 0.6362952539342507, 0.6681830357930688, 0.7417889882953694, 0.5897777249517009
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.1806823082218572
 Median: (0.9969168838767447, 0.996927640071643)
 Maximum: 6.501335063043788
 Mean: 1.1281725417388784
 Std Deviation: 0.6025357619207572
Post-processor Distribution using round method:
 0: 8.54%
 1: 70.97%
 2: 17.1%
 3: 2.83%
 4: 0.41%
 5: 0.11%
 6: 0.03%
 7: 0.01%

Output Distribution: lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 812ns
Raw Samples: 2.2311127724195376, 1.381697258064298, 1.064860406973389, 1.773220257987143, 1.1067339988312541
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.15826915601285957
 Median: (0.9904209337904174, 0.9905808875424859)
 Maximum: 7.47389854160491
 Mean: 1.1225167200192139
 Std Deviation: 0.5894445805924385
Post-processor Distribution using round method:
 0: 8.42%
 1: 71.51%
 2: 17.03%
 3: 2.47%
 4: 0.48%
 5: 0.06%
 6: 0.02%
 7: 0.01%

Output Distribution: Random.vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 937ns
Raw Samples: 6.171255491527489, 5.843547118553298, 5.949102916012425, 4.621930584214417, 3.5857589190647206
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0005094045909836397
 Median: (3.1127804266091728, 3.1134341115373294)
 Maximum: 6.282312906997316
 Mean: 3.129350314605287
 Std Deviation: 1.812655550665458
Post-processor Distribution using floor method:
 0: 15.84%
 1: 16.47%
 2: 16.0%
 3: 15.51%
 4: 15.74%
 5: 16.03%
 6: 4.41%

Output Distribution: vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 62ns, Mid: 77ns, Max: 156ns
Raw Samples: 3.542025025230099, 3.9304786155181977, 0.9362327767170853, 0.5516748988636856, 2.3901039085881153
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00010377605157448817
 Median: (3.1729866445710755, 3.1739098889299058)
 Maximum: 6.283126920075875
 Mean: 3.1533801005368574
 Std Deviation: 1.801236662762218
Post-processor Distribution using floor method:
 0: 15.55%
 1: 15.96%
 2: 15.41%
 3: 16.64%
 4: 16.1%
 5: 15.97%
 6: 4.37%

Output Distribution: Random.triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 500ns, Mid: 500ns, Max: 781ns
Raw Samples: 1.7868629205605888, 1.069689050288634, 1.5655547232869633, 2.6723959272391538, 5.145161763479783
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0006479019883816051
 Median: (2.9444476974473215, 2.946900841940371)
 Maximum: 9.947730376271611
 Mean: 3.3199881129814037
 Std Deviation: 2.3315330668208434
Post-processor Distribution using floor method:
 0: 18.44%
 1: 17.28%
 2: 15.15%
 3: 13.92%
 4: 11.08%
 5: 8.34%
 6: 7.08%
 7: 4.88%
 8: 2.89%
 9: 0.94%

Output Distribution: triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 1.0123369586885145, 7.244811650361144, 2.0252635417689757, 2.829584337354496, 1.5382101020409245
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0006758128883810333
 Median: (2.9699453029469582, 2.970540680382492)
 Maximum: 9.89929739914366
 Mean: 3.3549922690894998
 Std Deviation: 2.3713024958653817
Post-processor Distribution using floor method:
 0: 19.36%
 1: 16.52%
 2: 14.66%
 3: 13.01%
 4: 10.95%
 5: 9.11%
 6: 7.08%
 7: 5.2%
 8: 3.17%
 9: 0.94%

Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 750ns, Mid: 812ns, Max: 1562ns
Raw Samples: 2, 1, 7, 7, 6
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5071
 Std Deviation: 2.86663066109583
Sample Distribution:
 0: 10.14%
 1: 9.62%
 2: 9.67%
 3: 10.33%
 4: 10.45%
 5: 9.87%
 6: 9.76%
 7: 10.08%
 8: 10.23%
 9: 9.85%

Output Distribution: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 156ns
Raw Samples: 0, 9, 7, 2, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4751
 Std Deviation: 2.8657985396965735
Sample Distribution:
 0: 10.39%
 1: 9.69%
 2: 9.79%
 3: 10.29%
 4: 10.23%
 5: 10.06%
 6: 10.05%
 7: 9.98%
 8: 9.69%
 9: 9.83%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 3031ns, Mid: 3093ns, Max: 6000ns
Raw Samples: [4, 2, 1], [2, 5, 2], [6, 0, 7], [7, 3, 1], [6, 1, 5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9768
 Std Deviation: 2.4436159448425174
Sample Distribution:
 0: 19.01%
 1: 16.09%
 2: 14.21%
 3: 12.03%
 4: 11.5%
 5: 9.18%
 6: 7.33%
 7: 5.51%
 8: 3.63%
 9: 1.51%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 1906ns, Mid: 1937ns, Max: 2187ns
Raw Samples: [4, 4, 3], [3, 2, 7], [8, 2, 8], [0, 9, 1], [5, 5, 3]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9814
 Std Deviation: 2.4560654033894482
Sample Distribution:
 0: 18.28%
 1: 17.01%
 2: 14.52%
 3: 12.19%
 4: 10.7%
 5: 9.38%
 6: 6.92%
 7: 5.66%
 8: 3.38%
 9: 1.96%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 2562ns, Mid: 2593ns, Max: 3093ns
Raw Samples: [7, 1, 2], [2, 0, 2], [2, 4, 4], [3, 3, 2], [3, 3, 6]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0004
 Std Deviation: 2.461545400876461
Sample Distribution:
 0: 18.16%
 1: 16.9%
 2: 14.15%
 3: 12.5%
 4: 11.03%
 5: 8.91%
 6: 7.22%
 7: 5.68%
 8: 3.46%
 9: 1.99%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 1437ns, Mid: 1468ns, Max: 3125ns
Raw Samples: [2, 1, 1], [0, 0, 1], [1, 2, 4], [3, 3, 1], [3, 5, 3]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9896
 Std Deviation: 2.445872046736481
Sample Distribution:
 0: 18.64%
 1: 16.1%
 2: 14.15%
 3: 12.98%
 4: 10.89%
 5: 9.12%
 6: 7.3%
 7: 5.6%
 8: 3.52%
 9: 1.7%

Timer only: _random.shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 6687ns, Mid: 6937ns, Max: 10312ns

Timer only: shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 343ns, Mid: 375ns, Max: 812ns

Timer only: knuth(some_list) of size 10:
Approximate Single Execution Time: Min: 812ns, Mid: 843ns, Max: 1625ns

Timer only: fisher_yates(some_list) of size 10:
Approximate Single Execution Time: Min: 906ns, Mid: 937ns, Max: 2031ns

Output Distribution: Random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 4062ns, Mid: 4156ns, Max: 7125ns
Raw Samples: [2, 0, 1], [3, 9, 4], [4, 5, 3], [0, 8, 6], [1, 7, 5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5256
 Std Deviation: 2.868408516362632
Sample Distribution:
 0: 10.06%
 1: 9.67%
 2: 10.02%
 3: 9.63%
 4: 9.88%
 5: 10.24%
 6: 10.04%
 7: 10.49%
 8: 10.16%
 9: 9.81%

Output Distribution: sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 875ns, Mid: 906ns, Max: 1125ns
Raw Samples: [3, 0, 2], [4, 7, 0], [3, 8, 1], [0, 8, 7], [2, 9, 0]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5041
 Std Deviation: 2.869530730042992
Sample Distribution:
 0: 10.2%
 1: 9.36%
 2: 10.53%
 3: 9.84%
 4: 9.85%
 5: 10.19%
 6: 9.92%
 7: 10.12%
 8: 10.15%
 9: 9.84%


Total Test Time: 1.593 sec

```
