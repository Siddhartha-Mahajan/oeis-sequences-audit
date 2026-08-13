#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

// Exact ordered merge of the streams
//   P_n(i), P_n(i)+P_n(i+1), P_n(i)+P_n(i+1)+P_n(i+2), ... .
// Every interval of consecutive positive n-gonal numbers occurs once.  Since
// the priority queue is sorted by its sum, the first sum with multiplicity n
// is A343777(n), provided it is at most the supplied bound.

using u64 = std::uint64_t;

static u64 polygonal(unsigned sides, u64 k) {
    __int128 value = (__int128)((int)sides - 2) * k * k
                   - (__int128)((int)sides - 4) * k;
    value /= 2;
    if (value < 0 || (__uint128_t)value > UINT64_MAX) {
        std::cerr << "polygonal value overflow\n";
        std::exit(2);
    }
    return (u64)value;
}

struct Node {
    u64 sum;
    u64 first;
    u64 last;
};

struct Greater {
    bool operator()(const Node& a, const Node& b) const {
        if (a.sum != b.sum) return a.sum > b.sum;
        if (a.first != b.first) return a.first > b.first;
        return a.last > b.last;
    }
};

int main(int argc, char** argv) {
    if (argc < 3 || argc > 4) {
        std::cerr << "usage: consecutive_polygonal_search SIDES MAX_SUM [JSON_OUT]\n";
        return 2;
    }
    const unsigned sides = (unsigned)std::stoul(argv[1]);
    const u64 max_sum = std::stoull(argv[2]);
    if (sides < 3) return 2;

    std::priority_queue<Node, std::vector<Node>, Greater> heap;
    u64 max_start = 0;
    for (u64 i = 1;; ++i) {
        u64 p = polygonal(sides, i);
        if (p > max_sum) break;
        heap.push({p, i, i});
        max_start = i;
    }

    u64 distinct_sums = 0;
    u64 intervals = 0;
    bool found = false;
    u64 answer = 0;
    std::vector<Node> group;
    while (!heap.empty()) {
        const u64 value = heap.top().sum;
        group.clear();
        while (!heap.empty() && heap.top().sum == value) {
            group.push_back(heap.top());
            heap.pop();
        }
        ++distinct_sums;
        intervals += group.size();
        if (group.size() == sides) {
            found = true;
            answer = value;
            break;
        }
        for (const Node& node : group) {
            const u64 next = node.last + 1;
            const u64 add = polygonal(sides, next);
            if (add <= max_sum - node.sum)
                heap.push({node.sum + add, node.first, next});
        }
    }

    std::string json = "{\n";
    json += "  \"sides\": " + std::to_string(sides) + ",\n";
    json += "  \"status\": \"" + std::string(found ? "found" : "not_found") + "\",\n";
    if (found) json += "  \"value\": " + std::to_string(answer) + ",\n";
    json += "  \"max_sum\": " + std::to_string(max_sum) + ",\n";
    json += "  \"max_start_index\": " + std::to_string(max_start) + ",\n";
    json += "  \"distinct_represented_sums_examined\": " + std::to_string(distinct_sums) + ",\n";
    json += "  \"intervals_examined\": " + std::to_string(intervals) + "\n";
    json += "}\n";
    std::cout << json;
    if (argc == 4) {
        std::ofstream out(argv[3]);
        out << json;
    }
    return 0;
}
