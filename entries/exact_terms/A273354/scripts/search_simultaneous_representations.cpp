#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

using u64 = std::uint64_t;

struct Node { u64 sum; std::uint32_t a, b; };
struct Greater { bool operator()(const Node& x, const Node& y) const {
    if (x.sum != y.sum) return x.sum > y.sum;
    if (x.a != y.a) return x.a > y.a;
    return x.b > y.b;
}};

static u64 cube(u64 x) { return x*x*x; }

static u64 isqrt(u64 n) {
    u64 x = (u64)std::sqrt((long double)n);
    while ((__uint128_t)(x+1)*(x+1) <= n) ++x;
    while ((__uint128_t)x*x > n) --x;
    return x;
}

static std::vector<std::uint32_t> primes_through(std::uint32_t n) {
    std::vector<bool> composite(n+1);
    std::vector<std::uint32_t> primes;
    for (std::uint32_t p=2; p<=n; ++p) if (!composite[p]) {
        primes.push_back(p);
        if ((u64)p*p <= n) for (u64 q=(u64)p*p; q<=n; q+=p) composite[(std::size_t)q]=true;
    }
    return primes;
}

// Number of unordered representations x^2+y^2=n with 1<=x<=y.
static u64 positive_square_pairs(u64 n, const std::vector<std::uint32_t>& primes) {
    u64 remaining=n, product=1;
    bool forbidden=false;
    for (u64 p: primes) {
        if (p*p > remaining) break;
        if (remaining%p) continue;
        unsigned e=0;
        do { remaining/=p; ++e; } while (remaining%p==0);
        if (p%4==3 && e%2) forbidden=true;
        if (p%4==1) product*=e+1;
    }
    if (remaining>1) {
        if (remaining%4==3) forbidden=true;
        if (remaining%4==1) product*=2;
    }
    const u64 r2 = forbidden ? 0 : 4*product;
    const u64 root=isqrt(n);
    const u64 axis = root*root==n ? 4 : 0;
    const u64 halfroot = n%2==0 ? isqrt(n/2) : 0;
    const u64 diagonal = n%2==0 && halfroot*halfroot==n/2 ? 1 : 0;
    return (r2-axis+4*diagonal)/8;
}

int main(int argc,char**argv) {
    if(argc<3||argc>4){std::cerr<<"usage: search N MAX_SUM [JSON_OUT]\n";return 2;}
    unsigned target=std::stoul(argv[1]); u64 max_sum=std::stoull(argv[2]);
    auto primes=primes_through((std::uint32_t)isqrt(max_sum));
    std::priority_queue<Node,std::vector<Node>,Greater> heap;
    std::uint32_t max_a=0;
    for(u64 a=1;2*cube(a)<=max_sum;++a){heap.push({2*cube(a),(std::uint32_t)a,(std::uint32_t)a});max_a=a;}
    u64 sums=0,pairs=0,cube_groups_of_target_size=0,answer=0; bool found=false;
    std::vector<Node> group;
    while(!heap.empty()){
        u64 value=heap.top().sum; group.clear();
        while(!heap.empty()&&heap.top().sum==value){group.push_back(heap.top());heap.pop();}
        ++sums;pairs+=group.size();
        if(group.size()==target){
            ++cube_groups_of_target_size;
            if(positive_square_pairs(value,primes)==target){found=true;answer=value;break;}
        }
        for(auto node:group){
            u64 nb=(u64)node.b+1, add=cube(nb)-cube(node.b);
            if(add<=max_sum-node.sum) heap.push({node.sum+add,node.a,(std::uint32_t)nb});
        }
    }
    std::string j="{\n";
    j+="  \"target_multiplicity\": "+std::to_string(target)+",\n";
    j+="  \"status\": \""+std::string(found?"found":"not_found")+"\",\n";
    if(found)j+="  \"value\": "+std::to_string(answer)+",\n";
    j+="  \"max_sum\": "+std::to_string(max_sum)+",\n";
    j+="  \"max_first_cube_index\": "+std::to_string(max_a)+",\n";
    j+="  \"distinct_cube_sums_examined\": "+std::to_string(sums)+",\n";
    j+="  \"cube_pairs_examined\": "+std::to_string(pairs)+",\n";
    j+="  \"cube_groups_of_target_size_tested\": "+std::to_string(cube_groups_of_target_size)+"\n}\n";
    std::cout<<j; if(argc==4){std::ofstream out(argv[3]);out<<j;}
}
