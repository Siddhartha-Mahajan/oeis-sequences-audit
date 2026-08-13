#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

static bool valid(const std::vector<int>& sequence, int n) {
    for (std::size_t i = 1; i < sequence.size(); ++i)
        if (sequence[i] == sequence[i - 1]) return false;
    for (int a = 0; a < n; ++a) for (int b = a + 1; b < n; ++b) {
        int last = -1, runs = 0;
        for (int x : sequence) if (x == a || x == b) {
            if (x != last) { last = x; ++runs; }
        }
        if (runs >= 7) return false;
    }
    return true;
}

int main(int argc, char** argv) {
    int n = argc > 1 ? std::stoi(argv[1]) : 7;
    long long steps = argc > 2 ? std::stoll(argv[2]) : 2000000;
    std::uint64_t seed = argc > 3 ? std::stoull(argv[3]) : 15283;
    std::mt19937_64 rng(seed);
    std::vector<int> current(n), best;
    for (int i = 0; i < n; ++i) current[i] = i;
    std::shuffle(current.begin(), current.end(), rng);
    best = current;

    auto refill = [&]() {
        bool changed = true;
        while (changed) {
            changed = false;
            std::vector<std::pair<int, int>> moves;
            for (int position = 0; position <= (int)current.size(); ++position)
                for (int symbol = 0; symbol < n; ++symbol) {
                    current.insert(current.begin() + position, symbol);
                    bool ok = valid(current, n);
                    current.erase(current.begin() + position);
                    if (ok) moves.push_back({position, symbol});
                }
            if (!moves.empty()) {
                auto [position, symbol] = moves[rng() % moves.size()];
                current.insert(current.begin() + position, symbol);
                changed = true;
            }
        }
    };

    refill();
    best = current;
    for (long long step = 0; step < steps; ++step) {
        std::vector<int> backup = current;
        int remove = 1 + (rng() % 4);
        while (remove-- && !current.empty())
            current.erase(current.begin() + (rng() % current.size()));
        refill();
        if (current.size() > best.size()) best = current;
        if (current.size() + (rng() % 3) < backup.size()) current = backup;
        if (step && step % 20000 == 0) current = best;
    }
    std::cout << "n " << n << "\nlength " << best.size() << "\nsequence ";
    for (int x : best) std::cout << char('a' + x);
    std::cout << "\n";
}
