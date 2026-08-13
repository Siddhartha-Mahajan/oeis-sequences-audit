#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

using Matrix = std::uint16_t;

static Matrix multiply(Matrix a, Matrix b) {
    std::uint8_t brow[4];
    for (int i = 0; i < 4; ++i) brow[i] = (b >> (4 * i)) & 15;
    std::uint8_t image[16] = {};
    for (int mask = 1; mask < 16; ++mask) {
        int bit = __builtin_ctz(mask);
        image[mask] = image[mask ^ (1 << bit)] | brow[bit];
    }
    Matrix out = 0;
    for (int i = 0; i < 4; ++i)
        out |= Matrix(image[(a >> (4 * i)) & 15]) << (4 * i);
    return out;
}

class Closure {
  public:
    int size(const std::array<Matrix, 3>& generators) {
        ++stamp_;
        if (stamp_ == 0) {
            std::fill(seen_.begin(), seen_.end(), 0);
            stamp_ = 1;
        }
        queue_.clear();
        for (Matrix g : generators) add(g);
        for (std::size_t head = 0; head < queue_.size(); ++head) {
            Matrix x = queue_[head];
            for (Matrix g : generators) add(multiply(x, g));
        }
        return (int)queue_.size();
    }

  private:
    std::vector<std::uint32_t> seen_ = std::vector<std::uint32_t>(65536);
    std::uint32_t stamp_ = 0;
    std::vector<Matrix> queue_;
    void add(Matrix x) {
        if (seen_[x] != stamp_) {
            seen_[x] = stamp_;
            queue_.push_back(x);
        }
    }
};

static Matrix rows(const char* a, const char* b, const char* c, const char* d) {
    const char* rs[4] = {a, b, c, d};
    Matrix m = 0;
    for (int i = 0; i < 4; ++i)
        for (int j = 0; j < 4; ++j)
            if (rs[i][j] == '1') m |= Matrix(1) << (4 * i + j);
    return m;
}

static std::string bits(Matrix m) {
    std::string s;
    for (int i = 0; i < 4; ++i) {
        if (i) s += '/';
        for (int j = 0; j < 4; ++j) s += ((m >> (4 * i + j)) & 1) ? '1' : '0';
    }
    return s;
}

int main(int argc, char** argv) {
    const std::uint64_t trials = argc >= 2 ? std::stoull(argv[1]) : 20000;
    const std::uint64_t seed = argc >= 3 ? std::stoull(argv[2]) : 358784;
    const std::string output = argc >= 4 ? argv[3] : "";
    const std::string mode = argc >= 5 ? argv[4] : "mutation";
    const bool exhaustive = mode == "exhaust-first" || mode == "exhaust-middle" || mode == "exhaust-third";
    std::mt19937_64 rng(seed);
    Closure closure;
    std::array<Matrix, 3> published = {
        rows("0001", "1000", "0100", "0010"),
        rows("0001", "0010", "0100", "1001"),
        rows("0000", "0001", "0010", "0100")
    };
    std::array<Matrix, 3> improved = {
        rows("0001", "1000", "0100", "0010"),
        rows("0011", "0001", "0100", "1000"),
        rows("0000", "0001", "0010", "0100")
    };
    std::array<Matrix, 3> best = improved;
    int published_size = closure.size(published);
    int best_size = closure.size(best);
    std::uint64_t improvements = 0;

    // Search a reproducible mixture of single-bit neighborhoods and perturbed
    // restarts around the incumbent.  Every reported score is recomputed from
    // scratch by exact closure, so the heuristic affects discovery only.
    const std::uint64_t evaluations = exhaustive ? 65536 : trials;
    for (std::uint64_t trial = 0; trial < evaluations; ++trial) {
        if (exhaustive) {
            std::array<Matrix, 3> candidate = improved;
            const int position = mode == "exhaust-first" ? 0 : mode == "exhaust-middle" ? 1 : 2;
            candidate[position] = (Matrix)trial;
            int score = closure.size(candidate);
            if (score > best_size) {
                best = candidate;
                best_size = score;
                ++improvements;
                std::cerr << "improvement " << best_size << " at middle generator " << trial << "\n";
            }
            continue;
        }
        std::array<Matrix, 3> candidate = best;
        int flips = (trial % 64 == 0) ? 1 : 2 + (rng() % 8);
        for (int f = 0; f < flips; ++f) {
            int bit = rng() % 48;
            candidate[bit / 16] ^= Matrix(1) << (bit % 16);
        }
        int score = closure.size(candidate);
        if (score > best_size) {
            best = candidate;
            best_size = score;
            ++improvements;
            std::cerr << "improvement " << best_size << " at trial " << trial << "\n";
        }
        // Periodic wider restarts prevent a strict local maximum from making
        // every remaining evaluation identical in character.
        if (trial % 257 == 256) {
            candidate = published;
            for (int f = 0; f < 4 + int(rng() % 13); ++f) {
                int bit = rng() % 48;
                candidate[bit / 16] ^= Matrix(1) << (bit % 16);
            }
            int score2 = closure.size(candidate);
            if (score2 > best_size) {
                best = candidate;
                best_size = score2;
                ++improvements;
            }
        }
    }

    // Independent final recomputation catches accidental stale-score bugs.
    int verified = closure.size(best);
    std::string json = "{\n";
    json += "  \"dimension\": 4,\n";
    json += "  \"mode\": \"" + mode + "\",\n";
    json += "  \"evaluations\": " + std::to_string(evaluations) + ",\n";
    json += "  \"seed\": " + std::to_string(seed) + ",\n";
    json += "  \"published_size_recomputed\": " + std::to_string(published_size) + ",\n";
    json += "  \"best_size\": " + std::to_string(best_size) + ",\n";
    json += "  \"final_recomputed_size\": " + std::to_string(verified) + ",\n";
    json += "  \"strict_improvements\": " + std::to_string(improvements) + ",\n";
    json += "  \"generators\": [\"" + bits(best[0]) + "\", \"" + bits(best[1]) + "\", \"" + bits(best[2]) + "\"]\n";
    json += "}\n";
    std::cout << json;
    if (!output.empty()) { std::ofstream out(output); out << json; }
}
