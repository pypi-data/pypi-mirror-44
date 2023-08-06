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
Approximate Single Execution Time: Min: 562ns, Mid: 625ns, Max: 812ns
Raw Samples: 3, 9, 0, 2, 5
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5067
 Std Deviation: 2.8606596175261285
Sample Distribution:
 0: 9.81%
 1: 10.13%
 2: 9.81%
 3: 10.08%
 4: 9.65%
 5: 10.49%
 6: 10.14%
 7: 10.08%
 8: 10.06%
 9: 9.75%

Output Distribution: randbelow(10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 562ns
Raw Samples: 4, 9, 0, 6, 6
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4252
 Std Deviation: 2.878338660294222
Sample Distribution:
 0: 10.38%
 1: 10.56%
 2: 10.5%
 3: 9.83%
 4: 9.54%
 5: 9.85%
 6: 9.98%
 7: 10.15%
 8: 9.76%
 9: 9.45%

Output Distribution: Random.randint(1, 10)
Approximate Single Execution Time: Min: 1218ns, Mid: 1343ns, Max: 2250ns
Raw Samples: 8, 8, 8, 7, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.5075
 Std Deviation: 2.8629640944902945
Sample Distribution:
 1: 9.63%
 2: 10.08%
 3: 10.32%
 4: 9.92%
 5: 10.1%
 6: 9.87%
 7: 9.81%
 8: 10.2%
 9: 10.37%
 10: 9.7%

Output Distribution: randint(1, 10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 125ns
Raw Samples: 8, 10, 1, 5, 7
Test Samples: 10000
Sample Statistics:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4454
 Std Deviation: 2.8590271498578606
Sample Distribution:
 1: 10.16%
 2: 9.76%
 3: 10.97%
 4: 10.02%
 5: 9.84%
 6: 9.97%
 7: 10.1%
 8: 9.92%
 9: 9.81%
 10: 9.45%

Output Distribution: Random.randrange(0, 10, 2)
Approximate Single Execution Time: Min: 1312ns, Mid: 1359ns, Max: 1531ns
Raw Samples: 4, 6, 2, 6, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 3.9732
 Std Deviation: 2.8448007046373056
Sample Distribution:
 0: 20.63%
 2: 19.99%
 4: 19.42%
 6: 20.01%
 8: 19.95%

Output Distribution: randrange(0, 10, 2)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 2, 6, 0, 8, 2
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.0144
 Std Deviation: 2.8367229931267475
Sample Distribution:
 0: 19.99%
 2: 19.87%
 4: 19.95%
 6: 19.81%
 8: 20.38%

Output Distribution: Random.random()
Approximate Single Execution Time: Min: 31ns, Mid: 46ns, Max: 125ns
Raw Samples: 0.07229308495175646, 0.8602350828853721, 0.24894500706196898, 0.018388454848522917, 0.411281979102499
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0004142529985969867
 Median: (0.49761505752331114, 0.4976715372896202)
 Maximum: 0.9999816182206303
 Mean: 0.4971865692661913
 Std Deviation: 0.28883327191526004
Post-processor Distribution using round method:
 0: 50.31%
 1: 49.69%

Output Distribution: random()
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 93ns
Raw Samples: 0.531046238669966, 0.26820757887103647, 0.5553073358640125, 0.5823219419921947, 0.16502703852700476
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0001274730861330612
 Median: (0.4962008695477048, 0.49621891252284905)
 Maximum: 0.9999511997132907
 Mean: 0.49863280373130414
 Std Deviation: 0.2894267188000272
Post-processor Distribution using round method:
 0: 50.31%
 1: 49.69%

Output Distribution: Random.uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 218ns, Mid: 250ns, Max: 531ns
Raw Samples: 5.525177814743438, 5.764645499500939, 4.379157469908382, 0.1953788311692395, 7.258890877245067
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00034532132600517684
 Median: (4.909703381366731, 4.90987852042975)
 Maximum: 9.995713074296708
 Mean: 4.955172409875171
 Std Deviation: 2.874844231778139
Post-processor Distribution using floor method:
 0: 9.86%
 1: 10.35%
 2: 10.49%
 3: 10.14%
 4: 10.1%
 5: 9.88%
 6: 10.13%
 7: 9.26%
 8: 10.0%
 9: 9.79%

Output Distribution: uniform(0.0, 10.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 93ns
Raw Samples: 8.237658467499077, 1.9447965197101589, 4.074396024171002, 5.2552727697275206, 1.814249893659937
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0011603311977625512
 Median: (5.033699939622926, 5.034673156573187)
 Maximum: 9.999710542635528
 Mean: 5.007505995701304
 Std Deviation: 2.9008833515201045
Post-processor Distribution using floor method:
 0: 10.52%
 1: 9.6%
 2: 9.96%
 3: 9.77%
 4: 9.78%
 5: 10.0%
 6: 9.89%
 7: 10.24%
 8: 10.19%
 9: 10.05%

Output Distribution: Random.expovariate(1.0)
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 531ns
Raw Samples: 2.6776786163459336, 1.9703498738728153, 0.06359879974376102, 0.6749054263586046, 0.8616286574236739
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.3292391585541781e-05
 Median: (0.6864101203458027, 0.6864664023409701)
 Maximum: 10.071351794979797
 Mean: 1.0016806961714704
 Std Deviation: 1.01027537926835
Post-processor Distribution using floor method:
 0: 63.63%
 1: 22.62%
 2: 8.79%
 3: 3.16%
 4: 1.09%
 5: 0.44%
 6: 0.13%
 7: 0.12%
 9: 0.01%
 10: 0.01%

Output Distribution: expovariate(1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 218ns
Raw Samples: 0.2591668904824361, 1.220033324443836, 1.2589153980859262, 1.8141038461590242, 0.22302637399651437
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 5.363523068495954e-05
 Median: (0.6780536661311757, 0.678095983283787)
 Maximum: 12.122975537046992
 Mean: 1.0001183846253474
 Std Deviation: 1.0281650348211395
Post-processor Distribution using floor method:
 0: 63.8%
 1: 22.84%
 2: 8.11%
 3: 3.14%
 4: 1.31%
 5: 0.44%
 6: 0.21%
 7: 0.09%
 8: 0.04%
 9: 0.01%
 12: 0.01%

Output Distribution: Random.gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 1156ns, Mid: 1375ns, Max: 3031ns
Raw Samples: 2.930737428639916, 1.6089426458490308, 2.933961741202261, 2.446147973753288, 3.4847523637701694
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00900820023111997
 Median: (1.663874437265986, 1.6641862983644296)
 Maximum: 12.997025910533106
 Mean: 2.002913425104
 Std Deviation: 1.4193481886438644
Post-processor Distribution using round method:
 0: 9.08%
 1: 35.36%
 2: 26.64%
 3: 15.05%
 4: 7.69%
 5: 3.45%
 6: 1.66%
 7: 0.6%
 8: 0.24%
 9: 0.1%
 10: 0.07%
 11: 0.04%
 12: 0.01%
 13: 0.01%

Output Distribution: gammavariate(2.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 250ns
Raw Samples: 1.5934097770216602, 2.0976222943756864, 4.428438620998049, 1.3240329061088847, 5.555736742677747
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.012881814639218336
 Median: (1.6830491245812589, 1.6832923447947636)
 Maximum: 12.522717355653086
 Mean: 1.9816805343554134
 Std Deviation: 1.3986174254441563
Post-processor Distribution using round method:
 0: 9.36%
 1: 34.63%
 2: 27.91%
 3: 14.86%
 4: 7.46%
 5: 3.25%
 6: 1.37%
 7: 0.72%
 8: 0.24%
 9: 0.12%
 10: 0.04%
 11: 0.02%
 12: 0.01%
 13: 0.01%

Output Distribution: Random.weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 406ns, Mid: 406ns, Max: 593ns
Raw Samples: 3.095075752506419, 1.6986934763006856, 0.8914899120856806, 1.4761170738419767, 0.9701692276859157
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0001527311576566805
 Median: (0.678967074123007, 0.6790170191957153)
 Maximum: 8.844290630683473
 Mean: 1.0023835012965534
 Std Deviation: 1.013585477388962
Post-processor Distribution using floor method:
 0: 63.15%
 1: 23.33%
 2: 8.21%
 3: 3.35%
 4: 1.24%
 5: 0.42%
 6: 0.2%
 7: 0.06%
 8: 0.04%

Output Distribution: weibullvariate(1.0, 1.0)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 156ns
Raw Samples: 2.873982924025877, 1.5681759110159017, 1.3441626182011606, 1.5679800856302577, 0.8468533167312312
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00034914990638296124
 Median: (0.6775732015358351, 0.6776806747843829)
 Maximum: 10.496669381752696
 Mean: 0.9933286298865197
 Std Deviation: 0.9923402549423264
Post-processor Distribution using floor method:
 0: 63.44%
 1: 23.07%
 2: 8.59%
 3: 3.12%
 4: 1.23%
 5: 0.33%
 6: 0.13%
 7: 0.05%
 8: 0.02%
 9: 0.01%
 10: 0.01%

Output Distribution: Random.betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 2500ns, Mid: 2640ns, Max: 4156ns
Raw Samples: 0.4301362281370428, 0.23015593592316924, 0.8169209272662321, 0.7038605228713546, 0.6780825464012005
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00938259748538607
 Median: (0.49974196445592106, 0.49976324216757223)
 Maximum: 0.983983033076689
 Mean: 0.5009965977308289
 Std Deviation: 0.1895816104311026
Post-processor Distribution using round method:
 0: 50.05%
 1: 49.95%

Output Distribution: betavariate(3.0, 3.0)
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 1093ns
Raw Samples: 0.8754280072645699, 0.3392411342681032, 0.7477340065884961, 0.44616302461780427, 0.35518361123876874
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.006314868092072921
 Median: (0.499047241764077, 0.4990622244974764)
 Maximum: 0.9764916815022566
 Mean: 0.49884440268069874
 Std Deviation: 0.18910857110636597
Post-processor Distribution using round method:
 0: 50.22%
 1: 49.78%

Output Distribution: Random.paretovariate(4.0)
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 2812ns
Raw Samples: 1.217271052520398, 1.2286194362793585, 1.2328435049924706, 1.0279937693057852, 1.6160428543655818
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000166382942022
 Median: (1.1928918105852682, 1.1930168484427572)
 Maximum: 9.987282263745515
 Mean: 1.3373355259564115
 Std Deviation: 0.46056052023480254
Post-processor Distribution using floor method:
 1: 93.76%
 2: 4.9%
 3: 0.91%
 4: 0.3%
 5: 0.09%
 6: 0.01%
 7: 0.01%
 8: 0.01%
 9: 0.01%

Output Distribution: paretovariate(4.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 187ns
Raw Samples: 1.0372484307150154, 1.2329259167900564, 1.0378171283362163, 1.0237858863555835, 1.1708734470833795
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 1.0000570265854005
 Median: (1.1870723704535302, 1.1870857748571313)
 Maximum: 8.868943331764743
 Mean: 1.338843629481537
 Std Deviation: 0.4755182577644297
Post-processor Distribution using floor method:
 1: 93.4%
 2: 5.15%
 3: 1.06%
 4: 0.2%
 5: 0.1%
 6: 0.07%
 8: 0.02%

Output Distribution: Random.gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 562ns, Mid: 593ns, Max: 781ns
Raw Samples: 1.6437732541238481, 0.9045565845246568, 1.873735798046797, 0.9655830054832201, 1.5438984295182383
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.695651320000329
 Median: (1.0163377812134067, 1.0165382178417801)
 Maximum: 4.669678689891665
 Mean: 1.0154819988350552
 Std Deviation: 0.997442963228864
Post-processor Distribution using round method:
 -3: 0.02%
 -2: 0.54%
 -1: 5.74%
 0: 23.48%
 1: 38.89%
 2: 24.45%
 3: 6.22%
 4: 0.59%
 5: 0.07%

Output Distribution: gauss(1.0, 1.0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 281ns
Raw Samples: 0.07418013156186007, 2.3116219924787544, 0.7712003219509719, 1.6827234054554534, 0.7561100123804949
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -2.613051910948324
 Median: (0.99706046885693, 0.9973090062063324)
 Maximum: 5.117354296186206
 Mean: 0.9932073296932908
 Std Deviation: 0.9944420550458642
Post-processor Distribution using round method:
 -3: 0.01%
 -2: 0.68%
 -1: 5.95%
 0: 24.34%
 1: 38.27%
 2: 24.18%
 3: 5.96%
 4: 0.59%
 5: 0.02%

Output Distribution: Random.normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 625ns, Mid: 718ns, Max: 843ns
Raw Samples: 0.1568317911851612, -1.7135073684786395, -0.7825887571855921, -1.3755734652779912, 1.6500439793580357
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -10.545874445446161
 Median: (0.009367430610897516, 0.009939070462636954)
 Maximum: 10.825445486601907
 Mean: 0.007569702062889325
 Std Deviation: 2.806905721968985
Post-processor Distribution using round method:
 -11: 0.01%
 -10: 0.01%
 -9: 0.07%
 -8: 0.33%
 -7: 0.58%
 -6: 1.38%
 -5: 2.97%
 -4: 5.4%
 -3: 8.17%
 -2: 10.65%
 -1: 13.2%
 0: 14.36%
 1: 13.07%
 2: 11.53%
 3: 7.79%
 4: 5.09%
 5: 2.76%
 6: 1.54%
 7: 0.63%
 8: 0.3%
 9: 0.12%
 10: 0.02%
 11: 0.02%

Output Distribution: normalvariate(0.0, 2.8)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 375ns
Raw Samples: 4.76047696165964, 1.367855692990678, 0.756856014800625, 1.8623146778043815, -5.873502914588222
Test Samples: 10000
Pre-processor Statistics:
 Minimum: -9.452627636959287
 Median: (0.04044654608052613, 0.041099607025025554)
 Maximum: 9.733007571445148
 Mean: 0.0391045966930773
 Std Deviation: 2.7752729663402818
Post-processor Distribution using round method:
 -9: 0.15%
 -8: 0.26%
 -7: 0.58%
 -6: 1.39%
 -5: 2.77%
 -4: 4.89%
 -3: 7.66%
 -2: 11.25%
 -1: 13.61%
 0: 13.9%
 1: 13.4%
 2: 11.27%
 3: 8.33%
 4: 5.28%
 5: 2.88%
 6: 1.34%
 7: 0.71%
 8: 0.23%
 9: 0.08%
 10: 0.02%

Output Distribution: Random.lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 781ns, Mid: 843ns, Max: 1281ns
Raw Samples: 0.5425531309955529, 1.6434968906960663, 0.760433521400606, 1.291850008407099, 1.0757510124828
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.15041364017087452
 Median: (0.9983196348095651, 0.9983313101316652)
 Maximum: 6.340841988813364
 Mean: 1.131457214217093
 Std Deviation: 0.6095437130673893
Post-processor Distribution using round method:
 0: 8.39%
 1: 71.03%
 2: 17.18%
 3: 2.7%
 4: 0.5%
 5: 0.16%
 6: 0.04%

Output Distribution: lognormvariate(0.0, 0.5)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 218ns
Raw Samples: 0.6129248056029938, 0.6408171651459367, 0.4459512390847495, 0.7104857368222225, 1.3227431017687497
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.15385491684270008
 Median: (0.9892762525524973, 0.9894307046485679)
 Maximum: 6.601665982597798
 Mean: 1.1288981525989366
 Std Deviation: 0.6036355238740567
Post-processor Distribution using round method:
 0: 8.19%
 1: 71.14%
 2: 17.29%
 3: 2.78%
 4: 0.52%
 5: 0.05%
 6: 0.02%
 7: 0.01%

Output Distribution: Random.vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 250ns, Mid: 281ns, Max: 406ns
Raw Samples: 1.7540399164054603, 2.769298869012951, 0.1370568724757728, 4.853499259939353, 3.251614491801985
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.0015254630637543968
 Median: (3.117107086426068, 3.117734803710674)
 Maximum: 6.279784684488067
 Mean: 3.1381864746088817
 Std Deviation: 1.8249855397482684
Post-processor Distribution using floor method:
 0: 15.88%
 1: 16.38%
 2: 15.81%
 3: 15.3%
 4: 15.95%
 5: 16.12%
 6: 4.56%

Output Distribution: vonmisesvariate(0, 0)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 250ns
Raw Samples: 4.753538382325427, 0.047904575481924415, 5.014996922719001, 2.5925958127850577, 1.3148235228936693
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00023327835266282075
 Median: (3.1178326605027378, 3.117835719260189)
 Maximum: 6.283042359465571
 Mean: 3.1254706779550436
 Std Deviation: 1.81493182749057
Post-processor Distribution using floor method:
 0: 16.14%
 1: 16.07%
 2: 16.13%
 3: 15.71%
 4: 15.57%
 5: 16.0%
 6: 4.38%

Output Distribution: Random.triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 468ns, Mid: 562ns, Max: 1125ns
Raw Samples: 5.7272616191143335, 0.5500466992775177, 4.515218849168195, 6.196474841833616, 2.392176147452984
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 5.8363896862090314e-06
 Median: (2.921419339585439, 2.9217742355925953)
 Maximum: 9.948066399569589
 Mean: 3.3391353525694463
 Std Deviation: 2.3714540149890224
Post-processor Distribution using floor method:
 0: 19.17%
 1: 16.75%
 2: 15.37%
 3: 12.8%
 4: 10.56%
 5: 9.04%
 6: 7.07%
 7: 5.12%
 8: 3.22%
 9: 0.9%

Output Distribution: triangular(0.0, 10.0, 0.0)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 125ns
Raw Samples: 4.155307330223458, 6.132767824726762, 2.9829393536211954, 3.972799260903778, 2.96278847969325
Test Samples: 10000
Pre-processor Statistics:
 Minimum: 0.00010195209721453047
 Median: (2.893320155483756, 2.8955828048533325)
 Maximum: 9.925242533317567
 Mean: 3.313249938726445
 Std Deviation: 2.351762233329837
Post-processor Distribution using floor method:
 0: 19.03%
 1: 16.88%
 2: 15.61%
 3: 12.87%
 4: 10.98%
 5: 8.82%
 6: 7.03%
 7: 4.76%
 8: 3.06%
 9: 0.96%

Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 718ns, Mid: 781ns, Max: 1656ns
Raw Samples: 1, 6, 6, 9, 0
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4533
 Std Deviation: 2.8848312489872807
Sample Distribution:
 0: 10.24%
 1: 10.48%
 2: 10.06%
 3: 10.22%
 4: 9.84%
 5: 9.72%
 6: 9.71%
 7: 9.87%
 8: 9.98%
 9: 9.88%

Output Distribution: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 125ns
Raw Samples: 9, 3, 5, 2, 1
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4926
 Std Deviation: 2.8680599395378192
Sample Distribution:
 0: 10.14%
 1: 9.81%
 2: 10.04%
 3: 9.92%
 4: 10.17%
 5: 10.17%
 6: 9.89%
 7: 9.96%
 8: 10.08%
 9: 9.82%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 3156ns, Mid: 3187ns, Max: 3593ns
Raw Samples: [2, 3, 7], [2, 7, 5], [0, 6, 5], [2, 5, 0], [3, 7, 5]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0033
 Std Deviation: 2.4429666224882935
Sample Distribution:
 0: 17.87%
 1: 16.38%
 2: 15.02%
 3: 12.49%
 4: 11.05%
 5: 8.99%
 6: 7.32%
 7: 5.43%
 8: 3.69%
 9: 1.76%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=3)
Approximate Single Execution Time: Min: 2031ns, Mid: 2906ns, Max: 5187ns
Raw Samples: [3, 5, 0], [6, 1, 3], [0, 0, 6], [4, 5, 5], [7, 1, 7]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9853
 Std Deviation: 2.4520369406915243
Sample Distribution:
 0: 18.16%
 1: 16.77%
 2: 14.63%
 3: 12.86%
 4: 10.52%
 5: 8.87%
 6: 7.0%
 7: 5.82%
 8: 3.58%
 9: 1.79%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 2531ns, Mid: 2827ns, Max: 9062ns
Raw Samples: [6, 3, 9], [4, 4, 5], [1, 1, 8], [6, 2, 5], [2, 9, 6]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0006
 Std Deviation: 2.468321069247291
Sample Distribution:
 0: 18.2%
 1: 16.69%
 2: 14.61%
 3: 12.53%
 4: 10.9%
 5: 8.48%
 6: 7.17%
 7: 5.6%
 8: 4.04%
 9: 1.78%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=3)
Approximate Single Execution Time: Min: 1468ns, Mid: 1500ns, Max: 1656ns
Raw Samples: [1, 1, 9], [4, 6, 0], [3, 1, 0], [3, 8, 1], [0, 0, 1]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0031
 Std Deviation: 2.474894523063565
Sample Distribution:
 0: 18.35%
 1: 16.9%
 2: 14.02%
 3: 12.38%
 4: 11.06%
 5: 9.0%
 6: 6.71%
 7: 5.87%
 8: 3.75%
 9: 1.96%

Timer only: _random.shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 6906ns, Mid: 7234ns, Max: 11718ns

Timer only: shuffle(some_list) of size 10:
Approximate Single Execution Time: Min: 437ns, Mid: 437ns, Max: 562ns

Timer only: knuth(some_list) of size 10:
Approximate Single Execution Time: Min: 875ns, Mid: 906ns, Max: 1031ns

Timer only: fisher_yates(some_list) of size 10:
Approximate Single Execution Time: Min: 1000ns, Mid: 1000ns, Max: 1031ns

Output Distribution: Random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 4125ns, Mid: 5280ns, Max: 9750ns
Raw Samples: [4, 9, 8], [0, 7, 4], [2, 5, 7], [0, 1, 4], [5, 7, 8]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4529
 Std Deviation: 2.854924981442589
Sample Distribution:
 0: 10.08%
 1: 10.34%
 2: 10.03%
 3: 10.04%
 4: 9.8%
 5: 10.19%
 6: 10.29%
 7: 10.3%
 8: 9.59%
 9: 9.34%

Output Distribution: sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Approximate Single Execution Time: Min: 812ns, Mid: 875ns, Max: 2156ns
Raw Samples: [4, 3, 0], [2, 3, 5], [5, 2, 3], [1, 7, 9], [6, 0, 3]
Test Samples: 10000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4786
 Std Deviation: 2.857334155440624
Sample Distribution:
 0: 9.85%
 1: 10.17%
 2: 10.01%
 3: 10.06%
 4: 10.35%
 5: 10.11%
 6: 9.93%
 7: 9.84%
 8: 10.04%
 9: 9.64%


Total Test Time: 1.708 sec

```
