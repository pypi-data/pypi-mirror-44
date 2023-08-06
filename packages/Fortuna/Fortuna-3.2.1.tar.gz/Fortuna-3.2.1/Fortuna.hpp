#pragma once
#include <cstdlib>
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace Fortuna {
    using Integer = long long;
    using Float = double;
    using Bool = bool;

    struct Storm {
        using MT64_SCRAM = std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256>;
        std::random_device hardware_seed;
        MT64_SCRAM hurricane { hardware_seed() };
        template <typename D>
        auto operator()(D distribution) {
            return distribution(hurricane);
        }
        auto set_seed(unsigned long long seed) -> void {
            MT64_SCRAM cyclone { seed == 0 ? hardware_seed() : seed };
            hurricane = cyclone;
        }
    } storm;

    template <typename Number>
    auto smart_clamp(Number target, Number left_limit, Number right_limit) -> Number {
        return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
    }

    template <typename Function, typename Number>
    auto analytic_continuation(Function && func, Number number) -> Number {
        auto const num = smart_clamp(number, -std::numeric_limits<Number>::max(), std::numeric_limits<Number>::max());
        if (num < 0) return -func(-num);
            else if (num == 0) return 0;
            else return func(num);
                }

    auto min_int() -> Integer { return -std::numeric_limits<Integer>::max(); }
    auto max_int() -> Integer { return std::numeric_limits<Integer>::max(); }
    auto min_float() -> Float { return -std::numeric_limits<Float>::max(); }
    auto max_float() -> Float { return std::numeric_limits<Float>::max(); }
    auto min_below() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    auto min_above() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }


    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(storm.hurricane);
    }

    auto uniform(Float left_limit, Float right_limit) -> Float {
        auto const distribution = std::uniform_real_distribution<Float> {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return storm(distribution);
    }

    auto randbelow(Integer number) -> Integer {
        if (number > 0) {
            auto const distribution = std::uniform_int_distribution<Integer> { 0, number - 1 };
            return storm(distribution);
        } else return analytic_continuation(randbelow, number);
    }

    auto randint(Integer left_limit, Integer right_limit) -> Integer {
        auto const distribution = std::uniform_int_distribution<Integer> {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return storm(distribution);
    }

    /// RNG
    auto bernoulli(Float truth_factor) -> Bool {
        auto const distribution = std::bernoulli_distribution {
            smart_clamp(truth_factor, 0.0, 1.0)
        };
        return storm(distribution);
    }

    auto binomial(Integer number_of_trials, Float probability) -> Integer {
        auto const distribution = std::binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return storm(distribution);
    }

    auto negative_binomial(Integer number_of_trials, Float probability) -> Integer {
        auto const distribution = std::negative_binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return storm(distribution);
    }

    auto geometric(Float probability) -> Integer {
        auto const distribution = std::geometric_distribution<Integer> { smart_clamp(probability, 0.0, 1.0) };
        return storm(distribution);
    }

    auto poisson(Float mean) -> Integer {
        auto const distribution = std::poisson_distribution<Integer> { mean };
        return storm(distribution);
    }

    auto expovariate(Float lambda_rate) -> Float {
        auto const distribution = std::exponential_distribution<Float> { lambda_rate };
        return storm(distribution);
    }

    auto gammavariate(Float shape, Float scale) -> Float {
        auto const distribution = std::gamma_distribution<Float> { shape, scale };
        return storm(distribution);
    }

    auto weibullvariate(Float shape, Float scale) -> Float {
        auto const distribution = std::weibull_distribution<Float> { shape, scale };
        return storm(distribution);
    }

    auto normalvariate(Float mean, Float std_dev) -> Float {
        auto const distribution = std::normal_distribution<Float> { mean, std_dev };
        return storm(distribution);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) -> Float {
        auto const distribution = std::lognormal_distribution<Float> { log_mean, log_deviation };
        return storm(distribution);
    }

    auto extreme_value(Float location, Float scale) -> Float {
        auto const distribution = std::extreme_value_distribution<Float> { location, scale };
        return storm(distribution);
    }

    auto chi_squared(Float degrees_of_freedom) -> Float {
        auto const distribution = std::chi_squared_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return storm(distribution);
    }

    auto cauchy(Float location, Float scale) -> Float {
        auto const distribution = std::cauchy_distribution<Float> { location, scale };
        return storm(distribution);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        auto const distribution = std::fisher_f_distribution<Float> {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return storm(distribution);
    }

    auto student_t(Float degrees_of_freedom) -> Float {
        auto const distribution = std::student_t_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return storm(distribution);
    }

    /// Pyewacket
    auto randrange(Integer start, Integer stop, Integer step) -> Integer {
        if (start == stop) return randint(-1, 0);
        auto const width = Integer { std::abs(start - stop) - 1 };
        if (step > 0) return std::min(start, stop) + step * randbelow((width + step) / step);
        if (step < 0) return std::max(start, stop) - step * randbelow((width - step) / step);
        else return randint(-1, 0);
    }

    auto betavariate(Float alpha, Float beta) -> Float {
        auto const y = Float { gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + gammavariate(beta, 1.0));
    }

    auto paretovariate(Float alpha) -> Float {
        auto const u = Float { 1.0 - generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    auto vonmisesvariate(Float mu, Float kappa) -> Float {
        auto const PI = Float { 4 * std::atan(1) };
        auto const TAU = Float { 2 * PI };
        if (kappa <= 0.000001) return TAU * generate_canonical();
        auto const s = Float { 0.5 / kappa };
        auto const r = Float { s + std::sqrt(1 + s * s) };
        auto u1 = Float {0};
        auto z = Float {0};
        auto d = Float {0};
        auto u2 = Float {0};
        while (true) {
            u1 = generate_canonical();
            z = std::cos(PI * u1);
            d = z / (r + z);
            u2 = generate_canonical();
            if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
        }
        auto const q = Float { 1.0 / r };
        auto const f = Float { (q + z) / (1.0 + q * z) };
        auto const u3 = Float { generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        else return std::fmod(mu - std::acos(f), TAU);
    }

    auto triangular(Float low, Float high, Float mode) -> Float {
        if (high - low == 0) return low;
        auto u = Float { generate_canonical() };
        auto c = Float { (mode - low) / (high - low) };
        if (u > c) {
            u = 1.0 - u;
            c = 1.0 - c;
            auto const temp = low;
            low = high;
            high = temp;
        }
        return low + (high - low) * std::sqrt(u * c);
    }

    /// Fortuna
    auto percent_true(Float truth_factor) -> Bool {
        return uniform(0.0, 100.0) < truth_factor;
    }

    auto d(Integer sides) -> Integer {
        if (sides > 0) {
            return randint(1, sides);
        } else return analytic_continuation(d, sides);
            }

    auto dice(Integer rolls, Integer sides) -> Integer {
        if (rolls > 0) {
            auto total = Integer {0};
            for (auto i {0}; i < rolls; ++i) total += d(sides);
                return total;
        }
        if (rolls == 0) return 0;
        return -dice(-rolls, sides);
    }

    auto ability_dice(Integer num) -> Integer {
        auto const n { smart_clamp(num, Integer(3), Integer(9)) };
        if (n == 3) return dice(3, 6);
            std::vector<Integer> theRolls(n);
            std::generate(begin(theRolls), end(theRolls), []() { return d(6); });
        std::partial_sort(begin(theRolls), begin(theRolls) + 3, end(theRolls), std::greater<Integer>());
        return std::accumulate(begin(theRolls), begin(theRolls) + 3, 0);
    }

    auto plus_or_minus(Integer number) -> Integer {
        return randint(-number, number);
    }

    auto plus_or_minus_linear(Integer number) -> Integer {
        auto const num { std::abs(number) };
        return dice(2, num + 1) - (num + 2);
    }

    auto randindex(Integer size) {
        if (size > 0) {
            auto const distribution = std::uniform_int_distribution<Integer> {0, size - 1};
            return storm(distribution);
        }
        else if (size < 0) {
            auto const distribution = std::uniform_int_distribution<Integer> {size, -1};
            return storm(distribution);
        }
        else {
            auto const distribution = std::uniform_int_distribution<Integer> {-1, 0};
            return storm(distribution);
        }
    }

    /// QuantumMonty Methods, random index from size: randbelow(size)
    auto fuzzy_clamp(Integer target, Integer upper_bound) -> Integer {
        if (std::abs(target) >= 0 and std::abs(target) < std::abs(upper_bound)) return target;
        else return randindex(upper_bound);
    }

    auto back_gauss(Integer number) -> Integer;

    auto front_gauss(Integer number) -> Integer {
        if (number > 0) {
            auto const result { Integer(gammavariate(1.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(back_gauss, number) - 1;
    }

    auto middle_gauss(Integer number) -> Integer {
        if (number > 0) {
            auto const result { Integer(normalvariate(number / 2.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(middle_gauss, number) - 1;
    }

    auto back_gauss(Integer number) -> Integer {
        if (number > 0) {
            return number - front_gauss(number) - 1;
        }
        else return analytic_continuation(front_gauss, number) - 1;
    }

    auto quantum_gauss(Integer number) -> Integer {
        auto const rand_num { d(3) };
        if (rand_num == 1) return front_gauss(number);
        else if (rand_num == 2) return middle_gauss(number);
        else return back_gauss(number);
    }

    auto back_poisson(Integer number) -> Integer;

    auto front_poisson(Integer number) -> Integer {
        if (number > 0) {
            auto static const PI { 4 * std::atan(1) };
            auto const result { poisson(number / PI) };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(back_poisson, number) - 1;
    }

    auto back_poisson(Integer number) -> Integer {
        if (number > 0) {
            auto result { number - front_poisson(number) - 1 };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(front_poisson, number) - 1;
    }

    auto middle_poisson(Integer number) -> Integer {
        if (percent_true(50)) return front_poisson(number);
        else return back_poisson(number);
    }

    auto quantum_poisson(Integer number) -> Integer {
        auto rand_num { d(3) };
        if (rand_num == 1) return front_poisson(number);
        else if (rand_num == 2) return middle_poisson(number);
        else return back_poisson(number);
    }

    auto back_geometric(Integer number) -> Integer;

    auto front_geometric(Integer number) -> Integer {
        if (number > 0) {
            auto spread { number - 1 };
            auto result { plus_or_minus_linear(spread)};
            while (result < 0) result = plus_or_minus_linear(spread);
            return result;
        }
        else return analytic_continuation(back_geometric, number) - 1;
    }

    auto back_geometric(Integer number) -> Integer {
        if (number > 0) {
            auto spread { number - 1 };
            auto result { plus_or_minus_linear(spread)};
            while (result < 0) result = plus_or_minus_linear(spread);
            return spread - result;
        }
        else return analytic_continuation(front_geometric, number) - 1;
    }

    auto middle_geometric(Integer number) -> Integer {
        if (number > 0) {
            auto half { number / 2 };
            if (number % 2 == 1) return half + plus_or_minus_linear(half);
            else if (percent_true(50)) return back_geometric(half);
            else return half + front_geometric(half);
        }
        else return analytic_continuation(middle_geometric, number) - 1;
    }

    auto quantum_geometric(Integer number) -> Integer {
        auto rand_num { d(3) };
        if (rand_num == 1) return front_geometric(number);
        else if (rand_num == 2) return middle_geometric(number);
        else return back_geometric(number);
    }

    auto quantum_monty(Integer number) -> Integer {
        auto rand_num { d(3) };
        if (rand_num == 1) return quantum_geometric(number);
        else if (rand_num == 2) return quantum_gauss(number);
        else return quantum_poisson(number);
    }

} // end namespace
