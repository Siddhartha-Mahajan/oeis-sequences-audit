#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <unordered_set>

struct Point { int x, y; };
static constexpr Point MOVES[8] = {{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};

static std::uint64_t key(Point p) {
    return (std::uint64_t)(std::uint32_t)p.x << 32 | (std::uint32_t)p.y;
}

// Exact knight distance on the infinite board.
static int knight_distance(Point a, Point b) {
    int x = std::abs(a.x - b.x), y = std::abs(a.y - b.y);
    if (x < y) std::swap(x, y);
    if (x == 1 && y == 0) return 3;
    if (x == 2 && y == 2) return 4;
    int d = std::max((x + 1) / 2, (x + y + 2) / 3);
    d += (d + x + y) & 1;
    return d;
}

class Counter {
public:
    explicit Counter(int target_) : target(target_) {
        // The reversed path begins with (0,0)->(1,2).  The seven other
        // neighbors of the trap square must also be visited.
        int q = 0;
        for (Point m : MOVES) if (!(m.x == 1 && m.y == 2)) required[q++] = m;
        const int full = 1 << 7;
        for (int i = 0; i < 7; ++i) route[i][0] = 0;
        for (int mask = 1; mask < full; ++mask) {
            for (int i = 0; i < 7; ++i) {
                int best = 999;
                for (int j = 0; j < 7; ++j) if (mask & (1 << j))
                    best = std::min(best, knight_distance(required[i], required[j])
                                           + route[j][mask ^ (1 << j)]);
                route[i][mask] = best;
            }
        }
        visited.insert(key({0,0}));
        visited.insert(key({1,2}));
    }

    std::uint64_t run() { return dfs({1,2}, 1, 0); }

private:
    int target;
    Point required[7];
    int route[7][1 << 7]{};
    std::unordered_set<std::uint64_t> visited;

    int remaining_mask() const {
        int mask = 0;
        for (int i = 0; i < 7; ++i)
            if (!visited.count(key(required[i]))) mask |= 1 << i;
        return mask;
    }

    int cover_lower_bound(Point here, int mask) const {
        if (!mask) return 0;
        int best = 999;
        for (int j = 0; j < 7; ++j) if (mask & (1 << j))
            best = std::min(best, knight_distance(here, required[j])
                                   + route[j][mask ^ (1 << j)]);
        return best;
    }

    std::uint64_t dfs(Point here, int depth, int mask_unused) {
        (void)mask_unused;
        int mask = remaining_mask();
        if (cover_lower_bound(here, mask) > target - depth) return 0;
        if (depth == target) return mask == 0 ? 1 : 0;
        std::uint64_t total = 0;
        for (Point d : MOVES) {
            Point next{here.x + d.x, here.y + d.y};
            auto k = key(next);
            if (visited.insert(k).second) {
                total += dfs(next, depth + 1, mask);
                visited.erase(k);
            }
        }
        return total;
    }
};

int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "usage: count_trapped MOVES\n"; return 2; }
    int n = std::atoi(argv[1]);
    Counter counter(n);
    std::cout << "n=" << n << " count=" << counter.run() << '\n';
}
