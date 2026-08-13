#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

struct Graph {
  int n;
  std::vector<uint16_t> adj;
  std::unordered_map<uint32_t, uint64_t> aut_cache;
  std::unordered_map<uint16_t, bool> stable_cache;

  uint64_t automorphisms(uint16_t mask, int fixed = -1) {
    uint32_t key = uint32_t(mask) | (uint32_t(fixed + 1) << 16);
    auto found = aut_cache.find(key);
    if (found != aut_cache.end()) return found->second;
    std::vector<int> vertices;
    int degree[16] = {};
    for (int v = 0; v < n; ++v) if (mask & (1u << v)) {
      vertices.push_back(v);
      degree[v] = __builtin_popcount(adj[v] & mask);
    }
    int image[16];
    std::fill(image, image + 16, -1);
    uint16_t used = 0;
    if (fixed >= 0) {
      image[fixed] = fixed;
      used |= uint16_t(1u << fixed);
    }
    uint64_t total = 0;
    auto search = [&](auto&& self, int assigned) -> void {
      if (assigned == (int)vertices.size()) { ++total; return; }
      int best = -1;
      std::vector<int> candidates, best_candidates;
      for (int u : vertices) if (image[u] < 0) {
        candidates.clear();
        for (int w : vertices) if (!(used & (1u << w)) && degree[u] == degree[w]) {
          bool ok = true;
          for (int x : vertices) if (image[x] >= 0) {
            if (((adj[u] >> x) & 1u) != ((adj[w] >> image[x]) & 1u)) {
              ok = false; break;
            }
          }
          if (ok) candidates.push_back(w);
        }
        if (candidates.empty()) return;
        if (best < 0 || candidates.size() < best_candidates.size()) {
          best = u; best_candidates = candidates;
        }
      }
      for (int w : best_candidates) {
        image[best] = w; used |= uint16_t(1u << w);
        self(self, assigned + 1);
        used &= uint16_t(~(1u << w)); image[best] = -1;
      }
    };
    int initially = fixed >= 0 ? 1 : 0;
    search(search, initially);
    aut_cache[key] = total;
    return total;
  }

  bool stable(uint16_t mask) {
    if (!mask) return true;
    auto found = stable_cache.find(mask);
    if (found != stable_cache.end()) return found->second;
    for (int v = 0; v < n; ++v) if (mask & (1u << v)) {
      uint16_t smaller = mask & uint16_t(~(1u << v));
      if (automorphisms(mask, v) == automorphisms(smaller) && stable(smaller)) {
        return stable_cache[mask] = true;
      }
    }
    return stable_cache[mask] = false;
  }
};

Graph decode(const std::string& line) {
  Graph g;
  g.n = int(line[0]) - 63;
  g.adj.assign(g.n, 0);
  std::vector<int> bits;
  for (size_t i = 1; i < line.size(); ++i) {
    int x = int(line[i]) - 63;
    for (int shift = 5; shift >= 0; --shift) bits.push_back((x >> shift) & 1);
  }
  int pos = 0;
  for (int high = 1; high < g.n; ++high) for (int low = 0; low < high; ++low) {
    if (bits[pos]) {
      g.adj[low] |= uint16_t(1u << high);
      g.adj[high] |= uint16_t(1u << low);
    }
    ++pos;
  }
  return g;
}

int main(int argc, char** argv) {
  if (argc < 3) {
    std::cerr << "usage: verify_group_counts expected file.g6\n";
    return 2;
  }
  int expected = std::stoi(argv[1]);
  std::ifstream input(argv[2]);
  std::string line;
  int total = 0, stable = 0;
  while (std::getline(input, line)) if (!line.empty()) {
    ++total;
    Graph graph = decode(line);
    if (graph.stable(uint16_t((1u << graph.n) - 1))) ++stable;
  }
  std::cout << "input=" << total << " stable=" << stable << "\n";
  if (stable != expected) return 1;
  return 0;
}
