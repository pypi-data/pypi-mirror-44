#pragma once
#include <cstdlib>
#include <cmath>
#include <random>
#include <vector>
#include <algorithm>


namespace Pyewacket {
using Integer = long long;
using Float = double;
using Bool = bool;
static const Float PI = 4 * std::atan(1);
static const Float TAU = PI * 2;
static std::random_device hardware_seed;
static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 10>, 256> hurricane { hardware_seed() };

template <typename Number>
auto smart_clamp(Number target, Number left_limit, Number right_limit) {
    return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
}

template <typename Function, typename Number>
auto analytic_continuation(Function && func, Number number) {
    const Number minimum { -std::numeric_limits<Number>::max() };
    const Number maximum { std::numeric_limits<Number>::max() };
    const Number num { smart_clamp(number, minimum, maximum) };
    if (num < 0) return -func(-num);
    if (num == 0) return Number(0);
    return func(num);
}

Float generate_canonical() {
    return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
}

Integer random_int(Integer left_limit, Integer right_limit) {
    std::uniform_int_distribution<Integer> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(hurricane);
}

Float random_float(Float left_limit, Float right_limit) {
    std::uniform_real_distribution<Float> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(hurricane);
}

Float random_exponential(Float lambda_rate) {
    std::exponential_distribution<Float> distribution {
        lambda_rate
    };
    return distribution(hurricane);
}

Float random_gamma(Float shape, Float scale) {
    std::gamma_distribution<Float> distribution {
        shape,
        scale
    };
    return distribution(hurricane);
}

Float random_weibull(Float shape, Float scale) {
    std::weibull_distribution<Float> distribution {
        shape,
        scale
    };
    return distribution(hurricane);
}

Float random_normal(Float mean, Float std_dev) {
    std::normal_distribution<Float> distribution {
        mean,
        std_dev
    };
    return distribution(hurricane);
}

Float random_log_normal(Float log_mean, Float log_deviation) {
    std::lognormal_distribution<Float> distribution {
        log_mean,
        log_deviation
    };
    return distribution(hurricane);
}

Integer min_int() {
    return -std::numeric_limits<Integer>::max();
}

Integer max_int() {
    return std::numeric_limits<Integer>::max();
}

Float min_float() {
    return -std::numeric_limits<Float>::max();
}

Float max_float() {
    return std::numeric_limits<Float>::max();
}

Float min_below_zero() {
    return std::nextafter(0.0, std::numeric_limits<Float>::lowest());
}

Float min_above_zero() {
    return std::nextafter(0.0, std::numeric_limits<Float>::max());
}

Integer random_below(Integer number) {
    if (number > 0) {
        std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
        return distribution(hurricane);
    } else return analytic_continuation(random_below, number);
}

Integer randrange(Integer start, Integer stop, int step) {
    const int step_by = std::abs(step);
    if (stop == 0 and step_by == 1) return random_below(start);
    const Integer width = std::max(start, stop) - std::min(start, stop);
    if (step_by == 1) return start + random_below(width);
    if (start < stop) return start + step_by * random_below((width + step_by - 1) / step_by);
    if (start > stop)  return stop + step_by * random_below((width + step_by - 1) / step_by);
    else return start;
}

Float betavariate(Float alpha, Float beta) {
    const Float y = random_gamma(alpha, 1.0);
    if (y == 0) return 0.0;
    return y / (y + random_gamma(beta, 1.0));
}

Float paretovariate(Float alpha) {
    const Float u = 1.0 - generate_canonical();
    return 1.0 / std::pow(u, 1.0 / alpha);
}

Float vonmisesvariate(Float mu, Float kappa) {
    if (kappa <= 0.000001) {
        return TAU * generate_canonical();
    }
    const Float s = 0.5 / kappa;
    const Float r = s + std::sqrt(1 + s * s);
    Float z;
    while (true) {
        const Float u1 = generate_canonical();
        z = std::cos(PI * u1);
        const Float d = z / (r + z);
        const Float u2 = generate_canonical();
        if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
    }
    const Float q = 1.0 / r;
    const Float f = (q + z) / (1.0 + q * z);
    const Float u3 = generate_canonical();
    if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
    else return std::fmod(mu - std::acos(f), TAU);
}

Float triangular(Float low, Float high, Float mode) {
    if (high - low == 0) return low;
    Float u = generate_canonical();
    Float c = (mode - low) / (high - low);
    if (u > c) {
        u = 1.0 - u;
        c = 1.0 - c;
        const Float temp = low;
        low = high;
        high = temp;
    }
    return low + (high - low) * std::sqrt(u * c);
}

} // end namespace Pyewacket
