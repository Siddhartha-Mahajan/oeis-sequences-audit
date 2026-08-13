#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <vector>

// Exact computation of A007234(n).  Vertices are permutations in lexicographic
// order and an (undirected) edge joins sigma to sigma^2.  A loop forbids its
// endpoint.  The underlying simple graph is a pseudoforest, so repeatedly
// taking an isolated vertex or a leaf and deleting its neighbor is an exact
// maximum-independent-set algorithm; the remaining components are cycles.

static uint32_t rank_permutation(const std::vector<unsigned char>& p,
                                 const std::vector<uint64_t>& fact) {
    uint32_t rank = 0;
    unsigned used = 0;
    const unsigned n = p.size();
    for (unsigned i = 0; i < n; ++i) {
        const unsigned below = (1u << p[i]) - 1u;
        const unsigned digit = __builtin_popcount(below & ~used);
        rank += static_cast<uint32_t>(digit * fact[n - 1 - i]);
        used |= 1u << p[i];
    }
    return rank;
}

static void erase_vertex(uint32_t v, std::vector<unsigned char>& active,
                         std::vector<uint32_t>& degree,
                         const std::vector<uint64_t>& offset,
                         const std::vector<uint32_t>& adjacency,
                         std::queue<uint32_t>& leaves) {
    if (!active[v]) return;
    active[v] = 0;
    for (uint64_t j = offset[v]; j < offset[v + 1]; ++j) {
        const uint32_t u = adjacency[j];
        if (active[u]) {
            if (degree[u] == 0) throw std::runtime_error("degree underflow");
            --degree[u];
            if (degree[u] <= 1) leaves.push(u);
        }
    }
    degree[v] = 0;
}

int main(int argc, char** argv) {
    if (argc < 2 || argc > 4) {
        std::cerr << "usage: " << argv[0]
                  << " n [certificate.txt [selected_ranks.txt]]\n";
        return 2;
    }
    const unsigned n = std::stoul(argv[1]);
    if (n == 0 || n > 11) {
        std::cerr << "this implementation supports 1 <= n <= 11\n";
        return 2;
    }
    std::vector<uint64_t> fact(n + 1, 1);
    for (unsigned k = 1; k <= n; ++k) fact[k] = fact[k - 1] * k;
    const uint64_t N64 = fact[n];
    if (N64 > UINT32_MAX) throw std::runtime_error("vertex index overflow");
    const uint32_t N = static_cast<uint32_t>(N64);

    std::vector<uint32_t> image(N);
    std::vector<unsigned char> p(n), square(n);
    std::iota(p.begin(), p.end(), 0);
    uint32_t id = 0;
    do {
        for (unsigned i = 0; i < n; ++i) square[i] = p[p[i]];
        image[id++] = rank_permutation(square, fact);
    } while (std::next_permutation(p.begin(), p.end()));
    if (id != N) throw std::runtime_error("permutation enumeration mismatch");

    // Build the underlying simple graph.  A directed 2-cycle contributes one
    // undirected edge, not two.  Loops are recorded separately.
    std::vector<unsigned char> loop(N, 0);
    std::vector<uint32_t> degree(N, 0);
    uint64_t edges = 0;
    for (uint32_t v = 0; v < N; ++v) {
        const uint32_t u = image[v];
        if (u == v) {
            loop[v] = 1;
        } else if (!(image[u] == v && u < v)) {
            ++degree[v];
            ++degree[u];
            ++edges;
        }
    }
    std::vector<uint64_t> offset(N + 1, 0);
    for (uint32_t v = 0; v < N; ++v) offset[v + 1] = offset[v] + degree[v];
    if (offset[N] != 2 * edges) throw std::runtime_error("edge count mismatch");
    std::vector<uint32_t> adjacency(offset[N]);
    std::vector<uint64_t> cursor = offset;
    for (uint32_t v = 0; v < N; ++v) {
        const uint32_t u = image[v];
        if (u != v && !(image[u] == v && u < v)) {
            adjacency[cursor[v]++] = u;
            adjacency[cursor[u]++] = v;
        }
    }

    std::vector<unsigned char> active(N, 1);
    std::vector<unsigned char> selected(N, 0);
    std::queue<uint32_t> leaves;
    uint64_t fixed_points = 0;
    for (uint32_t v = 0; v < N; ++v) {
        if (loop[v]) {
            ++fixed_points;
            erase_vertex(v, active, degree, offset, adjacency, leaves);
        }
    }
    for (uint32_t v = 0; v < N; ++v)
        if (active[v] && degree[v] <= 1) leaves.push(v);

    uint64_t answer = 0, leaf_choices = 0, isolated_choices = 0;
    while (!leaves.empty()) {
        const uint32_t v = leaves.front();
        leaves.pop();
        if (!active[v] || degree[v] > 1) continue;
        uint32_t neighbor = UINT32_MAX;
        if (degree[v] == 1) {
            for (uint64_t j = offset[v]; j < offset[v + 1]; ++j)
                if (active[adjacency[j]]) { neighbor = adjacency[j]; break; }
            if (neighbor == UINT32_MAX) throw std::runtime_error("missing leaf neighbor");
            ++leaf_choices;
        } else {
            ++isolated_choices;
        }
        ++answer;
        selected[v] = 1;
        erase_vertex(v, active, degree, offset, adjacency, leaves);
        if (neighbor != UINT32_MAX)
            erase_vertex(neighbor, active, degree, offset, adjacency, leaves);
    }

    // What remains must be a disjoint union of simple cycles.
    std::vector<unsigned char> seen(N, 0);
    std::vector<uint64_t> cycle_hist(N + 1, 0);
    uint64_t cycle_vertices = 0, cycle_components = 0;
    for (uint32_t start = 0; start < N; ++start) {
        if (!active[start] || seen[start]) continue;
        std::vector<uint32_t> cycle;
        uint32_t previous = UINT32_MAX, v = start;
        do {
            seen[v] = 1;
            if (degree[v] != 2) throw std::runtime_error("non-cycle core");
            cycle.push_back(v);
            uint32_t next = UINT32_MAX;
            for (uint64_t j = offset[v]; j < offset[v + 1]; ++j) {
                const uint32_t u = adjacency[j];
                if (active[u] && u != previous) { next = u; break; }
            }
            if (next == UINT32_MAX) throw std::runtime_error("broken cycle traversal");
            previous = v;
            v = next;
        } while (v != start);
        const uint64_t length = cycle.size();
        ++cycle_components;
        cycle_vertices += length;
        ++cycle_hist[length];
        answer += length / 2;
        for (uint64_t j = 0; j < length / 2; ++j) selected[cycle[2 * j]] = 1;
    }

    std::cout << "n=" << n << "\n"
              << "vertices=" << N << "\n"
              << "simple_edges=" << edges << "\n"
              << "fixed_points=" << fixed_points << "\n"
              << "leaf_choices=" << leaf_choices << "\n"
              << "isolated_choices=" << isolated_choices << "\n"
              << "cycle_components=" << cycle_components << "\n"
              << "cycle_vertices=" << cycle_vertices << "\n"
              << "a(" << n << ")=" << answer << "\n";
    for (uint32_t k = 2; k <= N; ++k)
        if (cycle_hist[k]) std::cout << "cycles_length_" << k << "=" << cycle_hist[k] << "\n";

    if (argc >= 3) {
        std::ofstream out(argv[2]);
        if (!out) throw std::runtime_error("cannot open certificate output");
        out << "A007234 functional-graph reduction certificate\n"
            << "n " << n << "\nvertices " << N << "\nsimple_edges " << edges
            << "\nfixed_points " << fixed_points << "\nleaf_choices " << leaf_choices
            << "\nisolated_choices " << isolated_choices << "\ncycle_components "
            << cycle_components << "\ncycle_vertices " << cycle_vertices
            << "\nanswer " << answer << "\n";
        for (uint32_t k = 2; k <= N; ++k)
            if (cycle_hist[k]) out << "cycle_length " << k << " count " << cycle_hist[k] << "\n";
    }
    if (argc >= 4) {
        std::ofstream out(argv[3]);
        if (!out) throw std::runtime_error("cannot open selected-rank output");
        out << "# lexicographic zero-based ranks of a maximum x -> x^2-free subset of S_"
            << n << "\n";
        uint64_t written = 0;
        for (uint32_t v = 0; v < N; ++v)
            if (selected[v]) { out << v << "\n"; ++written; }
        if (written != answer) throw std::runtime_error("witness size mismatch");
    }
    return 0;
}
