#pragma once
#include <cstdlib>
#include <cmath>
#include <random>
#include <vector>
#include <algorithm>


namespace Fortuna {
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

Float random() {
    return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
}

Bool random_bool(Float truth_factor) {
    std::bernoulli_distribution distribution {
        smart_clamp(truth_factor, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer randint(Integer left_limit, Integer right_limit) {
    std::uniform_int_distribution<Integer> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(hurricane);
}

Integer binomial(Integer number_of_trials, Float probability) {
    std::binomial_distribution<Integer> distribution {
        std::max(number_of_trials, Integer(1)),
        smart_clamp(probability, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer negative_binomial(Integer number_of_trials, Float probability) {
    std::negative_binomial_distribution<Integer> distribution {
        std::max(number_of_trials, Integer(1)),
        smart_clamp(probability, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer geometric(Float probability) {
    std::geometric_distribution<Integer> distribution {
        smart_clamp(probability, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer poisson(Float mean) {
    std::poisson_distribution<Integer> distribution {
        mean
    };
    return distribution(hurricane);
}

Integer discrete(size_t count, Float xmin, Float xmax, int step) {
    std::discrete_distribution<Integer> distribution {
        count,
        std::max(xmin, 0.0),
        std::max(xmax, 0.0),
        [step](auto x) { return x + step; }
    };
    return distribution(hurricane);
}

Float uniform(Float left_limit, Float right_limit) {
    std::uniform_real_distribution<Float> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(hurricane);
}

Float exponential(Float lambda_rate) {
    std::exponential_distribution<Float> distribution {
        lambda_rate
    };
    return distribution(hurricane);
}

Float gamma(Float shape, Float scale) {
    std::gamma_distribution<Float> distribution {
        shape,
        scale
    };
    return distribution(hurricane);
}

Float weibull(Float shape, Float scale) {
    std::weibull_distribution<Float> distribution {
        shape,
        scale
    };
    return distribution(hurricane);
}

Float extreme_value(Float location, Float scale) {
    std::extreme_value_distribution<Float> distribution {
        location,
        scale
    };
    return distribution(hurricane);
}

Float normal(Float mean, Float std_dev) {
    std::normal_distribution<Float> distribution {
        mean,
        std_dev
    };
    return distribution(hurricane);
}

Float log_normal(Float log_mean, Float log_deviation) {
    std::lognormal_distribution<Float> distribution {
        log_mean,
        log_deviation
    };
    return distribution(hurricane);
}

Float chi_squared(Float degrees_of_freedom) {
    std::chi_squared_distribution<Float> distribution {
        std::max(degrees_of_freedom, Float(0.0))
    };
    return distribution(hurricane);
}

Float cauchy(Float location, Float scale) {
    std::cauchy_distribution<Float> distribution {
        location,
        scale
    };
    return distribution(hurricane);
}

Float fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) {
    std::fisher_f_distribution<Float> distribution {
        std::max(degrees_of_freedom_1, Float(0.0)),
        std::max(degrees_of_freedom_2, Float(0.0))
    };
    return distribution(hurricane);
}

Float student_t(Float degrees_of_freedom) {
    std::student_t_distribution<Float> distribution {
        std::max(degrees_of_freedom, Float(0.0))
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

Integer randbelow(Integer number) {
    if (number > 0) {
        std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
        return distribution(hurricane);
    } else return analytic_continuation(randbelow, number);
}

Integer fuzzy_clamp(Integer target, Integer upper_bound) {
    if (target >= 0 and target < upper_bound) return target;
    else return randbelow(upper_bound);
}

Integer d(Integer sides) {
    if (sides > 0) {
        return randint(1, sides);
    } else return analytic_continuation(d, sides);
}

Integer dice(Integer rolls, Integer sides) {
    if (rolls > 0) {
        Integer total = 0;
        for (auto i {0}; i < rolls; ++i) total += d(sides);
        return total;
    }
    if (rolls == 0) return 0;
    return -dice(-rolls, sides);
}

Integer ability_dice(Integer num) {
    const Integer n { smart_clamp(num, Integer(3), Integer(9)) };
    if (n == 3) return dice(3, 6);
    std::vector<Integer> theRolls(n);
    std::generate(begin(theRolls), end(theRolls), []() { return d(6); });
    std::partial_sort(begin(theRolls), begin(theRolls) + 3, end(theRolls), std::greater<Integer>());
    return std::accumulate(begin(theRolls), begin(theRolls) + 3, 0);
}

Integer plus_or_minus(Integer number) {
    return randint(-number, number);
}

Integer plus_or_minus_linear(Integer number) {
    const Integer num { std::abs(number) };
    return dice(2, num + 1) - (num + 2);
}

Bool percent_true(Float truth_factor) {
    return uniform(0.0, 100.0) < truth_factor;
}

Integer front_gauss(Integer number) {
    if (number > 0) { // Narrowing Float -> Integer
        const Integer result { Integer(std::floor(gamma(1.0, number / 10.0))) };
        return fuzzy_clamp(result, number);
    } else return analytic_continuation(front_gauss, number);
}

Integer middle_gauss(Integer number) {
    if (number > 0) { // Narrowing Float -> Integer
        const Integer result { Integer(std::floor(normal(number / 2.0, number / 10.0))) };
        return fuzzy_clamp(result, number);
    } else return analytic_continuation(middle_gauss, number);
}

Integer back_gauss(Integer number) {
    if (number > 0) {
        return number - front_gauss(number) - 1;
    } else return analytic_continuation(back_gauss, number);
}

Integer quantum_gauss(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return front_gauss(number);
    if (rand_num == 2) return middle_gauss(number);
    return back_gauss(number);
}

Integer front_poisson(Integer number) {
    if (number > 0) {
        const Integer result { poisson(number / PI) };
        return fuzzy_clamp(result, number);
    } else return analytic_continuation(front_poisson, number);
}

Integer back_poisson(Integer number) {
    if (number > 0) {
        const Integer result { number - front_poisson(number) - 1 };
        return fuzzy_clamp(result, number);
    } else return analytic_continuation(back_poisson, number);
}

Integer middle_poisson(Integer number) {
    if (number > 0) {
        if (percent_true(50.0)) return front_poisson(number);
        else return back_poisson(number);
    } else return analytic_continuation(middle_poisson, number);
}

Integer quantum_poisson(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return front_poisson(number);
    if (rand_num == 2) return middle_poisson(number);
    return back_poisson(number);
}

Integer front_geometric(Integer number) {
    if (number > 0) {
        const Integer spread = number - 1;
        Integer result { plus_or_minus_linear(spread)};
        while (result < 0) result = plus_or_minus_linear(spread);
        return result;
    } else return analytic_continuation(front_geometric, number);
}

Integer back_geometric(Integer number) {
    if (number > 0) {
        const Integer spread = number - 1;
        Integer result { plus_or_minus_linear(spread)};
        while (result < 0) result = plus_or_minus_linear(spread);
        return spread - result;
    } else return analytic_continuation(front_geometric, number);
}

Integer middle_geometric(Integer number) {
    if (number > 0) {
        const Integer half {number / 2};
        if (number % 2 == 1) return half + plus_or_minus_linear(half);
        if (percent_true(50)) return back_geometric(half);
        return half + front_geometric(half);
    } else return analytic_continuation(middle_geometric, number);
}

Integer quantum_geometric(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return front_geometric(number);
    if (rand_num == 2) return middle_geometric(number);
    else return back_geometric(number);
}

Integer quantum_monty(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return quantum_geometric(number);
    if (rand_num == 2) return quantum_gauss(number);
    return quantum_poisson(number);
}

Integer randrange(Integer start, Integer stop, int step) {
    const int step_by = std::abs(step);
    if (stop == 0 and step_by == 1) return randbelow(start);
    const Integer width = std::max(start, stop) - std::min(start, stop);
    if (step_by == 1) return start + randbelow(width);
    if (start < stop) return start + step_by * randbelow((width + step_by - 1) / step_by);
    if (start > stop) return stop + step_by * randbelow((width + step_by - 1) / step_by);
    else return start;
}

Float betavariate(Float alpha, Float beta) {
    const Float y = gamma(alpha, 1.0);
    if (y == 0) return 0.0;
    return y / (y + gamma(beta, 1.0));
}

Float paretovariate(Float alpha) {
    const Float u = 1.0 - random();
    return 1.0 / std::pow(u, 1.0 / alpha);
}

Float vonmisesvariate(Float mu, Float kappa) {
    if (kappa <= 0.000001) {
        return TAU * random();
    }
    const Float s = 0.5 / kappa;
    const Float r = s + std::sqrt(1 + s * s);
    Float z;
    while (true) {
        const Float u1 = random();
        z = std::cos(PI * u1);
        const Float d = z / (r + z);
        const Float u2 = random();
        if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
    }
    const Float q = 1.0 / r;
    const Float f = (q + z) / (1.0 + q * z);
    const Float u3 = random();
    if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
    else return std::fmod(mu - std::acos(f), TAU);
}

Float triangular(Float low, Float high, Float mode) {
    if (high - low == 0) return low;
    Float u = random();
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

} // end namespace Fortuna
