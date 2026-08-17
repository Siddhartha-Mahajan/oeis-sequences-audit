#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

static unsigned long long nodes = 0, pair_calls = 0;
static u64 maximum_q = 0;

static u64 mul_mod(u64 a, u64 b, u64 modulus) {
    return (u128)a * b % modulus;
}

static u64 pow_mod(u64 base, u64 exponent, u64 modulus) {
    u64 result = 1;
    while (exponent) {
        if (exponent & 1) result = mul_mod(result, base, modulus);
        base = mul_mod(base, base, modulus);
        exponent >>= 1;
    }
    return result;
}

static bool is_prime(u64 n) {
    if (n < 2) return false;
    for (u64 p : {2ULL, 3ULL, 5ULL, 7ULL, 11ULL, 13ULL, 17ULL, 19ULL,
                  23ULL, 29ULL, 31ULL, 37ULL}) {
        if (n % p == 0) return n == p;
    }
    u64 d = n - 1, s = 0;
    while ((d & 1) == 0) { d >>= 1; ++s; }
    // This witness set is deterministic for every 64-bit unsigned integer.
    for (u64 a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL,
                  9780504ULL, 1795265022ULL}) {
        if (a % n == 0) continue;
        u64 x = pow_mod(a % n, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (u64 r = 1; r < s; ++r) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { composite = false; break; }
        }
        if (composite) return false;
    }
    return true;
}

static u64 pollard_rho(u64 n) {
    if (n % 2 == 0) return 2;
    if (n % 3 == 0) return 3;
    static std::mt19937_64 rng(3167);
    for (;;) {
        u64 c = 1 + rng() % (n - 1);
        u64 x = 2 + rng() % (n - 2), y = x, divisor = 1;
        auto step = [&](u64 value) {
            return (u64)(((u128)mul_mod(value, value, n) + c) % n);
        };
        while (divisor == 1) {
            x = step(x); y = step(step(y));
            u64 difference = x > y ? x - y : y - x;
            divisor = std::gcd(difference, n);
        }
        if (divisor != n) return divisor;
    }
}

static void factor_rec(u64 n, std::vector<u64>& factors) {
    if (n == 1) return;
    if (is_prime(n)) { factors.push_back(n); return; }
    u64 divisor = pollard_rho(n);
    factor_rec(divisor, factors);
    factor_rec(n / divisor, factors);
}

static std::vector<std::pair<u64,int>> factor(u64 q) {
    std::vector<u64> flat;
    factor_rec(q, flat);
    std::sort(flat.begin(), flat.end());
    std::vector<std::pair<u64,int>> out;
    for (u64 prime : flat) {
        if (out.empty() || out.back().first != prime) out.push_back({prime, 1});
        else ++out.back().second;
    }
    return out;
}

static void divisors_at_most_q(const std::vector<std::pair<u64,int>>& factors,
                               int index, u64 value, u64 q,
                               std::vector<u64>& out) {
    if (index == (int)factors.size()) { out.push_back(value); return; }
    auto [prime, exponent] = factors[index];
    u64 power = 1;
    for (int e = 0; e <= 2 * exponent; ++e) {
        if ((u128)value * power > q) break;
        divisors_at_most_q(factors, index + 1, value * power, q, out);
        if (e != 2 * exponent) {
            if ((u128)power * prime > q) break;
            power *= prime;
        }
    }
}

// Count min <= x <= y with 1/x+1/y=p/q. The standard factorization is
// (p*x-q)(p*y-q)=q^2.
static unsigned long long count_pair(u64 p, u64 q, u64 minimum) {
    ++pair_calls;
    maximum_q = std::max(maximum_q, q);
    auto factors = factor(q);
    std::vector<u64> divisors;
    divisors_at_most_q(factors, 0, 1, q, divisors);
    unsigned long long answer = 0;
    u128 q2 = (u128)q * q;
    for (u64 d : divisors) {
        u128 left = (u128)d + q;
        if (left % p) continue;
        u128 other = q2 / d;
        if ((other + q) % p) continue;
        u128 x128 = left / p;
        if (x128 > UINT64_MAX) {
            std::cerr << "first terminal denominator exceeds 64 bits\n";
            std::exit(2);
        }
        u64 x = (u64)x128;
        if (x < minimum) continue;
        // d<=q implies x<=y; every solution occurs once.
        ++answer;
    }
    return answer;
}

static unsigned long long search(u64 p, u64 q, int remaining, u64 minimum) {
    ++nodes;
    if (remaining == 2) return count_pair(p, q, minimum);
    // x > q/p keeps the remainder positive; r/x >= p/q is necessary.
    u64 lower = std::max(minimum, q / p + 1);
    u64 upper = (u64)((u128)remaining * q / p);
    unsigned long long answer = 0;
    for (u64 x = lower; x <= upper; ++x) {
        u128 numerator128 = (u128)p * x - q;
        if (numerator128 > UINT64_MAX || (u128)q * x > UINT64_MAX) {
            std::cerr << "64-bit rational overflow at p=" << p << " q=" << q
                      << " x=" << x << "\n";
            std::exit(2);
        }
        u64 numerator = (u64)numerator128;
        u64 denominator = q * x;
        u64 g = std::gcd(numerator, denominator);
        numerator /= g; denominator /= g;
        answer += search(numerator, denominator, remaining - 1, x);
        if (x == UINT64_MAX) break;
    }
    return answer;
}

int main(int argc, char** argv) {
    int n = argc > 1 ? std::stoi(argv[1]) : 7;
    std::vector<u64> prefix;
    u64 range_lo = 0, range_hi = 0;
    for (int i = 2; i < argc; ++i) {
        if (std::string(argv[i]) == "--next-range") {
            if (i + 2 >= argc) { std::cerr << "missing range endpoints\n"; return 2; }
            range_lo = std::stoull(argv[++i]);
            range_hi = std::stoull(argv[++i]);
        } else prefix.push_back(std::stoull(argv[i]));
    }
    auto start = std::chrono::steady_clock::now();
    unsigned long long answer;
    if (!prefix.empty()) {
        u64 p = 1, q = 2, minimum = 1;
        int remaining = n;
        for (u64 x : prefix) {
            if (remaining <= 2 || x < minimum || (u128)p * x <= q ||
                    (u128)p * x > (u128)remaining * q) {
                std::cerr << "invalid fixed denominator prefix\n";
                return 2;
            }
            u128 numerator128 = (u128)p * x - q;
            if (numerator128 > UINT64_MAX) {
                std::cerr << "64-bit rational overflow in prefix\n";
                return 2;
            }
            u64 numerator = (u64)numerator128;
            if ((u128)q * x > UINT64_MAX) {
                std::cerr << "64-bit rational overflow in prefix\n";
                return 2;
            }
            u64 denominator = q * x;
            u64 g = std::gcd(numerator, denominator);
            p = numerator / g;
            q = denominator / g;
            minimum = x;
            --remaining;
        }
        if (range_lo) {
            u64 lower = std::max({minimum, q / p + 1, range_lo});
            u64 upper = std::min((u64)((u128)remaining * q / p), range_hi);
            answer = 0;
            for (u64 x = lower; x <= upper; ++x) {
                u128 numerator128 = (u128)p * x - q;
                if (numerator128 > UINT64_MAX) {
                    std::cerr << "64-bit rational overflow in range\n";
                    return 2;
                }
                u64 numerator = (u64)numerator128;
                if ((u128)q * x > UINT64_MAX) {
                    std::cerr << "64-bit rational overflow in range\n";
                    return 2;
                }
                u64 denominator = q * x;
                u64 g = std::gcd(numerator, denominator);
                answer += search(numerator / g, denominator / g,
                                 remaining - 1, x);
            }
        } else answer = search(p, q, remaining, minimum);
    } else {
        answer = search(1, 2, n, 1);
    }
    double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
    std::cout << "n " << n << "\nprefix";
    for (u64 x : prefix) std::cout << " " << x;
    std::cout << "\ncount " << answer
              << "\nnext_range " << range_lo << " " << range_hi
              << "\nsearch_nodes " << nodes << "\npair_calls " << pair_calls
              << "\nmaximum_terminal_denominator " << maximum_q
              << "\nseconds " << seconds << "\n";
}
