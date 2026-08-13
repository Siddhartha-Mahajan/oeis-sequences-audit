#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;

// Fraction-free elimination.  Every division is exact over the integers.
static i64 det_hankel6(const std::array<int, 11>& x) {
    i64 a[6][6];
    for (int i = 0; i < 6; ++i)
        for (int j = 0; j < 6; ++j)
            a[i][j] = x[i + j];
    i64 previous = 1;
    int sign = 1;
    for (int k = 0; k < 5; ++k) {
        int pivot_row = k;
        while (pivot_row < 6 && a[pivot_row][k] == 0) ++pivot_row;
        if (pivot_row == 6) return 0;
        if (pivot_row != k) {
            for (int j = k; j < 6; ++j) std::swap(a[k][j], a[pivot_row][j]);
            sign = -sign;
        }
        const i64 pivot = a[k][k];
        for (int i = k + 1; i < 6; ++i) {
            for (int j = k + 1; j < 6; ++j) {
                i128 numerator = (i128)a[i][j] * pivot - (i128)a[i][k] * a[k][j];
                a[i][j] = (i64)(numerator / previous);
            }
        }
        previous = pivot;
    }
    return sign * a[5][5];
}

struct Best {
    i64 minimum = 0;
    i64 maximum = 0;
    std::array<int, 11> min_x{};
    std::array<int, 11> max_x{};
    std::uint64_t tested = 0;
};

int main(int argc, char** argv) {
    unsigned workers = std::thread::hardware_concurrency();
    if (argc > 1) workers = std::max(1, std::atoi(argv[1]));
    std::vector<std::pair<int, int>> prefixes;
    for (int a = 0; a <= 10; ++a)
        for (int b = 0; b <= 10; ++b)
            if (a != b) prefixes.emplace_back(a, b);

    std::atomic<std::size_t> next{0};
    std::mutex merge_mutex;
    Best global;
    auto work = [&]() {
        Best local;
        while (true) {
            std::size_t task = next.fetch_add(1);
            if (task >= prefixes.size()) break;
            auto [a, b] = prefixes[task];
            std::array<int, 11> x{};
            x[0] = a;
            x[1] = b;
            int q = 2;
            for (int value = 0; value <= 10; ++value)
                if (value != a && value != b) x[q++] = value;
            do {
                // Reversal gives the same determinant, so retain one member
                // of every reversal pair.
                if (x[0] < x[10]) {
                    i64 d = det_hankel6(x);
                    ++local.tested;
                    if (d < local.minimum) { local.minimum = d; local.min_x = x; }
                    if (d > local.maximum) { local.maximum = d; local.max_x = x; }
                }
            } while (std::next_permutation(x.begin() + 2, x.end()));
        }
        std::lock_guard<std::mutex> lock(merge_mutex);
        global.tested += local.tested;
        if (local.minimum < global.minimum) { global.minimum = local.minimum; global.min_x = local.min_x; }
        if (local.maximum > global.maximum) { global.maximum = local.maximum; global.max_x = local.max_x; }
    };

    std::vector<std::thread> pool;
    for (unsigned i = 0; i < workers; ++i) pool.emplace_back(work);
    for (auto& thread : pool) thread.join();

    auto print_array = [](const std::array<int, 11>& x) {
        std::cout << '[';
        for (int i = 0; i < 11; ++i) std::cout << (i ? "," : "") << x[i];
        std::cout << ']';
    };
    std::cout << "tested=" << global.tested << "\nminimum=" << global.minimum << "\nmin_sequence=";
    print_array(global.min_x);
    std::cout << "\nmaximum=" << global.maximum << "\nmax_sequence=";
    print_array(global.max_x);
    std::cout << "\nmax_absolute=" << std::max(-global.minimum, global.maximum) << '\n';
}
