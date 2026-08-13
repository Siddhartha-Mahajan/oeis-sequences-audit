#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

// Certified lower bounds for A007847(n).  Enumerate nondecreasing primitive
// absolute normal vectors 0 <= a_1 <= ... <= a_n <= B.  For each level,
// verify affine spanning and add the exact cube-symmetry orbit.

using u64 = std::uint64_t;
using u128 = unsigned __int128;
static constexpr std::int64_t P = 1000000007;

static int n, bound;
static std::array<int, 12> a{};
static std::vector<u128> by_height, full_by_height;
static std::vector<u64> type_count, full_type_count;

static std::string decimal(u128 x) {
    if (!x) return "0";
    std::string s;
    while (x) { s.push_back(char('0' + x % 10)); x /= 10; }
    return std::string(s.rbegin(), s.rend());
}

static std::int64_t modpow(std::int64_t x, std::int64_t e) {
    std::int64_t y = 1;
    while (e) {
        if (e & 1) y = y * x % P;
        x = x * x % P;
        e >>= 1;
    }
    return y;
}

static int affine_rank(const std::vector<unsigned>& points) {
    if (points.empty()) return -1;
    std::array<std::array<std::int64_t, 12>, 12> basis{};
    std::array<bool, 12> used{};
    int rank = 0;
    unsigned base = points.front();
    for (std::size_t z = 1; z < points.size() && rank < n - 1; ++z) {
        std::array<std::int64_t, 12> row{};
        unsigned q = points[z];
        for (int j = 0; j < n; ++j) {
            int d = int((q >> j) & 1U) - int((base >> j) & 1U);
            row[j] = d < 0 ? P - 1 : d;
        }
        for (int col = 0; col < n; ++col) {
            if (!row[col]) continue;
            if (used[col]) {
                auto factor = row[col];
                for (int j = col; j < n; ++j) {
                    row[j] = (row[j] - factor * basis[col][j]) % P;
                    if (row[j] < 0) row[j] += P;
                }
            } else {
                auto inv = modpow(row[col], P - 2);
                for (int j = col; j < n; ++j) row[j] = row[j] * inv % P;
                basis[col] = row;
                used[col] = true;
                ++rank;
                break;
            }
        }
    }
    return rank;
}

static u128 factorial(int k) {
    u128 r = 1;
    for (int i = 2; i <= k; ++i) r *= unsigned(i);
    return r;
}

static void evaluate() {
    int g = 0, total = 0, nonzero = 0;
    for (int i = 0; i < n; ++i) {
        g = std::gcd(g, a[i]);
        total += a[i];
        nonzero += a[i] != 0;
    }
    if (g != 1) return;
    int height = a[n - 1];
    u128 placements = factorial(n);
    for (int i = 0, j; i < n; i = j) {
        for (j = i + 1; j < n && a[j] == a[i]; ++j) {}
        placements /= factorial(j - i);
    }
    std::vector<std::vector<unsigned>> levels(total / 2 + 1);
    for (unsigned x = 0; x < (1U << n); ++x) {
        int s = 0;
        for (int i = 0; i < n; ++i) if ((x >> i) & 1U) s += a[i];
        if (s <= total / 2) levels[s].push_back(x);
    }
    for (int b = 0; b <= total / 2; ++b) {
        if (affine_rank(levels[b]) != n - 1) continue;
        u128 orbit = placements;
        orbit <<= (nonzero - (2 * b == total ? 1 : 0));
        by_height[height] += orbit;
        ++type_count[height];
        if (nonzero == n) {
            full_by_height[height] += orbit;
            ++full_type_count[height];
        }
    }
}

static void generate(int pos, int minimum) {
    if (pos == n) { evaluate(); return; }
    for (int v = minimum; v <= bound; ++v) {
        a[pos] = v;
        generate(pos + 1, v);
    }
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: " << argv[0] << " dimension coefficient_bound\n";
        return 2;
    }
    n = std::atoi(argv[1]);
    bound = std::atoi(argv[2]);
    if (n < 2 || n > 11 || bound < 1) return 2;
    by_height.assign(bound + 1, 0);
    full_by_height.assign(bound + 1, 0);
    type_count.assign(bound + 1, 0);
    full_type_count.assign(bound + 1, 0);
    generate(0, 0);
    u128 cumulative = 0, full_cumulative = 0;
    u64 types = 0, full_types = 0;
    for (int h = 1; h <= bound; ++h) {
        cumulative += by_height[h];
        full_cumulative += full_by_height[h];
        types += type_count[h];
        full_types += full_type_count[h];
        std::cout << "B=" << h << " types=" << types
                  << " lower_bound=" << decimal(cumulative)
                  << " full_support_types=" << full_types
                  << " full_support_lower_bound=" << decimal(full_cumulative)
                  << "\n";
    }
}
